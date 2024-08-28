from itertools import chain
import numpy as np
import cv2 as cv
import sys
import cmapy
import ffmpegcv
from PIL import Image, ImageDraw
from dataclasses import dataclass
import customtkinter
import time
import copy
from sys import getsizeof
from matplotlib import cm

import matplotlib.pyplot as plt

COEF_FADE_IN = 1.00
COEF_FADE_OUT = 0.90
HEATMAP_CEIL = COEF_FADE_IN * 60


# Utilities
def get_image_from_cap(cap):
    _, cv_img = cap.read()
    cv_img = cv.cvtColor(cv_img, cv.COLOR_BGR2RGB)
    pil_img = Image.fromarray(cv_img)
    return pil_img


def draw_mask_on_image(img, mask_coordinate):
    draw = ImageDraw.Draw(img)
    draw.polygon(mask_coordinate, outline="red", fill="red")


def build_mask_from_coordinate(height, width, mask_coordinate):
    mask_contour = np.array(mask_coordinate)
    mask = np.full([height, width], 255, dtype=np.uint8)
    cv.fillPoly(mask, pts=[mask_contour], color=(0))
    return mask


def get_frames(cap, start_frame, end_frame):
    cap.set(cv.CAP_PROP_POS_FRAMES, float(start_frame))
    frames = [cap.read()[1] for _ in range(end_frame - start_frame)]
    return frames


def precomp_ref(frames):
    ref_image_precomputed = []
    ref = cv.cvtColor(frames[0], cv.COLOR_BGR2GRAY)
    for f in frames[1:]:
        current = cv.cvtColor(f, cv.COLOR_BGR2GRAY)
        ref_image_np = np.array(ref)
        current_np = np.array(current)
        np.maximum(ref_image_np, current_np, out=ref_image_np)
        ref_image = Image.fromarray(ref_image_np)
        ref_image_precomputed.append(ref_image)
    return ref_image_precomputed

class VideoPlayer:
    def __init__(
        self, video_data, tkinter_frame1, tkinter_frame2, tkinter_slider,label_slider_frame1
    ) -> None:
        self.video_data = video_data
        self.current_frame = 0
        self.tkinter_frame1 = tkinter_frame1
        self.tkinter_frame2 = tkinter_frame2
        self.tkinter_slider = tkinter_slider
        self.tkinter_label_frame1 = label_slider_frame1
        self.cap = cv.VideoCapture(video_data.file_name)
        self.playing = True
        self.mode = "binary"  # or "heatmap"
        self.current_processed_image = None

    def get_heat_map(self, start_frame, end_frame):
        cues = [
            self.calc_binary(self.cap, frame_i)[1]
            for frame_i in range(start_frame, end_frame)
        ]
        cues_sum = np.sum(np.array(cues), axis=0)  # sum

        # normalize
        min_value = np.min(cues_sum)
        max_value = np.max(cues_sum)
        normalized_array = (cues_sum - min_value) / (max_value - min_value) * 255
        normalized_array = normalized_array.astype(np.uint8)

        colormap = cm.get_cmap("viridis")  # You can use 'jet', 'plasma', etc.
        colored_array = colormap(
            normalized_array / 255.0
        )  # Normalize array to 0-1 for colormap

        # Matplotlib returns an RGBA image, convert to RGB
        colored_array_rgb = (colored_array[:, :, :3] * 255).astype(np.uint8)

        # Create the PIL image from the RGB array
        image = Image.fromarray(colored_array_rgb, "RGB")

        return image

    def calc_binary(self, cap, frame_i):
        height = self.video_data.height
        width = self.video_data.width
        mask = build_mask_from_coordinate(
            height, width, self.video_data.mask_coordinate
        )
        ref_image = self.video_data.ref_precomp[frame_i - 1]
        ret, current_col = cap.read()
        current = cv.cvtColor(current_col, cv.COLOR_BGR2GRAY)

        cue = cv.absdiff(current, np.array(ref_image))
        cue = cv.bitwise_and(cue, mask)
        ret, cue = cv.threshold(cue, 0, 200, cv.THRESH_TRIANGLE)
        # ret, cue_bin= cv.threshold(cue,threshold_value,250,cv.THRESH_BINARY)
        return Image.fromarray(cue).convert("RGB"), cue

    def show_frame(self, frame_i, set_slider=True):
        if set_slider:
            self.tkinter_slider.set(frame_i)
        self.cap.set(cv.CAP_PROP_POS_FRAMES, float(frame_i))
        pil_img = get_image_from_cap(self.cap)

        draw_mask_on_image(pil_img, self.video_data.mask_coordinate)

        frame_image = customtkinter.CTkImage(
            light_image=pil_img,
            dark_image=pil_img,
            size=(int(640 * 0.75), int(480 * 0.75)),
        )
        self.tkinter_frame1.configure(image=frame_image)
        self.tkinter_frame1.update()

        pil_bin_img, cue_bin = self.calc_binary(self.cap, frame_i)
        # buffer cue_bin to video_data
        if self.mode == "heatmap":
            window_size = min(frame_i-1, 20)
            pil_bin_img = self.get_heat_map(frame_i - window_size, frame_i)

        self.current_processed_image = pil_bin_img
        bin_image = customtkinter.CTkImage(
            light_image=pil_bin_img,
            dark_image=pil_bin_img,
            size=(int(640 * 0.75), int(480 * 0.75)),
        )
        self.tkinter_frame2.configure(image=bin_image)
        self.tkinter_frame2.update()
        self.tkinter_label_frame1.configure(text="Frame:"+str(frame_i)) 

    def set_frame_to(self, frame_i, set_slider=True):
        self.show_frame(frame_i, set_slider)
        if set_slider:
            self.current_frame = frame_i
        else:
            self.current_frame = int(self.tkinter_slider.get())
        
    def play(self):
        self.playing = True
        self.tkinter_slider
        start_frame = int(self.tkinter_slider.get())
        print("play clicked")
        for frame_i in range(start_frame, self.video_data.end_frame):
            # time.sleep(1/30)
            # print(f"showing frame {frame_i}")
            self.show_frame(frame_i)
            self.current_frame += 1
            if self.playing == False:
                break

    def pause(self, frame_i=None):
        self.playing = False
        if frame_i:
            self.show_frame(int(frame_i))
        else:
            self.show_frame(self.current_frame)

    def stop(self):
        self.playing = False
        self.show_frame(self.video_data.start_frame)
        self.current_frame = self.video_data.start_frame


@dataclass
class VideoData:
    file_name: str
    width: int
    height: int
    fps: int
    frame_length: int
    ref_image: Image
    start_frame: int
    end_frame: int
    ref_precomp: list
    mask_coordinate: list = None


class OpenFileModel:
    def __init__(self) -> None:
        self.file_name = None

    def set_file_name(self, file_name):
        self.file_name = file_name

    def load_video(self):
        cap = cv.VideoCapture(self.file_name)
        width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv.CAP_PROP_FPS)
        frame_length = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
        startframe = int(1)
        cap.set(cv.CAP_PROP_POS_FRAMES, float(startframe))
        pil_img = get_image_from_cap(cap)
        lastframe = int(frame_length)

        frames = get_frames(cap, startframe, lastframe)
        ref_precomp = precomp_ref(frames)

        video_data = VideoData(
            file_name=self.file_name,
            width=width,
            height=height,
            fps=fps,
            frame_length=frame_length,
            ref_image=pil_img.convert("L"),
            start_frame=startframe,
            end_frame=lastframe,
            ref_precomp=ref_precomp,
        )
        return video_data


class MainWindowModel:
    def __init__(self) -> None:
        self.video_data = None
        self.video_player = None

    def set_video_data(self, video_data):
        self.video_data = video_data

    def instantiate_video_player(self, tkinter_frame1, tkinter_frame2, tkinter_slider, label_slider_frame1):
        self.video_player = VideoPlayer(
            self.video_data, tkinter_frame1, tkinter_frame2, tkinter_slider, label_slider_frame1
        )


class MaskingModel:
    def __init__(self) -> None:
        self.mask_coordinate = []

    def add_mask_coordinate(self, coordinate):
        self.mask_coordinate.append(coordinate)
        if len(self.mask_coordinate) == 2:
            self.mask_coordinate.append(coordinate)

    def pop_mask_coordinate(self):
        if len(self.mask_coordinate) != 0:
            self.mask_coordinate.pop()
        print(self.mask_coordinate)

    def clear_mask_coordinate(self):
        self.mask_coordinate.clear()
        print(self.mask_coordinate)

    def get_mask_coordinate(self):
        return list(chain(self.mask_coordinate))


class ResultModel:
    pass

from itertools import chain
import numpy as np
import cv2 as cv
from PIL import Image, ImageDraw
from dataclasses import dataclass
import customtkinter
from matplotlib import cm
from datetime import datetime
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
    ref = np.array(ref)
    for f in frames[1:]:
        current = cv.cvtColor(f, cv.COLOR_BGR2GRAY)
        ref_image_np = ref.copy()
        current_np = np.array(current)
        np.maximum(ref_image_np, current_np, out=ref_image_np)
        ref_image_precomputed.append(ref_image_np)
    return ref_image_precomputed


class VideoPlayer:
    def __init__(
        self,
        video_data,
        tkinter_frame1,
        tkinter_frame2,
        tkinter_slider,
        label_slider_frame1,
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
        self.thresholding_method = "triangle"  # or "binary"
        self.binary_thresholding_param = 15
        self.current_processed_image = None
        self.mask = build_mask_from_coordinate(
            self.video_data.height,
            self.video_data.width,
            self.video_data.mask_coordinate,
        )

    def get_heat_map(self, start_frame, end_frame):
        cues = [
            self.calc_binary(self.cap, frame_i)[1]
            for frame_i in range(start_frame, end_frame)
        ]
        cues_sum = np.sum(cues, axis=0)  # sum

        # normalize
        min_value = np.min(cues_sum)
        max_value = np.max(cues_sum)
        normalized_array = (cues_sum - min_value) / (max_value - min_value) * 255
        normalized_array = normalized_array.astype(np.uint8)

        colormap = cm.get_cmap("nipy_spectral")  # You can use 'jet', 'plasma', etc.
        colored_array = colormap(
            normalized_array / 255.0
        )  # Normalize array to 0-1 for colormap

        # Matplotlib returns an RGBA image, convert to RGB
        colored_array_rgb = (colored_array[:, :, :3] * 255).astype(np.uint8)

        # Create the PIL image from the RGB array
        image = Image.fromarray(colored_array_rgb, "RGB")

        return image

    def on_the_fly_ref(self, frame_i, window_size=5):
        start_frame_i = max(0, frame_i - window_size)
        ref = cv.cvtColor(self.video_data.frames[start_frame_i], cv.COLOR_BGR2GRAY)
        ref = np.array(ref)
        for f in self.video_data.frames[start_frame_i:frame_i]:
            current = cv.cvtColor(f, cv.COLOR_BGR2GRAY)
            ref_image_np = ref.copy()
            current_np = np.array(current)
            np.maximum(ref_image_np, current_np, out=ref_image_np)

        return ref_image_np

    def calc_binary(self, cap, frame_i, return_img=True):
        if self.video_data.ref_precomp:
            ref_image = self.video_data.ref_precomp[frame_i - 1]
        else:
            ref_image = self.on_the_fly_ref(frame_i)

        ret, current_col = cap.read()
        current = cv.cvtColor(current_col, cv.COLOR_BGR2GRAY)
        cue = cv.absdiff(current, ref_image)

        cue = cv.bitwise_and(cue, self.mask)
        if self.thresholding_method == "triangle":
            ret, cue = cv.threshold(cue, 0, 200, cv.THRESH_TRIANGLE)
        elif self.thresholding_method == "binary":
            ret, cue = cv.threshold(
                cue, self.binary_thresholding_param, 250, cv.THRESH_BINARY
            )

        if return_img:
            # make it faster by skipping this if not needed
            img = Image.fromarray(cue).convert("RGB")
        else:
            img = None
        return img, cue

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
            window_size = min(frame_i - 1, 20)
            pil_bin_img = self.get_heat_map(frame_i - window_size, frame_i)

        self.current_processed_image = pil_bin_img
        bin_image = customtkinter.CTkImage(
            light_image=pil_bin_img,
            dark_image=pil_bin_img,
            size=(int(640 * 0.75), int(480 * 0.75)),
        )
        self.tkinter_frame2.configure(image=bin_image)
        self.tkinter_frame2.update()
        self.tkinter_label_frame1.configure(text="Frame:" + str(frame_i))

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
    ref_precomp: list = None
    mask_coordinate: list = None
    frames: list = None


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

        # DISABLE ref precomp TODO: CLEANING
        ref_precomp = None  # precomp_ref(frames)

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
            frames=frames,
        )
        return video_data


class MainWindowModel:
    def __init__(self) -> None:
        self.video_data = None
        self.video_player = None

    def set_video_data(self, video_data):
        self.video_data = video_data

    def instantiate_video_player(
        self, tkinter_frame1, tkinter_frame2, tkinter_slider, label_slider_frame1
    ):
        self.video_player = VideoPlayer(
            self.video_data,
            tkinter_frame1,
            tkinter_frame2,
            tkinter_slider,
            label_slider_frame1,
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

    def clear_mask_coordinate(self):
        self.mask_coordinate.clear()

    def get_mask_coordinate(self):
        return list(chain(self.mask_coordinate))


class ResultProcessModel:
    def __init__(self) -> None:
        self.fps = 60

    def calculate_count(self, video_player, start_frame, end_frame):
        print("calculate model")
        print(f"start {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        start_frame = int(start_frame)
        end_frame = int(end_frame)
        count_per_second = []
        tempcount = np.zeros(self.fps, dtype=np.uint)

        for i in range(end_frame - start_frame - 1):
            frame_i = start_frame + i
            video_player.cap.set(cv.CAP_PROP_POS_FRAMES, float(frame_i))
            _, cue = video_player.calc_binary(
                video_player.cap, frame_i, return_img=False
            )
            contours, hierarchy = cv.findContours(
                cue, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE
            )
            tempcount[frame_i % self.fps] = len(contours)

            if frame_i % self.fps == 0:
                count_per_second.append(np.average(tempcount))

        print(f"end {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        plt.plot(count_per_second)
        plt.xlabel("time")
        plt.ylabel("count")
        plt.show()

        return count_per_second


class ResultModel:
    pass

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

import matplotlib.pyplot as plt

COEF_FADE_IN  = 1.00
COEF_FADE_OUT = 0.90
HEATMAP_CEIL= COEF_FADE_IN * 60 

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
    mask_contour= np.array(mask_coordinate)
    mask = np.full([height, width], 255, dtype=np.uint8)
    cv.fillPoly(mask, pts=[mask_contour], color=(0))
    return mask
    
class VideoPlayer():

    def __init__(self, video_data, tkinter_frame1, tkinter_frame2, tkinter_slider) -> None:
        self.video_data = video_data
        self.current_frame = 0
        self.tkinter_frame1 = tkinter_frame1
        self.tkinter_frame2 = tkinter_frame2
        self.tkinter_slider = tkinter_slider
        self.cap = cv.VideoCapture(video_data.file_name)
        self.playing = True

    def get_heat_map(self, cue_raw):
        height = self.video_data.height
        width = self.video_data.width
        heatmap = np.zeros([height, width], dtype=np.single)
        heatmap_cue = np.full([height, width], 255, dtype=np.uint8)

        heatmap= heatmap + (COEF_FADE_IN * cue_raw/250)
        heatmap= heatmap - COEF_FADE_OUT
        heatmap= np.clip(heatmap, 0, None)
        heatmapf = np.clip(heatmap, 0, HEATMAP_CEIL) # saturated heatmap, only for display    
        heatmapf.itemset((0,0), HEATMAP_CEIL)
        cv.normalize(heatmapf, heatmap_cue, 0, 255, cv.NORM_MINMAX, cv.CV_8UC1)
        heatmap_render = cv.applyColorMap(heatmap_cue, cmapy.cmap('nipy_spectral'))

        return Image.fromarray(heatmap_render)

    def calc_binary(self, cap):

        threshold_value = 40
        height = self.video_data.height
        width = self.video_data.width
        mask = build_mask_from_coordinate(height,width, 
                        self.video_data.mask_coordinate)

        ret, current_col = cap.read()
        current= cv.cvtColor(current_col, cv.COLOR_BGR2GRAY) 
        
        # updating the reference/background image
        for y in range(height):
            for x in range(width):
                #self.video_data.ref_image.getpixel((x,y))
                if current.item(y,x) > self.video_data.ref_image.getpixel((x,y)):
                    self.video_data.ref_image.putpixel((x,y), current.item(y,x))

        cue = cv.absdiff(current, np.array(self.video_data.ref_image))
        cue = cv.bitwise_and(cue, mask)
        ret, cue = cv.threshold(cue, 0, 200, cv.THRESH_TRIANGLE)
        #ret, cue_bin= cv.threshold(cue,threshold_value,250,cv.THRESH_BINARY)
        return Image.fromarray(cue).convert('RGB'), cue
        
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

        pil_bin_img, cue_bin = self.calc_binary(self.cap)

        #pil_bin_img = self.get_heat_map(cue_bin)

        bin_image = customtkinter.CTkImage(
            light_image=pil_bin_img,
            dark_image=pil_bin_img,
            size=(int(640 * 0.75), int(480 * 0.75)),
        )
        self.tkinter_frame2.configure(image=bin_image)
        self.tkinter_frame2.update()
        

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
            time.sleep(1/30)
            print(f"showing frame {frame_i}")
            self.show_frame(frame_i)
            self.current_frame +=1
            if self.playing == False:
                break
 
    def pause(self, frame_i=None):
        self.playing=False
        if frame_i:
            self.show_frame(int(frame_i))
        else:
            self.show_frame(self.current_frame)

    def stop(self):
        self.playing=False
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

        video_data = VideoData(
            file_name=self.file_name,
            width=width,
            height=height,
            fps=fps,
            frame_length=frame_length,
            ref_image=pil_img.convert("L"),
            start_frame=startframe,
            end_frame=lastframe,
        )
        return video_data


class MainWindowModel:

    def __init__(self) -> None:
        self.video_data = None
        self.video_player = None
    
    def set_video_data(self, video_data):
        self.video_data = video_data

    def instantiate_video_player(self, tkinter_frame1, tkinter_frame2, tkinter_slider):
        self.video_player = VideoPlayer(self.video_data, tkinter_frame1, tkinter_frame2, tkinter_slider)


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

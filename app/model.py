from itertools import chain
import numpy as np
import cv2 as cv
import sys
import cmapy
import ffmpegcv
from PIL import Image
from dataclasses import dataclass
import customtkinter


# Utilities
def get_image_from_cap(cap):
    _, cv_img = cap.read()
    cv_img = cv.cvtColor(cv_img, cv.COLOR_BGR2RGB)
    pil_img = Image.fromarray(cv_img)
    return pil_img


class VideoPlayer():

    def __init__(self, video_data, tkinter_label) -> None:
        self.video_data = video_data
        self.current_frame = 0
        self.tkinter_label = tkinter_label
        self.cap = cv.VideoCapture(video_data.file_name)
        self.playing = True

    def show_frame(self, frame_i):
        self.cap.set(cv.CAP_PROP_POS_FRAMES, float(frame_i))
        pil_img = get_image_from_cap(self.cap)
        frame_image = customtkinter.CTkImage(
            light_image=pil_img,
            dark_image=pil_img,
            size=(int(640 * 0.75), int(480 * 0.75)),
        )
        self.tkinter_label.configure(image=frame_image)
        self.tkinter_label.update()

    def play(self):
        self.playing = True
        start_frame = self.current_frame
        print("play clicked")
        for frame_i in range(start_frame, self.video_data.end_frame):
            print(f"showing frame {frame_i}")
            self.show_frame(frame_i)
            self.current_frame +=1
            if self.playing == False:
                break
 
    def pause(self):
        self.playing=False
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
    first_frame_img: Image
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
            first_frame_img=pil_img,
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

    def instantiate_video_player(self, tkinter_label):
        self.video_player = VideoPlayer(self.video_data, tkinter_label)



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

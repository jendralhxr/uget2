import numpy as np
import cv2 as cv
from typing import Tuple


def substract_background(
    file_name: str, start_frame: int, end_frame: int, output_path: str = None
) -> Tuple[np.array, np.array]:
    """
    Subtract background from a video file.

    :param file_name: path to the input video file.
    :param start_frame: frame number to start background subtraction.
    :param end_frame: frame number to end background subtraction.
    :param output_path: optional path to save the output image file.

    :return: A tuple containing the background subtracted grayscale image and colored image.
    """
    framenum = 0
    cap = cv.VideoCapture(file_name)
    frame_length = int(cap.get(cv.CAP_PROP_FRAME_COUNT))

    cap.set(cv.CAP_PROP_POS_FRAMES, float(start_frame))
    framenum = start_frame

    while (framenum < end_frame) and (framenum < frame_length - 1):
        _, current_col = cap.read()
        current_gray = cv.cvtColor(current_col, cv.COLOR_BGR2GRAY)
        if framenum == start_frame:
            bg_col = current_col
            bg_gray = current_gray

        framenum += 1

        mask = current_gray > bg_gray
        bg_gray = np.where(mask, current_gray, bg_gray)
        bg_col = np.where(np.dstack([mask] * 3), current_col, bg_col)

    if output_path:
        cv.imwrite(output_path, bg_col)
    cap.release

    return bg_gray, bg_col

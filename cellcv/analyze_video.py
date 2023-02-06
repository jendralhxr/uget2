from typing import Tuple

import cv2
import numpy as np


class VideoAnalyzer:
    """
    The VideoAnalyzer class for analyzing video data in cell counting tasks
    """

    def __init__(self, file_name: str) -> None:
        """
        :param file_name: a string path to the video file
        """

        self.file_name = file_name
        self.alpha = 1.2  # Contrast control (1.0-3.0) bukan control tanpa r
        self.beta = 0  # Brightness control (0-100)
        self.aggre = 5
        self.density_minimum = 10000000

    def load_video(self, file_name: str) -> cv2.VideoCapture:
        """
        Load video from the given file name and set video properties.

        :param file_name: Name of the video file.
        :return: OpenCV video capture object.
        :raises: Prints "Error opening the video file" if the video file can't be opened.
        """
        cap = cv2.VideoCapture(file_name)
        if cap.isOpened() == False:
            print("Error opening the video file")
        self.video_width = int(cap.get(3))
        self.video_height = int(cap.get(4))
        self.fps = int(cap.get(cv2.CAP_PROP_FPS))
        self.n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        return cap

    def _calc_blob(self, frame_sum: np.ndarray) -> Tuple[int, int, int, int]:
        """
        Calculate the blob position in the given frame_sum.

        :param frame_sum: Sum of aggregated frames.
        :return: A tuple of total x, total y, total mass, and blob count.
        """
        # calculate blob position here
        contours, hierarchy = cv2.findContours(
            frame_sum, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE
        )
        total_x = 0
        total_y = 0
        total_m = 0
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            m = w * h
            total_x += x * m
            total_y += y * m
            total_m += m

        blob_count = len(contours)

        return total_x, total_y, total_m, blob_count

    def _calc_density(
        self, total_x: int, total_y: int, total_m: int, frame_sum: np.ndarray
    ) -> Tuple[int, int, int, float]:
        """
        Calculate the density of objects in the video frame.

        :param total_x: Total x-coordinate of objects.
        :param total_y: Total y-coordinate of objects.
        :param total_m: Total mass of objects.
        :param frame_sum: Sum of aggregated frames.

        :return: center_x, center_y, total_m, density
        """
        # hitung kepadatan
        r = np.sqrt(total_m)
        center_x = total_x / total_m
        center_y = total_y / total_m
        density = 0

        x_start = int(center_x - r / 2)
        if x_start < 0:
            x_start = 0
        x_stop = int(center_x + r / 2)
        if x_stop > self.video_width:
            x_stop = self.video_width
        y_start = int(center_y - r / 2)
        if y_start < 0:
            y_start = 0
        y_stop = int(center_y + r / 2)
        if y_stop > self.video_height:
            y_stop = self.video_height

        for i in range(x_start, x_stop - 1, 1):
            for j in range(y_start, y_stop - 1, 1):
                if frame_sum[j, i]:
                    density += 1

        if self.density_minimum > total_m:
            self.density_minimum = total_m

        return center_x, center_y, total_m, total_m / self.density_minimum

    def analyse(self, start_frame: int, end_frame: int, show_video: bool = False):
        """
        Analyse the video and print the outputs

        :param start_frame: the starting frame to analyze
        :param end_frame: the end frame to analyze
        """
        self.start_frame = start_frame
        self.end_frame = end_frame

        cap = self.load_video(self.file_name)
        cap.set(cv2.CAP_PROP_POS_FRAMES, float(start_frame))

        fgbg = cv2.createBackgroundSubtractorMOG2(50, 10, bool(0))
        frameb = []
        for frame_n in range(start_frame, end_frame):
            ret, frame = cap.read()
            invr = cv2.bitwise_not(frame)

            # init the frames
            adjusted = cv2.convertScaleAbs(invr, alpha=self.alpha, beta=self.beta)
            framen = fgbg.apply(adjusted)
            if frame_n - 1 < start_frame:
                for i in range(0, self.aggre):
                    frameb.append(framen)

            for i in range(0, self.aggre - 1):
                frameb[i] = frameb[i + 1]
            frameb[self.aggre - 1] = framen

            frame_sum = 0
            for i in range(0, self.aggre):
                frame_sum += frameb[i]

            total_x, total_y, total_m, blob_count = self._calc_blob(frame_sum)

            if frame_n - start_frame > self.aggre:
                center_x, center_y, total_m, ratio = self._calc_density(
                    total_x, total_y, total_m, frame_sum
                )
                time = (frame_n - start_frame) / self.fps
                print(
                    "time:{:0.2f}\tcount:{}\tpoint:({:0.2f},{:0.2f})\tdensity={:0.0f}\tratio={:0.3f}".format(
                        time, blob_count, center_x, center_y, total_m, ratio
                    )
                )

            if show_video:
                cv2.imshow("frame", frame)
                cv2.imshow("deteksi", frame_sum)
                k = cv2.waitKey(1) & 0xFF
                if k == 27:
                    break

        cap.release()
        cv2.destroyAllWindows()

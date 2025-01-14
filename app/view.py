import customtkinter
from customtkinter import CTkOptionMenu
from PIL import Image, ImageTk
import sys
import os

DEFAULT_BINARY_THRESHOLD = 15


class MainWindowView:
    def __init__(self):
        super().__init__()
        self._show_gui("COMOT ver 0.1")

    def set_title(self, title):
        self.window.title(title)

    def _show_gui(self, title):
        self.window = customtkinter.CTk()
        self.window.title(title)
        self.window.geometry("1024x640")
        self.window.minsize(1024, 640)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        frame = customtkinter.CTkFrame(self.window)
        frame.place(relx=0.5, rely=0.5, anchor="c")

        self.image1 = customtkinter.CTkImage(
            light_image=Image.open("assets/comot_loading.png"),
            dark_image=Image.open("assets/comot_loading.png"),
            size=(int(640 * 0.75), int(480 * 0.75)),
        )

        self.color_bar = Image.open("assets/colorbar.png")
        ###############################################################################
        # Frame 1 widgets definition (Annotated Video)
        ###############################################################################
        self.window.video_frame1 = customtkinter.CTkLabel(
            frame, image=self.image1, text=""
        )  # display image with a CTkLabel
        self.window.video_frame1.grid(
            row=0, columnspan=5, padx=10, pady=10, sticky="ew"
        )

        self.window.label_slider_frame1 = customtkinter.CTkLabel(
            frame, text="Frame", anchor="w"
        )
        self.window.label_slider_frame1.grid(
            row=1, column=0, columnspan=2, padx=5, pady=(10, 0), sticky="ews"
        )

        self.window.slider_frame1 = customtkinter.CTkSlider(
            frame, from_=0, to=100, number_of_steps=100
        )
        self.window.slider_frame1.grid(
            row=2, column=0, columnspan=5, padx=10, pady=(0, 10), sticky="ewn"
        )

        self.window.button_frame1_min5s = customtkinter.CTkButton(
            frame, width=50, text="-5s"
        )
        self.window.button_frame1_min5s.grid(
            row=4, column=0, padx=10, pady=10, sticky="ew"
        )

        self.window.button_frame1_play = customtkinter.CTkButton(
            frame, width=80, text="Play"
        )
        self.window.button_frame1_play.grid(
            row=4, column=1, padx=5, pady=10, sticky="ew"
        )

        self.window.button_frame1_pause = customtkinter.CTkButton(
            frame, width=80, text="Pause"
        )
        self.window.button_frame1_pause.grid(
            row=4, column=2, padx=5, pady=10, sticky="ew"
        )

        self.window.button_frame1_stop = customtkinter.CTkButton(
            frame, width=80, text="Stop"
        )
        self.window.button_frame1_stop.grid(
            row=4, column=3, padx=5, pady=10, sticky="ew"
        )

        self.window.button_frame1_add5s = customtkinter.CTkButton(
            frame, width=50, text="+5s"
        )
        self.window.button_frame1_add5s.grid(
            row=4, column=4, padx=10, pady=10, sticky="ew"
        )

        ###############################################################################
        # Frame 2 widgets definition (Binary and Heatmap Video)
        ###############################################################################
        self.window.video_frame2 = customtkinter.CTkLabel(
            frame, image=self.image1, text=""
        )  # display image with a CTkLabel
        self.window.video_frame2.grid(
            row=0, column=6, columnspan=5, padx=10, pady=10, sticky="ew"
        )

        self.window.label_slider_frame2 = customtkinter.CTkLabel(
            frame, text=f"Threshold (Binary): {DEFAULT_BINARY_THRESHOLD}", anchor="w"
        )
        self.window.label_slider_frame2.grid(row=1, column=6, sticky="w")
        self.window.slider_frame2 = customtkinter.CTkSlider(
            frame, from_=0, to=50, number_of_steps=50
        )
        self.window.slider_frame2.set(DEFAULT_BINARY_THRESHOLD)
        self.window.slider_frame2.grid(
            row=2, column=6, columnspan=5, padx=10, pady=(0, 10), sticky="ewn"
        )

        self.window.label_thresholding_method = customtkinter.CTkLabel(
            frame, text="Method:", anchor="w"
        )
        self.window.label_thresholding_method.grid(row=3, column=6, sticky="w")
        self.window.option_menu_frame2_thresholding_method = CTkOptionMenu(
            frame, values=["Triangle", "Binary  "], width=100, height=30, anchor="w"
        )
        self.window.option_menu_frame2_thresholding_method.configure(width=80)

        self.window.option_menu_frame2_thresholding_method.grid(
            row=4, column=6, columnspan=2, padx=10, pady=10, sticky="ew"
        )

        self.window.label_display_method = customtkinter.CTkLabel(
            frame, text="Display:", anchor="w"
        )
        self.window.label_display_method.grid(row=3, column=8, sticky="w")
        self.window.button_frame2_switcher = customtkinter.CTkButton(
            frame, width=80, text="Detection"
        )
        self.window.button_frame2_switcher.grid(
            row=4, column=8, padx=10, pady=10, sticky="ew"
        )

        self.window.button_frame2_snapshot = customtkinter.CTkButton(
            frame, width=80, text="Snapshot"
        )
        self.window.button_frame2_snapshot.grid(
            row=4, column=9, padx=10, pady=10, sticky="ew"
        )

        self.window.button_result = customtkinter.CTkButton(
            frame, width=80, text="Results"
        )
        self.window.button_result.grid(row=4, column=10, padx=10, pady=10, sticky="ew")

    def on_closing(self):
        # Add your custom function here
        print("System exit")
        self.window.destroy()
        sys.exit()

    def run(self):
        self.window.mainloop()


class OpenFileView:
    def __init__(self):
        self.title = "Open video file"

    def _build_gui(self, parent):
        self.window = customtkinter.CTkToplevel(parent)
        self.window.title(self.title)
        self.window.geometry("450x180")
        self.window.minsize(450, 180)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)

        self.window.label = customtkinter.CTkLabel(
            self.window,
            text="Welcome to Cell Counting and Motility Observation Tool ver 0.1",
        )
        self.window.label.grid(row=0, columnspan=3, padx=10, pady=10, sticky="ew")
        self.window.button_load_video = customtkinter.CTkButton(
            self.window, width=80, text="Load Video"
        )
        self.window.button_load_video.grid(
            row=1, column=1, padx=10, pady=10, sticky="ew"
        )

    def on_closing(self):
        # Add your custom function here
        print("System exit")
        self.window.destroy()
        sys.exit()

    def run(self, parent):
        self._build_gui(parent)
        self.window.deiconify()


class MaskingView:
    def __init__(self):
        super().__init__()
        self.title = "Masking - COMOT ver 0.1"

    def _build_gui(self, parent):
        self.window = customtkinter.CTkToplevel(parent)
        self.window.title(self.title)
        self.window.geometry("1024x640")
        self.window.minsize(1024, 640)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        frame = customtkinter.CTkFrame(self.window)
        frame.place(relx=0.5, rely=0.5, anchor="c")

        img = ImageTk.PhotoImage(self.start_frame_img)
        self.window.masking_canvas = customtkinter.CTkCanvas(
            frame, width=int(640), height=int(480)
        )
        self.window.masking_canvas.image = img
        self.window.masking_canvas.create_image(0, 0, anchor="nw", image=img)
        self.window.masking_canvas.grid(
            row=0, columnspan=10, padx=10, pady=10, sticky="ew"
        )

        self.window.button_undo_masking = customtkinter.CTkButton(
            frame, width=80, text="undo"
        )
        self.window.button_undo_masking.grid(
            row=1, column=7, padx=10, pady=10, sticky="ew"
        )

        self.window.button_clear_masking = customtkinter.CTkButton(
            frame, width=80, text="clear"
        )
        self.window.button_clear_masking.grid(
            row=1, column=8, padx=10, pady=10, sticky="ew"
        )

        self.window.button_masking = customtkinter.CTkButton(
            frame, width=80, text="masking"
        )
        self.window.button_masking.grid(row=1, column=9, padx=10, pady=10, sticky="ew")

    def set_start_frame_image(self, img):
        self.start_frame_img = img

    def on_closing(self):
        # Add your custom function here
        print("System exit")
        self.window.destroy()
        sys.exit()

    def run(self, parent):
        self._build_gui(parent)
        self.window.deiconify()


class ResultProcessView:
    def __init__(self):
        self.title = "Result process"

    def _build_gui(self, parent):
        self.window = customtkinter.CTkToplevel(parent)
        self.window.title(self.title)
        self.window.geometry("400x300")
        self.window.minsize(400, 300)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        frame = customtkinter.CTkFrame(self.window)
        frame.place(relx=0.5, rely=0.5, anchor="c")
        # Create label and entry for "start"
        self.window.label_start = customtkinter.CTkLabel(frame, text="Start (second)")
        self.window.label_start.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        self.window.entry_start = customtkinter.CTkEntry(frame, width=100)
        self.window.entry_start.grid(
            row=1, column=0, padx=10, pady=(0, 10), sticky="ew"
        )

        # Create label and entry for "end"
        self.window.label_end = customtkinter.CTkLabel(frame, text="End (second)")
        self.window.label_end.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")

        self.window.entry_end = customtkinter.CTkEntry(frame, width=100)
        self.window.entry_end.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ew")

        self.window.button_process = customtkinter.CTkButton(
            frame, width=80, text="process"
        )
        self.window.button_process.grid(row=2, column=5, padx=10, pady=10, sticky="ew")

    def on_closing(self):
        # Add your custom function here
        print("System exit")
        self.window.destroy()
        sys.exit()

    def run(self, parent):
        self._build_gui(parent)
        self.window.deiconify()


class ProcessingView:
    def __init__(self):
        self.title = "Processing"

    def _build_gui(self, parent):
        self.window = customtkinter.CTkToplevel(parent)
        self.window.title(self.title)
        self.window.geometry("400x300")
        self.window.minsize(400, 300)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        frame = customtkinter.CTkFrame(self.window)
        frame.place(relx=0.5, rely=0.5, anchor="c")

        self.window.label = customtkinter.CTkLabel(frame, text=" ⌛ Processing... ⌛")
        self.window.label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    def on_closing(self):
        # Add your custom function here
        print("System exit")
        self.window.destroy()
        os._exit(1) # may break os-compatibility
        sys.exit()

    def run(self, parent):
        self._build_gui(parent)
        self.window.deiconify()


class ResultView:
    def __init__(self):
        self.title = "Result View"

    def _build_gui(self, parent):
        self.window = customtkinter.CTkToplevel(parent)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.window.title(self.title)
        self.window.geometry("800x600")
        self.window.minsize(800, 600)

        frame = customtkinter.CTkFrame(self.window)
        frame.place(relx=0.5, rely=0.5, anchor="c")

        self.window.image_frame = customtkinter.CTkLabel(frame, text="")
        self.window.image_frame.grid(
            row=0, column=0, columnspan=10, padx=10, pady=10, sticky="ew"
        )

        self.window.button_save_csv = customtkinter.CTkButton(
            frame, width=80, text="Save CSV"
        )
        self.window.button_save_csv.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

        self.window.button_save_image = customtkinter.CTkButton(
            frame, width=80, text="Save Image"
        )
        self.window.button_save_image.grid(
            row=5, column=1, padx=10, pady=10, sticky="ew"
        )

    def set_image(self, img):
        self.window.image_frame.configure(image=img)
        self.window.image_frame.image = img

    def on_closing(self):
        # Add your custom function here
        print("System exit")
        self.window.destroy()
        sys.exit()

    def run(self, parent):
        self._build_gui(parent)
        self.window.deiconify()

import customtkinter
from customtkinter import filedialog
from PIL import Image


class OpenFileView(customtkinter.CTkToplevel):
    def __init__(self, master, config):
        super().__init__(master)
        self.master = master
        self.config = config
        self.callbacks = {}
        self._showGUI("Open video file")

    def _showGUI(self, title):
        self.title(title)
        self.geometry("400x180")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(
            self, text="Welcome to Uget-Uget Counting ver 0.1"
        )
        self.label.grid(row=0, columnspan=3, padx=10, pady=10, sticky="ew")
        self.button = customtkinter.CTkButton(
            self, width=80, text="Load Video", command=self.button_callback
        )
        self.button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    def button_callback(self):
        self.master.deiconify()
        pass


class MainWindowView:
    def __init__(self):
        super().__init__()
        self.callbacks = {}
        # self._init_assets()
        self._show_gui("Uget-Uget Counting ver 0.1")
        # self.open_video()

        # self.run() #this should be called in controler

    def _show_gui(self, title):
        self.window = customtkinter.CTk()
        self.window.title(title)
        self.window.geometry("1024x640")

        frame = customtkinter.CTkFrame(self.window)
        frame.place(relx=0.5, rely=0.5, anchor="c")

        self.image1 = customtkinter.CTkImage(
            light_image=Image.open("4879.png"),
            dark_image=Image.open("4879.png"),
            size=(int(640 * 0.75), int(480 * 0.75)),
        )

        ###############################################################################
        # Frame 1 widgets definition (Annotated Video)
        ###############################################################################
        self.window.video_frame1 = customtkinter.CTkLabel(
            frame, image=self.image1, text=""
        )  # display image with a CTkLabel
        self.window.video_frame1.grid(
            row=0, columnspan=5, padx=10, pady=10, sticky="ew"
        )

        self.window.label_slider_frame1 = customtkinter.CTkLabel(frame, text="Frame")
        self.window.label_slider_frame1.grid(
            row=1, column=0, padx=5, pady=(10, 0), sticky="ews"
        )

        self.window.slider_frame1 = customtkinter.CTkSlider(
            frame, from_=0, to=100, number_of_steps=100
        )
        self.window.slider_frame1.grid(
            row=2, column=0, columnspan=5, padx=10, pady=(0, 10), sticky="ewn"
        )

        self.window.button_frame1_add5s = customtkinter.CTkButton(
            frame, width=50, text="-5s"
        )
        self.window.button_frame1_add5s.grid(
            row=3, column=0, padx=10, pady=10, sticky="ew"
        )

        self.window.button_frame1_play = customtkinter.CTkButton(
            frame, width=80, text="Play"
        )
        self.window.button_frame1_play.grid(
            row=3, column=1, padx=5, pady=10, sticky="ew"
        )

        self.window.button_frame1_pause = customtkinter.CTkButton(
            frame, width=80, text="Pause"
        )
        self.window.button_frame1_pause.grid(
            row=3, column=2, padx=5, pady=10, sticky="ew"
        )

        self.window.button_frame1_stop = customtkinter.CTkButton(
            frame, width=80, text="Stop"
        )
        self.window.button_frame1_stop.grid(
            row=3, column=3, padx=5, pady=10, sticky="ew"
        )

        self.window.button_frame1_min5s = customtkinter.CTkButton(
            frame, width=50, text="+5s"
        )
        self.window.button_frame1_min5s.grid(
            row=3, column=4, padx=10, pady=10, sticky="ew"
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
            frame, text="Threshold"
        )
        self.window.label_slider_frame2.grid(
            row=1, column=6, padx=5, pady=(10, 0), sticky="ews"
        )
        self.window.slider_frame2 = customtkinter.CTkSlider(
            frame, from_=0, to=100, number_of_steps=100
        )
        self.window.slider_frame2.grid(
            row=2, column=6, columnspan=5, padx=10, pady=(0, 10), sticky="ewn"
        )

        self.window.button_frame2_switcher = customtkinter.CTkButton(
            frame, width=80, text="Binary"
        )
        self.window.button_frame2_switcher.grid(
            row=3, column=8, padx=10, pady=10, sticky="ew"
        )

        self.window.button_frame2_snapshot = customtkinter.CTkButton(
            frame, width=80, text="Snapshot"
        )
        self.window.button_frame2_snapshot.grid(
            row=3, column=9, padx=10, pady=10, sticky="ew"
        )

        self.window.button_result = customtkinter.CTkButton(
            frame, width=80, text="Results"
        )
        self.window.button_result.grid(row=3, column=10, padx=10, pady=10, sticky="ew")

    def run(self):
        self.window.mainloop()


class MaskingView:
    pass


class ResultView:
    pass

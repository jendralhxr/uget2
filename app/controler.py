import customtkinter
from customtkinter import filedialog
from PIL import Image
from view import OpenFileView


class MainWindowControler:
    def __init__(self, view, model, config) -> None:
        self.view = view
        self.config = config
        self.model = model

        self.init_callbacks()
        self.open_video()
        self.view.run()

    def open_video(self):
        top = OpenFileView(self.view.window, None)
        # top.protocol("WM_DELETE_WINDOW", self.on_top_window_close)
        self.view.window.withdraw()
        top.deiconify()

    def init_callbacks(self):
        ###############################################################################
        # Frame 1 widgets callbacks init (Annotated Video)
        ###############################################################################
        self.view.window.slider_frame1.configure(command=self.slider_frame1_event)
        self.view.window.button_frame1_add5s.configure(
            command=self.button_frame1_add5s_pressed
        )
        self.view.window.button_frame1_play.configure(
            command=self.button_frame1_play_pressed
        )
        self.view.window.button_frame1_pause.configure(
            command=self.button_frame1_pause_pressed
        )
        self.view.window.button_frame1_stop.configure(
            command=self.button_frame1_stop_pressed
        )
        self.view.window.button_frame1_min5s.configure(
            command=self.button_frame1_min5s_pressed
        )

        ###############################################################################
        # Frame 2 widgets  (Binary and Heatmap Video)
        ###############################################################################
        self.view.window.slider_frame2.configure(command=self.slider_frame2_event)
        self.view.window.button_frame2_switcher.configure(
            command=self.button_frame2_switcher_pressed
        )
        self.view.window.button_frame2_snapshot.configure(
            command=self.button_frame2_snapshot_pressed
        )
        self.view.window.button_result.configure(command=self.button_result_pressed)

    def slider_frame1_event(self, value):
        print(int(value))

    def button_frame1_add5s_pressed(self):
        print("btn pressed")
        pass

    def button_frame1_play_pressed(self):
        self.view.image1 = customtkinter.CTkImage(
            light_image=Image.open("1160s.png"),
            dark_image=Image.open("1160s.png"),
            size=(int(640 * 0.75), int(480 * 0.75)),
        )
        self.view.window.video_frame1.configure(image=self.view.image1)
        self.view.window.video_frame1.update()

    def button_frame1_pause_pressed(self):
        self.view.image1 = customtkinter.CTkImage(
            light_image=Image.open("4879.png"),
            dark_image=Image.open("4879.png"),
            size=(int(640 * 0.75), int(480 * 0.75)),
        )
        self.view.window.video_frame1.configure(image=self.view.image1)
        self.view.window.video_frame1.update()

    def button_frame1_stop_pressed(self):
        print("btn pressed")
        pass

    def button_frame1_min5s_pressed(self):
        print("btn pressed")
        pass

    def slider_frame2_event(self, value):
        print(int(value))

    def button_frame2_switcher_pressed(self):
        print("btn pressed")
        pass

    def button_frame2_snapshot_pressed(self):
        print("btn pressed")
        pass

    def button_result_pressed(self):
        print("btn pressed")
        pass


class OpenFileControler:
    def __init__(self, view, model, config) -> None:
        self.view = view
        self.config = config
        self.model = model

    def button_callback(self):
        filename = filedialog.askopenfilename()
        print(f"file name is {filename}")
        self.withdraw()
        top = self.view.main_view(self)
        top.protocol("WM_DELETE_WINDOW", self.on_top_window_close)
        top.deiconify()

    def on_top_window_close(self):
        self.deiconify()
        self.destroy()


class MaskingControler:
    def __init__(self, view, model, config) -> None:
        self.view = view
        self.config = config
        self.model = model


class ResultControler:
    def __init__(self, view, model, config) -> None:
        self.view = view
        self.config = config
        self.model = model

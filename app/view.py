import customtkinter
from customtkinter import filedialog
from PIL import Image, ImageTk


class MainWindowView:
    def __init__(self):
        super().__init__()
        self._show_gui("Uget-Uget Counting ver 0.1")

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


class OpenFileView:
    def __init__(self):
        self.title = "Open video file"

    def _build_gui(self, parent):
        self.window = customtkinter.CTkToplevel(parent)
        self.window.title(self.title)
        self.window.geometry("400x180")
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)

        self.window.label = customtkinter.CTkLabel(
            self.window, text="Welcome to Uget-Uget Counting ver 0.1"
        )
        self.window.label.grid(row=0, columnspan=3, padx=10, pady=10, sticky="ew")
        self.window.button_load_video = customtkinter.CTkButton(
            self.window, width=80, text="Load Video"
        )
        self.window.button_load_video.grid(
            row=1, column=1, padx=10, pady=10, sticky="ew"
        )

    def run(self, parent):
        self._build_gui(parent)
        self.window.deiconify()


class MaskingView:
    def __init__(self):
        super().__init__()
        self.title = "Masking - Uget-Uget Counting ver 0.1"

    def _build_gui(self, parent):
        self.window = customtkinter.CTkToplevel(parent)
        self.window.title(self.title)
        self.window.geometry("1024x640")

        frame = customtkinter.CTkFrame(self.window)
        frame.place(relx=0.5, rely=0.5, anchor="c")

        self.image1 = Image.open("4879.png")

        img = ImageTk.PhotoImage(self.image1)
        canvas = customtkinter.CTkCanvas(frame,width=int(640),height=int(480))
        canvas.image = img
        canvas.create_image(0,0,anchor='nw',image=img)
        canvas.grid(row=0, columnspan=5, padx=10, pady=10, sticky="ew")
        canvas.bind("<Button 1>", self.get_coor)
        
        self.window.button_clear_masking = customtkinter.CTkButton(
            frame, width=80, text="clear"
        )   
        self.window.button_clear_masking.grid(
            row=1, column=3, padx=10, pady=10, sticky="ew"
        )

        self.window.button_masking = customtkinter.CTkButton(
            frame, width=80, text="masking"
        )

        self.window.button_masking.grid(
            row=1, column=4, padx=10, pady=10, sticky="ew"
        )

    def get_coor(self, event):
        mouse_xy = (event.x, event.y)
        print(mouse_xy)

    def run(self, parent):
        self._build_gui(parent)
        self.window.deiconify()


class ResultView:
    pass


# frame information
# snapshots 2 tombol
# ukuran frame

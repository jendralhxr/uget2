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

        self.label = customtkinter.CTkLabel(self, text="Welcome to Uget-Uget Counting ver 0.1")
        self.label.grid(row=0, columnspan=3, padx=10, pady=10, sticky="ew")
        self.button = customtkinter.CTkButton(self, width = 80, text="Load Video", command=self.button_callback)
        self.button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    def button_callback(self):
        self.master.deiconify()
        pass

class MainWindowView():
    def __init__(self):
        super().__init__()
        self.callbacks={}
        #self._init_assets()
        self._show_gui("Uget-Uget Counting ver 0.1")
        self.open_video()

        self.run() #this shpuld be called in controler

    def _show_gui(self, title):
        self.window = customtkinter.CTk()
        self.window.title(title)
        self.window.geometry("1024x640")

        frame = customtkinter.CTkFrame(self.window)
        frame.place(relx=0.5, rely=0.5, anchor="c")

        self.image1 = customtkinter.CTkImage(light_image=Image.open("4879.png"),
                                  dark_image=Image.open("4879.png"),
                                  size=(int(640*0.75), int(480*0.75)))
        self.window.video_frame1 = customtkinter.CTkLabel(frame, image=self.image1, text="")  # display image with a CTkLabel
        self.window.video_frame1.grid(row=0, columnspan=5, padx=10, pady=10, sticky="ew")

        self.window.video_frame2 = customtkinter.CTkLabel(frame, image=self.image1, text="")  # display image with a CTkLabel
        self.window.video_frame2.grid(row=0, column = 6,columnspan=5, padx=10, pady=10, sticky="ew")

        self.window.label_frame_slider = customtkinter.CTkLabel(frame, text="Frame")
        self.window.label_frame_slider.grid(row=1, column=0, padx=5, pady=(10,0), sticky="ews")
        self.window.slider = customtkinter.CTkSlider(frame, from_=0, to=100,number_of_steps=100, command=self.slider_event)
        self.window.slider.grid(row=2, column=0, columnspan=5, padx=10, pady=(0,10), sticky="ewn")

        self.window.button_frame_5s = customtkinter.CTkButton(frame, width = 50, text="-5s", command=self.play_video)
        self.window.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.window.button = customtkinter.CTkButton(frame, width = 80, text="Play", command=self.play_video)
        self.window.button.grid(row=3, column=1, padx=5, pady=10, sticky="ew")

        self.window.button = customtkinter.CTkButton(frame,width=80, text="Pause", command=self.pause_video)
        self.window.button.grid(row=3, column=2, padx=5, pady=10, sticky="ew")

        self.window.button = customtkinter.CTkButton(frame,width=80, text="Stop", command=self.play_video)
        self.window.button.grid(row=3, column=3, padx=5, pady=10, sticky="ew")

        self.window.button = customtkinter.CTkButton(frame,width=50, text="+5s", command=self.play_video)
        self.window.button.grid(row=3, column=4, padx=10, pady=10, sticky="ew")


        self.window.label_threshold_slider = customtkinter.CTkLabel(frame, text="Threshold")
        self.window.label_threshold_slider.grid(row=1, column=6, padx=5, pady=(10,0), sticky="ews")
        self.window.slider = customtkinter.CTkSlider(frame, from_=0, to=100,number_of_steps=100, command=self.slider_event)
        self.window.slider.grid(row=2, column=6, columnspan=5, padx=10, pady =(0,10), sticky="ewn")

        self.window.button = customtkinter.CTkButton(frame,width=80, text="Binary", command=self.play_video)
        self.window.button.grid(row=3, column=8, padx=10, pady=10, sticky="ew")

        self.window.button = customtkinter.CTkButton(frame,width=80, text="Snapshot", command=self.play_video)
        self.window.button.grid(row=3, column=9, padx=10, pady=10, sticky="ew")


        self.window.button = customtkinter.CTkButton(frame,width=80, text="Results", command=self.play_video)
        self.window.button.grid(row=3, column=10, padx=10, pady=10, sticky="ew")

        

    def open_video(self):
        top = OpenFileView(self.window, None)
        #top.protocol("WM_DELETE_WINDOW", self.on_top_window_close)
        self.window.withdraw()
        top.deiconify()

    def add_callback(self, key, method):
        self.callbacks[key] = method

    def bind_commands(self):
        self.importButton.config(command=self.callbacks['import'])

    def run(self):
        self.window.mainloop()

    def play_video(self):
        self.image1 = customtkinter.CTkImage(light_image=Image.open("1160s.png"),
                                  dark_image=Image.open("1160s.png"),
                                  size=(int(640*0.75), int(480*0.75)))
        self.window.video_frame1.configure(image = self.image1)
        self.window.video_frame1.update()

    def pause_video(self):
        self.image1 = customtkinter.CTkImage(light_image=Image.open("4879.png"),
                                  dark_image=Image.open("4879.png"),
                                  size=(int(640*0.75), int(480*0.75)))
        self.window.video_frame1.configure(image = self.image1)
        self.window.video_frame1.update()

    def slider_event(self,value):

        print(int(value))


class MaskingView():
    pass

class ResultView():
    pass
        
        
import customtkinter
from customtkinter import filedialog
from PIL import Image
from view import OpenFileView, MaskingView
from PIL import Image, ImageTk


class MainWindowControler:
    def __init__(self, view, model, config) -> None:
        self.view = view
        self.config = config
        self.model = model

        self.init_callbacks()

    def set_video_data(self, video_data):
        self.model.set_video_data(video_data)

    def bind_top_windows_controlers(self, controler_dict):
        self.top_controler = controler_dict

    def run(self, starting=True):
        if starting:
            self.open_video()
            self.view.run()
        else:
            self.model.instantiate_video_player(self.view.window.video_frame1, self.view.window.slider_frame1)

            # set slider params
            self.view.window.slider_frame1._from_ = self.model.video_data.start_frame
            self.view.window.slider_frame1._to = self.model.video_data.end_frame
            self.view.window.slider_frame1._number_of_steps = self.model.video_data.end_frame
            self.view.window.slider_frame1.set(self.model.video_data.start_frame)

            self.model.video_player.show_frame(self.model.video_data.start_frame)
            self.view.window.deiconify()
            
    def open_video(self):
        self.top_controler["open_file"].run(self)
        self.view.window.withdraw()

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
        print("slider event")
        if self.model.video_player.playing:
            self.model.video_player.pause()
        self.model.video_player.set_frame_to(int(value), set_slider=False)
        self.view.window.slider_frame1.set(int(value))
        print(int(value))

    def button_frame1_min5s_pressed(self):
        current_frame = self.model.video_player.current_frame
        self.model.video_player.set_frame_to(current_frame - 5)
        self.model.video_player.pause()

    def button_frame1_play_pressed(self):
        self.model.video_player.play()

    def button_frame1_pause_pressed(self):
        self.model.video_player.pause()

    def button_frame1_stop_pressed(self):
        self.model.video_player.stop()

    def button_frame1_add5s_pressed(self):
        current_frame = self.model.video_player.current_frame
        self.model.video_player.set_frame_to(current_frame + 5)
        self.model.video_player.pause()

    def slider_frame2_event(self, value):
        print(int(value))

    def button_frame2_switcher_pressed(self):
        print("btn switch pressed")
        pass

    def button_frame2_snapshot_pressed(self):
        print("btn snapshot pressed")
        pass

    def button_result_pressed(self):
        print("btn result pressed")
        pass


class OpenFileControler:
    def __init__(self, view, model, config) -> None:
        self.view = view
        self.config = config
        self.model = model

    def init_callbacks(self):
        self.view.window.button_load_video.configure(
            command=self.button_load_video_pressed
        )

    def button_load_video_pressed(self):
        filename = filedialog.askopenfilename()
        print(f"file name is {filename}")
        self.model.set_file_name(filename)

        # load video data to the main controler
        video_data = self.model.load_video()
        self.parent_controler.set_video_data(video_data)

        self.view.window.withdraw()
        self.parent_controler.top_controler["masking"].set_start_frame_image(
            video_data.first_frame_img
        )
        self.parent_controler.top_controler["masking"].run(self.parent_controler)

    def run(self, parent_controler):
        self.parent_controler = parent_controler
        self.view.run(parent_controler.view.window)
        self.init_callbacks()


class MaskingControler:
    def __init__(self, view, model, config) -> None:
        self.view = view
        self.config = config
        self.model = model

    def init_callbacks(self):
        # mask via mouse click bind
        self.view.window.masking_canvas.bind("<Button 1>", self.get_coor)

        self.view.window.button_undo_masking.configure(
            command=self.button_undo_masking_pressed
        )
        self.view.window.button_clear_masking.configure(
            command=self.button_clear_masking_pressed
        )
        self.view.window.button_masking.configure(command=self.button_masking_pressed)

    def button_undo_masking_pressed(self):
        self.model.pop_mask_coordinate()
        if len(self.model.mask_coordinate) != 0:
            self.draw_mask()

    def button_clear_masking_pressed(self):
        self.model.clear_mask_coordinate()
        self.delete_mask()

    def button_masking_pressed(self):
        print("Masked")
        self.view.window.withdraw()
        self.parent_controler.model.video_data.mask_coordinate = self.model.mask_coordinate
        self.parent_controler.run(starting=False)

    def get_coor(self, event):
        mouse_xy = (event.x, event.y)
        self.model.add_mask_coordinate(mouse_xy)
        self.draw_mask()
        print(mouse_xy)
        print(self.model.mask_coordinate)

    def draw_mask(self):
        mask_coordinate = self.model.get_mask_coordinate()
        self.view.window.masking_canvas.delete("mask_polygon")
        self.view.window.masking_canvas.delete("mask_line")
        if len(mask_coordinate) > 2:
            self.view.window.masking_canvas.create_line(
                mask_coordinate, tag="mask_line"
            )
            self.view.window.masking_canvas.create_polygon(
                mask_coordinate, tag="mask_polygon"
            )

    def delete_mask(self):
        self.view.window.masking_canvas.delete("mask_polygon")
        self.view.window.masking_canvas.delete("mask_line")

    def set_start_frame_image(self, img):
        self.view.set_start_frame_image(img)

    def run(self, parent_controler):
        self.parent_controler = parent_controler
        self.view.run(parent_controler.view.window)
        self.init_callbacks()


class ResultControler:
    def __init__(self, view, model, config) -> None:
        self.view = view
        self.config = config
        self.model = model

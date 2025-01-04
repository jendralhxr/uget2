from customtkinter import filedialog
import threading


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
            if self.model.video_data.file_name:
                self.view.set_title(f"COMOT - {self.model.video_data.file_name}")
            self.model.instantiate_video_player(
                self.view.window.video_frame1,
                self.view.window.video_frame2,
                self.view.window.slider_frame1,
                self.view.window.label_slider_frame1,
                self.view.color_bar,
            )

            # set slider params
            self.view.window.slider_frame1._from_ = self.model.video_data.start_frame
            self.view.window.slider_frame1._to = self.model.video_data.end_frame
            self.view.window.slider_frame1._number_of_steps = (
                self.model.video_data.end_frame
            )
            self.view.window.slider_frame1.set(self.model.video_data.start_frame)

            self.model.video_player.show_frame(self.model.video_data.start_frame)
            self.view.window.deiconify()

    def open_video(self):
        self.top_controler["open_file"].run(self)
        self.view.window.withdraw()

    def update_frame(self):
        value = self.view.window.slider_frame1.get()
        self.model.video_player.set_frame_to(int(value), set_slider=False)

    def init_callbacks(self):
        ###############################################################################
        # Frame 1 widgets callbacks init (Annotated Video)
        ###############################################################################
        # self.view.window.slider_frame1.configure(command=self.slider_frame1_event)
        self.view.window.slider_frame1.bind(
            "<ButtonRelease-1>", self.slider_frame1_event
        )
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
        self.view.window.slider_frame2.configure(
            command=self.slider_frame2_event, state="disabled"
        )
        self.view.window.option_menu_frame2_thresholding_method.configure(
            command=self.option_menu_frame2_thresholding_method_event
        )
        self.view.window.button_frame2_switcher.configure(
            command=self.button_frame2_switcher_pressed
        )
        self.view.window.button_frame2_snapshot.configure(
            command=self.button_frame2_snapshot_pressed
        )
        self.view.window.button_result.configure(command=self.button_result_pressed)

    def slider_frame1_event(self, event):
        value = self.view.window.slider_frame1.get()
        if self.model.video_player.playing:
            self.model.video_player.set_frame_to(int(value), set_slider=False)
            self.model.video_player.pause(value)
        self.model.video_player.set_frame_to(int(value), set_slider=False)

    def button_frame1_min5s_pressed(self):
        current_frame = self.model.video_player.current_frame
        fps = self.model.video_player.video_data.fps
        targetframe = current_frame - int(5 * fps)
        if targetframe < 0:
            targetframe = 0
        self.model.video_player.pause()
        self.model.video_player.set_frame_to(targetframe)
        self.model.video_player.play()

    def button_frame1_play_pressed(self):
        self.model.video_player.play()

    def button_frame1_pause_pressed(self):
        self.model.video_player.pause()

    def button_frame1_stop_pressed(self):
        self.model.video_player.stop()

    def button_frame1_add5s_pressed(self):
        current_frame = self.model.video_player.current_frame
        fps = self.model.video_player.video_data.fps
        targetframe = current_frame + int(5 * fps)
        if targetframe >= self.model.video_player.framecount:
            targetframe = self.model.video_player.framecount - int(5 * fps)
        self.model.video_player.pause()
        self.model.video_player.set_frame_to(targetframe)
        self.model.video_player.play()

    def slider_frame2_event(self, value):
        self.model.video_player.binary_thresholding_param = int(value)
        self.view.window.label_slider_frame2.configure(
            text=f"Threshold (Binary): {int(value)}"
        )
        self.update_frame()

    def option_menu_frame2_thresholding_method_event(self, value):
        if value == "Triangle":
            self.view.window.slider_frame2.configure(state="disabled")
            self.model.video_player.thresholding_method = "triangle"
        elif value == "Binary  ":
            self.view.window.slider_frame2.configure(state="normal")
            self.model.video_player.thresholding_method = "binary"
        self.update_frame()

    def button_frame2_switcher_pressed(self):
        if self.model.video_player.mode == "binary":
            self.model.video_player.mode = "heatmap"
            self.view.window.button_frame2_switcher.configure(text="Heatmap")
        else:
            self.model.video_player.mode = "binary"
            self.view.window.button_frame2_switcher.configure(text="Binary")
        self.update_frame()

    def button_frame2_snapshot_pressed(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*"),
            ],
        )
        if file_path:  # Check if a path was selected
            self.model.video_player.current_processed_image.save(file_path)

    def button_result_pressed(self):
        self.model.video_player.stop()
        print("btn result pressed")
        self.view.window.withdraw()
        self.top_controler["result_process"].run(self)


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
        filepath = filedialog.askopenfilename()
        self.model.set_file_path(filepath)

        # load video data to the main controler
        video_data = self.model.load_video()
        self.parent_controler.set_video_data(video_data)

        self.view.window.withdraw()
        self.parent_controler.top_controler["masking"].set_start_frame_image(
            video_data.ref_image
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
        self.view.window.withdraw()
        self.parent_controler.model.video_data.mask_coordinate = (
            self.model.mask_coordinate
        )
        self.parent_controler.run(starting=False)

    def get_coor(self, event):
        mouse_xy = (event.x, event.y)
        self.model.add_mask_coordinate(mouse_xy)
        self.draw_mask()

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


class ResultProcessControler:
    def __init__(self, view, model, config) -> None:
        self.view = view
        self.config = config
        self.model = model

    def init_callbacks(self):
        self.view.window.button_process.configure(
            command=self.button_get_result_pressed
        )
        end_time = round(
            self.parent_controler.model.video_data.end_frame
            / self.parent_controler.model.video_data.fps,
            3,
        )
        self.view.window.entry_start.insert(0, string=0)
        self.view.window.entry_end.insert(0, string=end_time)

    def button_get_result_pressed(
        self,
    ):
        start_time = self.view.window.entry_start.get()
        end_time = self.view.window.entry_end.get()

        self.view.window.withdraw()

        self.parent_controler.top_controler["processing"].run(
            self, self.parent_controler.model.video_player, start_time, end_time
        )

    def run(self, parent_controler):
        self.parent_controler = parent_controler
        self.view.run(parent_controler.view.window)
        self.init_callbacks()


class ProcessingControler:
    def __init__(self, view, model, config) -> None:
        self.view = view
        self.config = config
        self.model = model

    def run(self, parent_controler, video_player, start_time, end_time):
        self.parent_controler = parent_controler.parent_controler

        # Show the view
        self.view.run(self.parent_controler.view.window)

        # Perform calculations in a separate thread
        threading.Thread(
            target=self.calculate_and_update, args=(video_player, start_time, end_time)
        ).start()

    def calculate_and_update(self, video_player, start_time, end_time):
        count_per_second, tk_image_count_plot, meta_data = self.model.calculate_count(
            video_player, start_time, end_time
        )

        self.parent_controler.top_controler["result"].run(
            self, count_per_second, tk_image_count_plot, meta_data
        )
        self.view.window.withdraw()


class ResultControler:
    def __init__(self, view, model, config) -> None:
        self.view = view
        self.config = config
        self.model = model
        self.count_per_second = None
        self.tmp_count_plot_path = None

    def init_callbacks(self):
        self.view.window.button_save_csv.configure(command=self.button_save_csv_pressed)
        self.view.window.button_save_image.configure(
            command=self.button_save_image_pressed
        )

    def button_save_csv_pressed(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                ("csv files", "*.csv"),
            ],
        )
        if file_path:
            self.model.save_csv(file_path, self.count_per_second, self.meta_data)

    def button_save_image_pressed(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*"),
            ],
        )
        if file_path:
            self.model.save_image(file_path, self.count_per_second, self.meta_data)

    def run(self, parent_controler, count_per_second, tk_image_count_plot, meta_data):
        self.count_per_second = count_per_second
        self.meta_data = meta_data
        self.parent_controler = parent_controler
        self.view.run(parent_controler.view.window)
        self.view.set_image(tk_image_count_plot)
        self.init_callbacks()

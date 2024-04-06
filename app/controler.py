from customtkinter import filedialog

class AppControler():

    def __init__(self, main_controler, open_file_controler, masking_controler, result_controler) -> None:
        
        self.main_controler = main_controler
        self.open_file_controler = open_file_controler 
        self.masking_controler = masking_controler 
        self.result_controler = result_controler

    def mainloop(self):
        self.main_controler.view.mainloop()



class OpenFileControler():

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


class MainWindowControler():

    def __init__(self, view, model, config) -> None:
        self.view = view
        self.config = config
        self.model = model

class MaskingControler():
    def __init__(self, view, model, config) -> None:
        self.view = view
        self.config = config
        self.model = model

class ResultControler():
    def __init__(self, view, model, config) -> None:
        self.view = view
        self.config = config
        self.model = model
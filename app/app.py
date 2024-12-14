from config import Configuration
from controler import (
    MainWindowControler,
    OpenFileControler,
    MaskingControler,
    ResultControler,
    ResultProcessControler,
    ResultControler
)
from view import (
    MainWindowView,
    OpenFileView,
    MaskingView,
    ResultView,
    ResultProcessView,
    ResultView
)
from model import (
    MainWindowModel,
    OpenFileModel,
    MaskingModel,
    ResultModel,
    ResultProcessModel,
    ResultModel
)

config = Configuration()

# main windows instantiation
main_view = MainWindowView()
main_model = MainWindowModel()
main_controler = MainWindowControler(main_view, main_model, config)

# open file instantiation
open_file_view = OpenFileView()
open_file_model = OpenFileModel()
open_file_controler = OpenFileControler(open_file_view, open_file_model, config)

# masking instantiation
masking_view = MaskingView()
masking_model = MaskingModel()
masking_controler = MaskingControler(masking_view, masking_model, config)

# result process instantiation
result_process_view = ResultProcessView()
result_process_model = ResultProcessModel()
result_process_controler = ResultProcessControler(
    result_process_view, result_process_model, config
)

# result instantiation
result_view = ResultView()
result_model = ResultModel()
result_controler = ResultControler(result_view, result_model, config)

controlers = {
    "open_file": open_file_controler,
    "masking": masking_controler,
    "result": result_controler,
    "result_process": result_process_controler,
}

main_controler.bind_top_windows_controlers(controlers)
main_controler.run()

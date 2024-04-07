from config import Configuration
from controler import (
    MainWindowControler,
    OpenFileControler,
    MaskingControler,
    ResultControler,
)
from view import MainWindowView, OpenFileView, MaskingView, ResultView
from model import MainWindowModel, OpenFileModel, MaskingModel, ResultModel

config = Configuration()

# open file instantiation
open_file_view = OpenFileView()
open_file_model = OpenFileModel()
open_file_controler = OpenFileControler(open_file_view, open_file_model, config)

# masking instantiation
masking_view = MaskingView()
masking_model = MaskingModel()
masking_controler = MaskingControler(masking_view, masking_model, config)

# result instantiation
result_view = ResultView()
result_model = ResultModel()
result_controler = ResultControler(result_view, result_model, config)

# main windows instantiation
main_view = MainWindowView()
main_model = MainWindowModel()
main_controler = MainWindowControler(main_view, main_model, config)

main_controler.run()

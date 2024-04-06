from config import Configuration
from controler import (
    MainWindowControler,
    OpenFileControler,
    MaskingControler,
    ResultControler,
)
from view import MainWindowView, OpenFileView, MaskingView, ResultView
from model import MainWindowModel, OpenFileModel, MaskingModel, ResultModel

# call config

# instantiate controlers (feed )

# feed controlers
config = Configuration()
# main_window_controler = MainWindowControler(MainWindowView(), MainWindowModel())


main_view = MainWindowView()
main_controler = MainWindowControler(main_view, None, config)

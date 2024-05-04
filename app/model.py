from itertools import chain


class OpenFileModel:
    pass


class MainWindowModel:
    pass


class MaskingModel:
    def __init__(self) -> None:
        self.mask_coordinate = []

    def add_mask_coordinate(self, coordinate):
        self.mask_coordinate.append(coordinate)
        if len(self.mask_coordinate) == 2:
            self.mask_coordinate.append(coordinate)

    def pop_mask_coordinate(self):
        if len(self.mask_coordinate) != 0:
            self.mask_coordinate.pop()
        print(self.mask_coordinate)

    def clear_mask_coordinate(self):
        self.mask_coordinate.clear()
        print(self.mask_coordinate)

    def get_mask_coordinate(self):
        return list(chain(self.mask_coordinate))


class ResultModel:
    pass

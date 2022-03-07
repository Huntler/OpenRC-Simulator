from typing import Tuple


class Wall:
    dict_name = "walls"
    def __init__(self, start_pos: Tuple, end_pos: Tuple) -> None:
        self.__start_pos = start_pos
        self.__end_pos = end_pos
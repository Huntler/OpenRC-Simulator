from typing import Tuple
from graphics.objects.sprite import Sprite


class Goal(Sprite):
    def __init__(self) -> None:
        super().__init__()
    
    def draw(self) -> None:
        super().draw()

    def collidepoint(self, point: Tuple[int, int]) -> bool:
        pass
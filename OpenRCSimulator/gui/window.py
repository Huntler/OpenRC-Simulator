from OpenRCSimulator.graphics.window import BaseWindow


class MainWindow(BaseWindow):
    def sprites(self) -> None:
        # define sprites here
        pass

    def draw(self) -> None:
        pass

    def event(self, event) -> None:
        super().event(event)
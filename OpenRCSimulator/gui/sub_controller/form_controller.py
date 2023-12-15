from typing import Any, Dict, List, Tuple
from OpenRCSimulator.graphics.callback import TextListener
from OpenRCSimulator.graphics.objects.rectangle import Rectangle
from OpenRCSimulator.graphics.objects.sprite import Sprite
from OpenRCSimulator.graphics.objects.text import Text
from OpenRCSimulator.graphics.objects.text_field import TextField
from OpenRCSimulator.graphics.window import BaseWindow

from OpenRCSimulator.graphics.sub_controller import BaseSubController
from OpenRCSimulator.gui import FORM_TITLE_SEPARATION, FORM_BACKGROUND_COLOR, FORM_ELEMENT_SEPARATION, FORM_MARGIN, FORM_TEXT_COLOR


class FormListener:
    def on_form_change(self, name: str, value: Any) -> None:
        pass


class FormController(BaseSubController, TextListener):

    LEFT_ALIGNED = 0
    CENTER_ALIGNED = 1
    RIGHT_ALIGNED = 2

    def __init__(self, window: BaseWindow, title: str, position: Tuple[int, int], size: Tuple[int, int], 
                 alignment: int = 0, listener: FormListener = None) -> None:
        super().__init__()
        self._window = window
        self._surface = self._window.get_surface()
        self._listener = listener

        # configure the form
        self._elements: Dict[str: Tuple[int, Text, TextField]]= {}
        self._align = alignment
        self._x, self._y = position
        self._w, self._h = size

        # define fonts
        self._font_form_title = self._window.get_font().copy(size=40)
        self._font_element_title = self._window.get_font().copy(size=32)
        self._font_element = self._window.get_font().copy(size=28)

        # get font heights
        self._height_form_title = self._font_form_title.unpack().size("Example")[1]
        self._height_element_title = self._font_element_title.unpack().size("Example")[1]
        self._height_element = self._font_element.unpack().size("Example")[1]
        
        # create title object
        self._title = Text(self._surface, title, 0, 0, FORM_TEXT_COLOR, self._font_form_title)
        self._window.add_sprite(f"text_form_{title}", self._title)

        # create background
        self._background = Rectangle(self._surface, self._x, self._y, self._w, self._h, FORM_BACKGROUND_COLOR)
        self._window.add_sprite(f"background_form_{title}", self._background, zindex=97)
    
    def on_text_changed(self, object: TextField, text: str) -> None:
        if object.is_activated():
            # update the text of the active element
            object.update_text(text)

            if not self._listener:
                return
            
            # get the register name of the active element
            name = ""
            for name, tuple_object in self._elements.items():
                _, _, element = tuple_object
                if element == object:
                    break
                    
            # inform the upper controller that something has changed
            value = text
            if object.filter == TextField.FILTER_NUMBERS:
                value = float(text)
            self._listener.on_form_change(name, value)
    
    def on_text_end(self, object: TextField) -> None:
        object.deactivate()
    
    def _activate_element(self) -> None:
        """Deactivate input fields if a new one gets selected.
        """
        for name, object in self._elements.items():
            _, _, element = object
            element.deactivate()

        self._window.toggle_text_capture(overwrite=True)
    
    def _update_positions(self) -> None:
        if len(self._elements) == 0:
            return
        
        # position each entry correctly
        elements: List[Tuple[Sprite, Sprite]] = sorted([_ for _ in self._elements.values()], key=lambda x: x[0])
        elements.insert(0, (0, self._title, self._background))

        # position the elements on screen
        y = self._y + FORM_MARGIN[1]
        for i, title, element in elements:
            w = max(title.get_size()[0], element.get_size()[0])
            h = max(title.get_size()[1], element.get_size()[1])

            # calculate position
            x = self._x + FORM_MARGIN[0]
            if self._align == FormController.CENTER_ALIGNED:
                x = self._x + (self._w + FORM_MARGIN[2]) / 2
            elif self._align == FormController.RIGHT_ALIGNED:
                x = self._x + self._w - w
            
            # set position of title
            if i == 0:
                title.set_position((self._x + (self._w + FORM_MARGIN[2]) / 2, y), Text.ANCHOR_CENTER)
            else:
                title.set_position((x, y), Text.ANCHOR_TOP_LEFT)
            y += title.get_size()[1] + FORM_TITLE_SEPARATION

            # set position of element
            if i != 0:
                element.set_position((x, y))
                y += element.get_size()[0] + FORM_ELEMENT_SEPARATION
        
        # reset background
        self._background.set_position((self._x, self._y))

        # warn if size exceeds initial definition
        if self._h < y:
            print(f"Element {self._title.get_text()} oversaturated.")
    
    def add_element(self, name: str, title: str, default: str = "", filter: int = TextField.FILTER_NONE) -> None:
        # element title
        element_title = Text(self._surface, title, 0, 0, FORM_TEXT_COLOR, self._font_element_title)       
        element = TextField(self._surface, 0, 0, default, self._font_element)

        element.on_activated(self._activate_element)
        element.set_text_filter(filter)

        # setup on window
        self._window.add_sprite("title_" + name, element_title)
        self._window.add_sprite("element" + name, element)
        self._window.set_listener(self, element)

        self._elements[name] = (len(self._elements) + 1, element_title, element)

        # calculate start display height of form
        self._update_positions()

    def remove_element(self, name: str) -> None:
        self._window.remove_listener(self, self._elements[name])
        del self._elements[name]
    
    def get_data(self) -> Dict[str, Any]:
        """Collects all data from the form and outputs as formatted dict.

        Returns:
            Dict[str, Any]: Containing formatted values.
        """
        data = {}

        for name, (_, _, element) in self._elements.items():
            value = element.get_text() if len(element.get_text()) != 0 else None
            if element.filter == TextField.FILTER_NUMBERS and value:
                value = float(value)
            data[name] = value
        
        return data

    def set_data(self, data: Dict[str, Any]) -> None:        
        for name, (_, _, element) in self._elements.items():
            value = data.get(name, None)
            if value:
                element.set_text(str(value))

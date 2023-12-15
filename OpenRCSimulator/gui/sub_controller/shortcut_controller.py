from typing import Callable, Dict
from OpenRCSimulator.graphics.callback import KeyListener
from OpenRCSimulator.graphics.objects.text import Text
from OpenRCSimulator.graphics.sub_controller import BaseSubController
from OpenRCSimulator.graphics.window import BaseWindow
from OpenRCSimulator.gui import SHORTCUT_TEXT_COLOR, SHORTCUT_TEXT_COLOR_ACTIVE, SHORTCUT_ENTRY_SEPARATION


class ShortcutController(BaseSubController, KeyListener):
    def __init__(self, window: BaseWindow) -> None:
        super().__init__()

        self._entries = {}
        self._toggled = []
        self._callback_registry: Dict[int, Callable] = {}

        # window and surface information
        self._window = window
        self._window.set_listener(self)
        self._ww, self._wh = window.get_window_size()
        self._surface = window.get_surface()

        # define fonts
        self._font_title = window.get_font().copy(size=36)
        self._font_entry = window.get_font().copy(size=30)

        # get font heights
        self._title_height = self._font_title.unpack().size("Example")[1]
        self._entry_height = self._font_entry.unpack().size("Example")[1]

        # create title object
        self._title = Text(self._surface, "Shortcuts", 0, 0, SHORTCUT_TEXT_COLOR, self._font_title)
        self._window.add_sprite("text_storage", self._title)

    def on_key_pressed(self, key: int) -> None:
        if key in self._callback_registry.keys():
            self._callback_registry[key]()
    
    def _update_positions(self) -> None:
        """Updates the positions by changing the y coordinate depending on the amount of shortcuts added.
        """
        if len(self._entries) == 0:
            return
        
        # calculate start display height of shortcut section
        section_height = self._wh - (self._title_height + (len(self._entries) * (self._entry_height + SHORTCUT_ENTRY_SEPARATION))) - 20
        self._title.set_position((20, section_height), anchor=Text.ANCHOR_TOP_LEFT)

        # position each entry correctly
        entry_list = sorted([_ for _ in self._entries.values()], key=lambda x: x[0])
        for i, entry, _ in entry_list:
            entry_y = section_height + SHORTCUT_ENTRY_SEPARATION * i + self._entry_height * i
            entry.set_position((20, entry_y), Text.ANCHOR_TOP_LEFT)
            print(section_height, entry_y)
            
    def add_shortcut(self, name: str, callback, title: str, key: int, can_toggle: bool = False) -> None:    
        # add the shortcut text and callback
        shortcut = Text(self._surface, title, 0, 0, SHORTCUT_TEXT_COLOR, self._font_entry)       
        self._window.add_sprite(name, shortcut)

        callback = callback if not can_toggle else self._toggle(name, callback)
        self._callback_registry[key] = callback

        self._entries[name] = (len(self._entries) + 1, shortcut, key)

        # calculate start display height of shortcut section
        self._update_positions()
    
    def remove_shortcut(self, name: str) -> None:
        num, _, key= self._entries[name]
        self._toggled.pop(num - 1)

        del self._entries[name]
        del self._callback_registry[key]
    
    def untoggle_all(self) -> None:
        for name in self._toggled:
            self._entries[name][1].set_color(SHORTCUT_TEXT_COLOR)
        
        self._toggled = []

    def _toggle(self, name: str, func) -> None:
        def toggle_text():
            num, entry, _ = self._entries[name]
            if name not in self._toggled:
                self._toggled.append(name)
                entry.set_color(SHORTCUT_TEXT_COLOR_ACTIVE)
            else:
                self._toggled.remove(name)
                entry.set_color(SHORTCUT_TEXT_COLOR)
            
            func()
        
        return toggle_text
        



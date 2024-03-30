"""This module manages a shortcut controller which can be added to any controller."""
from typing import Callable, Dict
from OpenRCSimulator.graphics.callback import KeyListener
from OpenRCSimulator.graphics.objects.text import Text
from OpenRCSimulator.graphics.sub_controller import BaseSubController
from OpenRCSimulator.graphics.window import BaseWindow
from OpenRCSimulator.gui import SHORTCUT_TEXT_COLOR, SHORTCUT_TEXT_COLOR_ACTIVE, \
    SHORTCUT_ENTRY_SEPARATION


class ShortcutController(BaseSubController, KeyListener):
    """The shortcut controller allows shortcuts to be defined and action
    executed.

    Args:
        BaseSubController (BaseSubController): The base class.
        KeyListener (KeyListener): This controller reacts to key pressed events.
    """

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
        self._font_title = window.get_font().copy(size=16)
        self._font_entry = window.get_font().copy(size=14)

        # get font heights
        self._title_height = self._font_title.unpack().size("Example")[1]
        self._entry_height = self._font_entry.unpack().size("Example")[1]

        # create title object
        self._title = Text(self._surface, "Shortcuts", 0, 0,
                           SHORTCUT_TEXT_COLOR, self._font_title)
        self._window.add_sprite("text_storage", self._title)

    def on_key_pressed(self, key: int) -> None:
        if key in self._callback_registry:
            for callback in self._callback_registry[key].items():
                callback[1]()

    def _update_positions(self) -> None:
        """Updates the positions by changing the y coordinate depending on the amount of 
        shortcuts added.
        """
        if len(self._entries) == 0:
            return

        # calculate start display height of shortcut section
        section_height = self._wh - (self._title_height + (
            len(self._entries) * (self._entry_height + SHORTCUT_ENTRY_SEPARATION))) - 20
        self._title.set_position((20, section_height),
                                 anchor=Text.ANCHOR_TOP_LEFT)

        # position each entry correctly
        entry_list = sorted(
            [_ for _ in self._entries.values()], key=lambda x: x[0])
        for i, entry, _ in entry_list:
            entry_y = section_height + SHORTCUT_ENTRY_SEPARATION * i + self._entry_height * i
            entry.set_position((20, entry_y), Text.ANCHOR_TOP_LEFT)
            print(section_height, entry_y)

    def add_shortcut(self, name: str, callback, title: str, key: int,
                     can_toggle: bool = False, silent: bool = False) -> None:
        """This method adds a shortcut to the controller.

        Args:
            name (str): Referal name.
            callback (function): Action to execute if shortcut is
            title (str): The text shown on scree.
            key (int): The key to press.
            can_toggle (bool, optional): Can be enabled and disabled, if true. Defaults to False.
            silent (bool, optional): Show the shortcut as text on screen. Defaults to False.
        """
        # register the shortcut
        callback = callback if not can_toggle else self._toggle(name, callback)
        reg_dict = self._callback_registry.get(key, {})
        reg_dict[name] = callback
        self._callback_registry[key] = reg_dict

        if not silent:
            # add the shortcut text and callback
            shortcut = Text(self._surface, title, 0, 0,
                            SHORTCUT_TEXT_COLOR, self._font_entry)
            self._window.add_sprite(name, shortcut)
            self._entries[name] = (len(self._entries) + 1, shortcut, key)

            # calculate start display height of shortcut section
            self._update_positions()

    def remove_shortcut(self, name: str) -> None:
        """Removes a registered shortcut based on the given name.

        Args:
            name (str): The shortcut to remove.
        """
        num, _, key = self._entries[name]
        self._toggled.pop(num - 1)

        del self._entries[name]
        del self._callback_registry[key][name]

    def untoggle_all(self) -> None:
        """Untoggles all shortcuts which can be toggled.
        """
        for name in self._toggled:
            self._entries[name][1].set_color(SHORTCUT_TEXT_COLOR)

        self._toggled = []

    def _toggle(self, name: str, func) -> None:
        def toggle_text():
            _, entry, _ = self._entries[name]
            if name not in self._toggled:
                self._toggled.append(name)
                entry.set_color(SHORTCUT_TEXT_COLOR_ACTIVE)
            else:
                self._toggled.remove(name)
                entry.set_color(SHORTCUT_TEXT_COLOR)

            func()

        return toggle_text

    def from_dict(self, d: Dict) -> None:
        print("Shortcut controller can not be set. Use managing controller class.")

    def to_dict(self) -> Dict:
        print("Shortcut controller can not be exported. Use managing controller class.")

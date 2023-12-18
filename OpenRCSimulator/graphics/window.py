from multiprocessing import Lock
from typing import List, Tuple, Any
import pygame as py
from OpenRCSimulator.graphics.callback import BaseListener, KeyListener, MouseListener, TextListener, WindowListener
from OpenRCSimulator.graphics.objects.sprite import Sprite
from OpenRCSimulator.graphics.font import FontWrapper


MUTEX = Lock()


class BaseWindow:
    """This class structurizes a game and the corresponding GUI for 
    it. The main loop will block the main thread, so be sure to 
    specify all callbacks before.

    Args:
        window_size (Tuple[int, int]): The size of the window in pixels (width, height)
        draw_area (Tuple[int, int], optional): The area in which sprites are drawn. Defaults to None.
        frame_rate (int, optional): The framerate at which the scene is rendered. Defaults to 60.
        flags (int, optional): Flags like fullscreen or hardware acceleration. Defaults to 0.
    """

    def __init__(self, window_size: Tuple[int, int], draw_area: Tuple[int, int] = None,
                 title: str = "", frame_rate: int = 60, flags: int = 0) -> None:
        py.init()
        py.font.init()

        # set the screen size and draw area
        self._width, self._height = self._window_size = window_size
        self._draw_area = draw_area
        if not self._draw_area:
            self._draw_area = self._window_size

        # define the screen on which all sprites are rendered
        self._flags = flags  # py.FULLSCREEN | py.HWSURFACE | py.DOUBLEBUF# | py.SCALED
        self._screen = py.display.set_mode(self._window_size, self._flags)
        py.display.set_caption(title)
        self._font = FontWrapper(name="dejavusansmono", size=14)

        # define a clock to limit the frames per second
        self._clock = py.time.Clock()
        self._frame_rate = frame_rate

        # set up everything else
        self._running = False
        self._callbacks: List[Tuple[Any, BaseListener]] = []
        self._text_input = False
        self._text_cache = ""
        self._mous_pos = py.mouse.get_pos()

        # sprite containers
        self._sprites = {}
        self._sprite_list = []

    def set_title(self, title: str) -> None:
        """Sets the window's title

        Args:
            title (str): The window title.
        """
        py.display.set_caption(title)

    def toggle_text_capture(self, overwrite: bool = None) -> None:
        """Reads keyboard inputs to cache which can be received by utilizing a 
        callback e.g. TEXT_INPUT. Caution: this may 
        prevent shortcuts to work.
        """
        self._text_cache = ""

        if overwrite is None:
            self._text_input = not self._text_input
        else:
            self._text_input = overwrite

    def get_surface(self) -> py.Surface:
        """Returns the surface which is used to create sprites.

        Returns:
            py.Surface: The pygames surface of this window.
        """
        return self._screen

    def get_window_size(self) -> Tuple[int, int]:
        """The window's size.

        Returns:
            Tuple[int, int]: width and height in pixels.
        """
        return self._window_size

    def get_flags(self):
        return self._flags

    def get_font(self) -> FontWrapper:
        """Returns font name and font size.

        Returns:
            Font: Font name and size.
        """
        return self._font

    @property
    def frame_rate(self) -> int:
        return self._frame_rate

    @frame_rate.setter
    def frame_rate(self, frame_rate) -> None:
        if frame_rate < 1 or frame_rate > 60:
            raise ValueError("The frame rate has to be between 1 and 60.")
        self._frame_rate = frame_rate

    def add_sprite(self, name: str, sprite: Sprite, zindex: int = 0) -> None:
        """This method adds a sprite to the window. For easier handling, give a
        name to the sprite.

        Args:
            name (str): Name of the sprite.
            sprite (Sprite): The sprite object.
            zindex (int, optional): Layering the sprites (higher values = send to
            back). Defaults to 0.
        """
        self._sprites[name] = (zindex, sprite)

        # convert to list and sort
        self._update_sprite_list()

    def remove_sprite(self, name: str) -> None:
        """This method removes a registered sprite based on the name.

        Args:
            name (str): The name of the sprite to remove.
        """
        self._sprites.pop(name, "")

        # convert to list and sort
        self._update_sprite_list()

    def _update_sprite_list(self) -> None:
        # the sprite list is used to sort sprites corresponding to their
        # zindex value.
        def comp(sprite): return sprite[0]
        self._sprite_list = list(self._sprites.values())
        self._sprite_list.sort(key=comp, reverse=True)

    def set_listener(self, listener: BaseListener, object: Any = None) -> None:
        """
        Using this method, callbacks can be registered. If the 
        defined event occurs, then the given function is executed.
        """
        self._callbacks.append((object, listener))

    def remove_listener(self, listener: BaseListener, object: Any = None) -> None:
        """
        This method removes a registered callback
        """
        if len(self._callbacks) != 0:
            if object:
                for i, (registered_object, _) in enumerate(self._callbacks):
                    if object == registered_object:
                        self._callbacks.pop(i)
                        break
                return

            for i, (_, registered_listener) in enumerate(self._callbacks):
                if listener == registered_listener:
                    self._callbacks.pop(i)
                    break

    def _get_listeners(self, listener: object) -> List[str]:
        return [c.__name__ for c in listener.__class__.__bases__]

    def start(self) -> None:
        """
        This method holds the main loop that updates the GUI. Be 
        aware that this blocks the main thread.
        """
        self._running = True
        while self._running:
            for event in py.event.get():
                self.event(event)

            # draw all registered sprites first
            for _, sprite in self._sprite_list:
                sprite.draw()

            self.draw()

            # cap at the given frame rate
            self._clock.tick(self._frame_rate)
            py.display.flip()

        print("Graphics has stopped.")

    def event(self, event) -> None:
        """
        This method is used to handle GUI events.
        """
        if event.type == py.QUIT:
            self._running = False

            for object, callback in self._callbacks:
                if WindowListener.__name__ in self._get_listeners(callback):
                    callback.on_quit()

        # keyboard input
        if event.type == py.KEYDOWN:
            # text input enabled, ignoring shortcuts
            if self._text_input:
                if event.key == py.K_ESCAPE or event.key == py.K_RETURN:
                    self._text_input = False
                    for object, callback in self._callbacks:
                        if TextListener.__name__ in self._get_listeners(callback):
                            callback.on_text_end(object)
                    self._text_cache = ""
                else:
                    self._text_cache += event.unicode
                    if event.key == py.K_BACKSPACE:
                        self._text_cache = self._text_cache[:-2]

                    for object, callback in self._callbacks:
                        if TextListener.__name__ in self._get_listeners(callback):
                            callback.on_text_changed(object, self._text_cache)

            else:
                # execute a key pressed callback, the name has to be the key name
                for object, callback in self._callbacks:
                    if KeyListener.__name__ in self._get_listeners(callback):
                        callback.on_key_pressed(event.key)

        # mouse input
        mouse_pos = py.mouse.get_pos()
        mouse_buttons = py.mouse.get_pressed()

        if True in mouse_buttons:
            for object, callback in self._callbacks:
                if MouseListener.__name__ in self._get_listeners(callback):
                    callback.on_click(mouse_buttons, mouse_pos)

        if mouse_pos != self._mous_pos:
            delta = (self._mous_pos[0] - mouse_pos[0],
                     self._mous_pos[1] - mouse_pos[1])
            self._mous_pos = mouse_pos
            for object, callback in self._callbacks:
                if MouseListener.__name__ in self._get_listeners(callback):
                    callback.on_movement(self._mous_pos, delta)

    def draw(self) -> None:
        """
        This method can be used to draw elements on the GUI.
        """
        raise NotImplementedError

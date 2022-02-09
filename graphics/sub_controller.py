from typing import Dict


class BaseSubController:
    def __init__(self) -> None:
        self._toggle_callback = False
        self._toggled = False

    def is_toggled(self) -> bool:
        return self._toggled

    def on_toggle(self, func) -> None:
        self._toggle_callback = func
    
    def toggle(self, call: bool = True) -> None:
        self._toggled = not self._toggled
        
        if self._toggle_callback and call:
            self._toggle_callback(self)
    
    def dict(self) -> Dict:
        raise NotImplementedError
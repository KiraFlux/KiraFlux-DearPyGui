from abc import ABC
from dataclasses import dataclass
from dataclasses import field
from typing import Optional
from typing import final

from dearpygui import dearpygui as dpg

from kf_dpg.abc.entities import Item

DpgTag = int | str


@dataclass
class DpgItem(Item[DpgTag], ABC):
    _tag: Optional[DpgTag] = field(init=False, default=None)

    def update(self) -> None:
        """Обновить компонент"""

    def _onRegister(self, tag: DpgTag) -> None:
        # if self.isRegistered():
        #     raise ValueError(f"re registering not allowed: {tag} (exist: {self.tag()}")

        self._tag = tag
        self.update()

    @final
    def tag(self) -> Optional[DpgTag]:
        return self._tag

    @final
    def configure(self, **kwargs) -> None:
        """Настроить"""
        dpg.configure_item(self.tag(), **kwargs)

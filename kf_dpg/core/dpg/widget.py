from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from dataclasses import field
from typing import Optional
from typing import final

from dearpygui import dearpygui as dpg

from kf_dpg.abc.entities import Font
from kf_dpg.abc.entities import Widget
from kf_dpg.core.dpg.item import DpgTag
from kf_dpg.core.dpg.traits import DpgDeletable
from kf_dpg.core.dpg.traits import DpgVisibility


@dataclass
class DpgWidget(Widget[DpgTag], DpgDeletable, DpgVisibility, ABC):
    """Виджет системы DPG"""

    __font: Optional[Font] = field(init=False, default=None)
    """Шрифт"""

    def _onRegister(self, tag: DpgTag) -> None:
        super()._onRegister(tag)
        self._updateVisibility()

        if self.__font is not None:
            self._updateFont()

    @final
    def setFont(self, font: Font[DpgTag]) -> None:
        self.__font = font

        if self.isRegistered():
            self._updateFont()

    def _updateFont(self):
        if self.__font:
            dpg.bind_item_font(self.tag(), self.__font.tag())

    @final
    def register(self, parent: Widget[DpgTag]) -> None:
        """Зарегистрировать виджет"""
        self._onRegister(self._createTag(parent.tag()))

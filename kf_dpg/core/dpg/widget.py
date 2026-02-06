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

    def _on_register(self, tag: DpgTag) -> None:
        super()._on_register(tag)
        self._update_visibility()

        if self.__font is not None:
            self._update_font()

    @final
    def set_font(self, font: Font[DpgTag]) -> None:
        self.__font = font

        if self.is_registered():
            self._update_font()

    def _update_font(self):
        if self.__font:
            dpg.bind_item_font(self.tag(), self.__font.tag())

    @final
    def register(self, parent: Widget[DpgTag]) -> None:
        """Зарегистрировать виджет"""
        self._on_register(self._create_tag(parent.tag()))

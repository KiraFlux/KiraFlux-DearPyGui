from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar
from typing import MutableSequence
from typing import final

from dearpygui import dearpygui as dpg

from kf_dpg.abc.entities import Font
from kf_dpg.core.dpg.item import DpgItem
from kf_dpg.core.dpg.item import DpgTag


@dataclass
class DpgFont(DpgItem, Font[DpgTag]):
    _fonts: ClassVar[MutableSequence[DpgFont]] = list()
    """Загруженные шрифты"""

    _source: Path
    """Файл шрифта"""

    _size: int
    """Размер шрифта в пикселях"""

    _smooth: bool = True
    """Сглаживание шрифта"""

    def __post_init__(self) -> None:
        self._fonts.append(self)

    @final
    def sub(self, *, size: int) -> DpgFont:
        """Создать подтип шрифта"""
        return DpgFont(
            self._source,
            size,
            self._smooth
        )

    @classmethod
    def load(cls) -> None:
        """Загрузить все шрифты"""
        with dpg.font_registry():
            for font in cls._fonts:
                font._register()

    @final
    def _register(self) -> None:
        self._tag = dpg.add_font(
            file=str(self._source),
            size=self._size,
            pixel_snapH=not self._smooth
        )
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default, parent=self._tag)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic, parent=self._tag)

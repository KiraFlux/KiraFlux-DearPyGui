from __future__ import annotations

from dataclasses import dataclass
from typing import final

from dearpygui import dearpygui as dpg

from kf_dpg.core.dpg.item import DpgTag
from kf_dpg.core.dpg.traits import DpgColored
from kf_dpg.core.dpg.traits import DpgValued
from kf_dpg.core.dpg.widget import DpgWidget
from rs.misc.color import Color


@final
@dataclass
class _Text(DpgWidget, DpgValued[str], DpgColored):
    """Текст"""

    _bullet: bool = False
    """Отображает маркер перед текстом"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_text(
            self._value,
            parent=parent_tag,
            bullet=self._bullet
        )


def Text(
        default: str = None,
        *,
        color: Color = Color.white(),
        bullet: bool = False
):
    """Текст"""
    return _Text(_bullet=bullet, _value=default, _color=color)

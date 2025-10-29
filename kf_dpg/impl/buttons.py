from dataclasses import dataclass
from dataclasses import field
from typing import final

from dearpygui import dearpygui as dpg

from kf_dpg.core.dpg.item import DpgTag
from kf_dpg.core.dpg.traits import DpgColored
from kf_dpg.core.dpg.traits import DpgLabeled
from kf_dpg.core.dpg.traits import DpgSimpleHandlerable
from kf_dpg.core.dpg.traits import DpgSizable
from kf_dpg.core.dpg.traits import DpgValueHandlerable
from kf_dpg.core.dpg.widget import DpgWidget


@final
@dataclass
class Button(DpgWidget, DpgSizable[int], DpgSimpleHandlerable, DpgLabeled):
    """Dpg: button"""

    _small: bool = field(kw_only=True, default=False)
    """Меньший размер кнопки"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_button(

            parent=parent_tag,

            small=self._small,
        )


@final
@dataclass
class ColorDisplay(DpgWidget, DpgSizable, DpgColored, DpgLabeled):
    """Кнопка"""

    _border: bool = field(kw_only=True, default=False)

    def _updateColor(self):
        self.configure(default_value=self._color.toRGBA8888())

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_color_button(
            parent=parent_tag,

            no_border=not self._border,
        )


@final
@dataclass
class CheckBox(DpgWidget, DpgValueHandlerable[bool], DpgLabeled):
    """Dpg: checkbox"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_checkbox(
            parent=parent_tag,
        )

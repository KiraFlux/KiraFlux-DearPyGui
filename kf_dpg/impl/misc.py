from dataclasses import dataclass
from typing import final

import dearpygui.dearpygui as dpg

from kf_dpg.core.dpg.item import DpgTag
from kf_dpg.core.dpg.traits import DpgSizable
from kf_dpg.core.dpg.widget import DpgWidget


@final
class Separator(DpgWidget):
    """Dpg: separator"""

    def _create_tag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_separator(
            parent=parent_tag,
        )


@final
@dataclass(kw_only=True)
class Spacer(DpgWidget, DpgSizable):
    """Dpg spacer"""

    def _create_tag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_spacer(
            parent=parent_tag,
        )

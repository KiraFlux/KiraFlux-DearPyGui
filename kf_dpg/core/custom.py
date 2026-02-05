from typing import Any
from typing import Callable
from typing import Optional

from kf_dpg.abc.entities import Font
from kf_dpg.abc.entities import Widget
from kf_dpg.abc.traits import Deletable
from kf_dpg.abc.traits import Visibility
from kf_dpg.core.dpg.item import DpgTag
from kf_dpg.core.dpg.widget import DpgWidget


class CustomWidget(Widget[DpgWidget], Deletable, Visibility):
    """Пользовательский виджет"""

    def __init__(self, base: DpgWidget) -> None:
        self.__base = base

    def detach_delete_observer(self, f: Callable[[Deletable], Any]) -> None:
        self.__base.detach_delete_observer(f)

    def attach_delete_observer(self, f: Callable[[Deletable], Any]) -> None:
        self.__base.attach_delete_observer(f)

    def is_visible(self) -> bool:
        return self.__base.is_visible()

    def set_visibility(self, is_visible: bool) -> None:
        self.__base.set_visibility(is_visible)

    def register(self, parent: Widget[DpgWidget]) -> None:
        self.__base.register(parent)

    def tag(self) -> Optional[DpgTag]:
        return self.__base.tag()

    def set_font(self, font: Font) -> None:
        self.__base.set_font(font)

    def _create_tag(self, parent_tag: DpgTag) -> DpgTag:
        return self.__base._create_tag(parent_tag)

    def delete(self) -> None:
        self.__base.delete()

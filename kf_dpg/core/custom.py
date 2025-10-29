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

    def detachDeleteObserver(self, f: Callable[[Deletable], Any]) -> None:
        self.__base.detachDeleteObserver(f)

    def attachDeleteObserver(self, f: Callable[[Deletable], Any]) -> None:
        self.__base.attachDeleteObserver(f)

    def isVisible(self) -> bool:
        return self.__base.isVisible()

    def setVisibility(self, is_visible: bool) -> None:
        self.__base.setVisibility(is_visible)

    def register(self, parent: Widget[DpgWidget]) -> None:
        self.__base.register(parent)

    def tag(self) -> Optional[DpgTag]:
        return self.__base.tag()

    def setFont(self, font: Font) -> None:
        self.__base.setFont(font)

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return self.__base._createTag(parent_tag)

    def delete(self) -> None:
        self.__base.delete()

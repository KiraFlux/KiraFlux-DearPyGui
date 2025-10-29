from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from dataclasses import field
from typing import Callable
from typing import ClassVar
from typing import Iterable
from typing import MutableSequence
from typing import Optional
from typing import final

from dearpygui import dearpygui as dpg

from kf_dpg.abc.entities import Widget
from kf_dpg.core.dpg.container import DpgContainer
from kf_dpg.core.dpg.item import DpgTag
from kf_dpg.core.dpg.traits import DpgLabeled
from kf_dpg.core.dpg.traits import DpgSizable
from kf_dpg.core.dpg.traits import DpgToggleable
from kf_dpg.core.dpg.traits import DpgValueHandlerable
from kf_dpg.core.dpg.traits import DpgWidthAdjustable
from kf_dpg.core.dpg.widget import DpgWidget


@dataclass
class _DpgWidgetContainer(DpgContainer[Widget[DpgTag]], ABC):

    @final
    def _registerItem(self, item: Widget[DpgTag]) -> None:
        item.register(self)


@final
@dataclass(kw_only=True)
class _Box(_DpgWidgetContainer, DpgSizable[int]):
    """Dpg: group"""

    _is_horizontal: bool

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_group(
            parent=parent_tag,
            horizontal=self._is_horizontal
        )


def VBox() -> _Box:
    """Вертикальный контейнер"""
    return _Box(_is_horizontal=False)


def HBox() -> _Box:
    """Горизонтальный контейнер"""
    return _Box(_is_horizontal=True)


@final
@dataclass
class Details(_DpgWidgetContainer, DpgLabeled):
    """Dpg: collapsing_header"""

    _default_open: bool = False
    """Открыт по умолчанию"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_collapsing_header(
            parent=parent_tag,
            default_open=self._default_open
        )


@dataclass(kw_only=True)
class ComboBox[T](DpgWidget, DpgLabeled, DpgWidthAdjustable[int], DpgToggleable, DpgValueHandlerable[T]):
    """Dpg: combo_box"""

    # todo подчистить нейрошизу

    _items_provider: Callable[[], Iterable[T]]
    _items_cache: dict[str, T] = field(init=False, default_factory=dict)
    _current_value: Optional[T] = None

    def _updateItems(self) -> None:
        current_str = dpg.get_value(self.tag()) if self.isRegistered() else None

        self._items_cache = {
            str(item): item for item in self._items_provider()
        }

        self.configure(items=sorted(self._items_cache.keys()))

        if current_str and current_str in self._items_cache:
            dpg.set_value(self.tag(), current_str)

    def _getValue(self) -> T:
        if not self.isRegistered():
            return self._current_value

        selected_str = dpg.get_value(self.tag())

        return self._items_cache.get(selected_str, self._current_value)

    # noinspection PyFinal
    def setValue(self, value: T) -> None:
        self._current_value = value
        if not self.isRegistered():
            return

        # Находим строковое представление для объекта
        for s, item in self._items_cache.items():
            if item == value:
                dpg.set_value(self.tag(), s)
                return

        # Если не нашли, устанавливаем первое значение
        if self._items_cache:
            first_key = next(iter(self._items_cache.keys()))
            dpg.set_value(self.tag(), first_key)

    def _updateValue(self) -> None:
        """Синхронизация при изменении значения в DPG"""
        if self.isRegistered():
            selected_str = dpg.get_value(self.tag())
            self._current_value = self._items_cache.get(selected_str)

    def update(self) -> None:
        super().update()
        self._updateItems()

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        tag = dpg.add_combo(parent=parent_tag)

        # Обработчик изменений в реальном времени
        dpg.set_item_callback(tag, self._updateValue)
        return tag


@final
@dataclass
class Tab(_DpgWidgetContainer, DpgLabeled):
    """Dpg: tab"""

    _label: str
    """Наименование вкладки"""

    _closable: bool = False
    """Вкладка может быть закрыта"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_tab(
            parent=parent_tag,
            closable=self._closable,
        )


@final
@dataclass
class TabBar(DpgContainer[Tab]):
    """Dpg: tab_bar"""

    _reorderable: bool = False
    """Поддерживает перемещение вкладок"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_tab_bar(
            parent=parent_tag,
            reorderable=self._reorderable
        )

    def _registerItem(self, item: Tab) -> None:
        item.register(self)


@final
@dataclass
class Window(_DpgWidgetContainer, DpgSizable[int], DpgLabeled):
    """Dpg: window"""

    _windows: ClassVar[MutableSequence[Window]] = list()
    """Экземпляры окон"""

    _menubar: bool = False
    """Место под полосу меню"""
    _auto_size: bool = True
    """Размер окна автоматически подстраивается под виджеты"""
    _modal: bool = False
    """Является модальным окном"""

    def __post_init__(self):
        self.__class__._windows.append(self)

    @classmethod
    def registerAll(cls) -> None:
        """Регистрация всех окон"""
        for w in cls._windows:
            # noinspection PyTypeChecker
            w.register(None)

    # noinspection PyFinal
    def register(self, parent: Widget) -> None:
        self._onRegister(dpg.add_window(
            menubar=self._menubar,
            autosize=self._auto_size,
            modal=self._modal,
        ))

    def update(self) -> None:
        super().update()
        if self._modal:
            self.hide()

    def _createTag(self, parent_tag):
        raise RuntimeError


@final
@dataclass(kw_only=True)
class ChildWindow(_DpgWidgetContainer, DpgSizable[int]):
    """Дочернее очно"""

    resizable_x: bool = False
    resizable_y: bool = False

    auto_size_x: bool = False
    auto_size_y: bool = False

    border: bool = True

    # Внешний вид
    background: bool = False
    menu_bar: bool = False
    scrollable_y: bool = False
    scrollable_x: bool = False

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_child_window(
            parent=parent_tag,
            border=self.border,
            frame_style=self.background,
            menubar=self.menu_bar,
            resizable_x=self.resizable_x,
            resizable_y=self.resizable_y,
            no_scrollbar=not self.scrollable_y,
            horizontal_scrollbar=self.scrollable_x,
            autosize_x=self.auto_size_x,
            autosize_y=self.auto_size_y,
            no_scroll_with_mouse=not self.scrollable_y,
        )

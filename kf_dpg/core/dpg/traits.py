from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, ClassVar
from typing import Optional, final

from dearpygui import dearpygui as dpg

from kf_dpg.abc.traits import Colored, Deletable, Handlerable, HeightAdjustable, Intervaled, Labeled, Sizable, \
    Toggleable, Valued, Visibility, WidthAdjustable, Themeable
from kf_dpg.core.dpg.item import DpgItem, DpgTag
from kf_dpg.misc.color import Color
from kf_dpg.misc.subject import Subject


@dataclass(kw_only=True)
class DpgLabeled(DpgItem, Labeled):
    """Объект Dpg имеющий метку (label)"""

    _label: Optional[str] = None

    @final
    def get_label(self) -> Optional[str]:
        if self.is_registered():
            self._label = dpg.get_item_label(self.tag())

        return self._label

    @final
    def set_label(self, label: Optional[str]) -> None:
        self._label = label

        if self.is_registered():
            self._updateLabel()

    def _updateLabel(self) -> None:
        dpg.set_item_label(self.tag(), self._label)

    def update(self) -> None:
        super().update()
        self._updateLabel()


@dataclass(kw_only=True)
class DpgColored(DpgItem, Colored):
    _color: Color
    """Цвет"""

    def _update_color(self):
        self.configure(color=self._color.to_rgba8888())

    def update(self) -> None:
        super().update()
        self._update_color()

    @final
    def get_color(self) -> Color:
        return self._color

    @final
    def set_color(self, color: Color) -> None:
        self._color = color

        if self.is_registered():
            self._update_color()


@dataclass(kw_only=True)
class DpgToggleable(DpgItem, Toggleable):
    _enabled: bool = True
    """Объект включен"""

    def _updateEnabled(self) -> None:
        if self._enabled:
            dpg.enable_item(self.tag())
        else:
            dpg.disable_item(self.tag())

    def update(self) -> None:
        super().update()
        self._updateEnabled()

    @final
    def is_enabled(self) -> bool:
        if self.is_registered():
            self._enabled = dpg.is_item_enabled(self.tag())

        return self._enabled

    @final
    def set_enabled(self, enabled: bool) -> None:
        self._enabled = enabled

        if self.is_registered():
            self._updateEnabled()


@dataclass
class DpgDeletable(DpgItem, Deletable):
    _delete_subject: Subject[Deletable] = field(init=False, default_factory=Subject)

    def attach_delete_observer(self, f: Callable[[Deletable], Any]) -> None:
        self._delete_subject.add_listener(f)

    def detach_delete_observer(self, f: Callable[[Deletable], Any]) -> None:
        self._delete_subject.remove_listener(f)

    def delete(self) -> None:
        self._delete_subject.notify(self)
        dpg.delete_item(self.tag())


@dataclass(kw_only=True)
class DpgVisibility(DpgItem, Visibility):
    _visible: bool = True
    """Объект видимый"""

    def _update_visibility(self) -> None:
        if self._visible:
            dpg.show_item(self.tag())
        else:
            dpg.hide_item(self.tag())

    def update(self) -> None:
        super().update()
        self._update_visibility()

    @final
    def is_visible(self) -> bool:
        if self.is_registered():
            self._visible = dpg.is_item_visible(self.tag())

        return self._visible

    @final
    def set_visibility(self, is_visible: bool) -> None:
        self._visible = is_visible

        if self.is_registered():
            self._update_visibility()


@dataclass(kw_only=True)
class DpgValued[T](DpgItem, Valued[T], ABC):
    """Виджет со значением на стороне DPG"""

    _value: T
    """Значение по умолчанию"""

    def _update_value(self):
        dpg.set_value(self.tag(), self._value)

    def _get_value(self) -> T:
        return dpg.get_value(self.tag())

    def update(self) -> None:
        super().update()
        self._update_value()

    @final
    def get_value(self) -> T:
        if self.is_registered():
            self._value = self._get_value()

        return self._value

    @final
    def set_value(self, value: T) -> None:
        self._value = value

        if self.is_registered():
            self._update_value()


@dataclass(kw_only=True)
class DpgIntervaled[T](DpgItem, Intervaled[T]):
    """Виджет DPG имеющий диапазон и значение"""

    _interval_max: Optional[T]
    """Максимальное допустимое значение"""

    _interval_min: Optional[T]
    """Минимальное допустимое значение"""

    def _update_interval_max(self) -> None:
        if self._interval_max:
            self.configure(max_value=self._interval_max)

    def _update_interval_min(self) -> None:
        if self._interval_min:
            self.configure(min_value=self._interval_min)

    def update(self) -> None:
        super().update()
        self._update_interval_min()
        self._update_interval_max()

    @final
    def set_interval_max(self, new_max: T) -> None:
        self._interval_max = new_max

        if self.is_registered():
            self._update_interval_max()

    @final
    def set_interval_min(self, new_min: T) -> None:
        self._interval_min = new_min

        if self.is_registered():
            self._update_interval_min()

    @final
    def get_interval_max(self) -> T:
        return self._interval_max

    @final
    def get_interval_min(self) -> T:
        return self._interval_min


@dataclass(kw_only=True)
class DpgHasThickness[T](DpgItem):
    """Поддерживает толщину"""

    _thickness: T = 2

    @final
    def set_thickness(self, thickness: float) -> None:
        self._thickness = thickness
        self._update_thickness()

    def _update_thickness(self):
        if self.is_registered():
            dpg.configure_item(self.tag(), thickness=self._thickness)

    @final
    def get_thickness(self) -> float:
        return self._thickness

    @final
    def with_thickness(self, thickness: float):
        self.set_thickness(thickness)
        return self

    def update(self) -> None:
        super().update()
        self._update_thickness()


@dataclass(kw_only=True)
class _DpgHandlerable[F: Callable](DpgItem, Handlerable[F], ABC):
    _callback: Optional[F] = None
    """Обработчик обратного вызова"""

    @abstractmethod
    def _create_callback_wrapper(self) -> Callable[[Any], Any]:
        """Создать обёртку для передачи в DPG"""

    @final
    def set_handler(self, f: F) -> None:
        self._callback = f

        if self.is_registered():
            self._update_callback()

    def _update_callback(self) -> None:
        self.configure(
            callback=(
                None
                if self._callback is None else
                self._create_callback_wrapper()
            )
        )

    def update(self) -> None:
        super().update()
        self._update_callback()


class DpgValueHandlerable[T](DpgValued[T], _DpgHandlerable[Callable[[T], Any]]):
    """Объект DPG поддерживающий обратный вызов со значением"""

    def _create_callback_wrapper(self) -> Callable[[Any], Any]:
        return lambda _: self._callback(self.get_value())


class DpgSimpleHandlerable(_DpgHandlerable[Callable[[], Any]]):
    """Объект DPG поддерживающий обратный вызов"""

    def _create_callback_wrapper(self) -> Callable[[Any], Any]:
        return lambda _: self._callback()


@dataclass(kw_only=True)
class DpgWidthAdjustable[T: (int, float)](DpgItem, WidthAdjustable[T]):
    """Объект DPG способный управлять шириной"""

    _width: T = 0
    """Изначальная ширина"""

    @final
    def set_width(self, width: T) -> None:
        self._width = width

        if self.is_registered():
            self._update_width()

    @final
    def get_width(self) -> T:
        if self.is_registered():
            self._width = dpg.get_item_width(self.tag())

        return self._width

    def _update_width(self) -> None:
        self.configure(width=self._width)

    def update(self) -> None:
        super().update()
        self._update_width()


@dataclass(kw_only=True)
class DpgHeightAdjustable[T: (int, float)](DpgItem, HeightAdjustable):
    _height_key: ClassVar[str] = 'height'

    _height: T = 0
    """Изначальная высота"""

    def _update_height(self):
        self.configure(**{
            self._height_key: self._height
        })

    def update(self) -> None:
        super().update()
        self._update_height()

    @final
    def get_height(self) -> T:
        if self.is_registered():
            self._height = dpg.get_item_height(self.tag())

        return self._height

    @final
    def set_height(self, height: T) -> None:
        self._height = height

        if self.is_registered():
            self._update_height()


@dataclass(kw_only=True)
class DpgSizable[T: (int, float)](DpgWidthAdjustable[T], DpgHeightAdjustable[T], Sizable[T], DpgItem):
    """Виджет DPG имеющий размеры"""


@dataclass(kw_only=True)
class DpgThemeable(DpgItem, Themeable, ABC):
    """Реализация Themeable для DPG элементов"""

    _theme_tag: Optional[DpgTag] = field(init=False, default=None)
    _color: Color = field(default_factory=Color.white)

    @final
    def get_color(self) -> Color:
        return self._color

    @final
    def set_color(self, color: Color) -> None:
        self._color = color
        self._update_theme()

    def _update_theme(self) -> None:
        """Обновить или создать тему с цветом"""
        if not self.is_registered():
            return

        component = self._get_theme_component()
        color_target = self._get_color_target()
        category = self._get_color_category()

        if self._theme_tag is None:
            # Создаём новую тему
            with dpg.theme() as theme_id:
                with dpg.theme_component(component):
                    dpg.add_theme_color(color_target, self._color.to_rgba8888(), category=category)
            self._theme_tag = theme_id
        else:
            # Находим и обновляем компонент цвета
            theme_components = dpg.get_item_children(self._theme_tag, slot=1)
            if theme_components:
                color_items = dpg.get_item_children(theme_components[0], slot=1)
                if color_items:
                    dpg.set_value(color_items[0], self._color.to_rgba8888())

        dpg.bind_item_theme(self.tag(), self._theme_tag)

    def update(self) -> None:
        super().update()
        if self.is_registered():
            self._update_theme()

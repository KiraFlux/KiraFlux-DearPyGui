from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Callable
from typing import ClassVar
from typing import Optional
from typing import final

from dearpygui import dearpygui as dpg

from kf_dpg.abc.traits import Colored
from kf_dpg.abc.traits import Deletable
from kf_dpg.abc.traits import Handlerable
from kf_dpg.abc.traits import HeightAdjustable
from kf_dpg.abc.traits import Intervaled
from kf_dpg.abc.traits import Labeled
from kf_dpg.abc.traits import Sizable
from kf_dpg.abc.traits import Toggleable
from kf_dpg.abc.traits import Valued
from kf_dpg.abc.traits import Visibility
from kf_dpg.abc.traits import WidthAdjustable
from kf_dpg.core.dpg.item import DpgItem
from rs.misc.color import Color
from rs.misc.subject import Subject


@dataclass(kw_only=True)
class DpgLabeled(DpgItem, Labeled):
    """Объект Dpg имеющий метку (label)"""

    _label: Optional[str] = None

    @final
    def getLabel(self) -> Optional[str]:
        if self.isRegistered():
            self._label = dpg.get_item_label(self.tag())

        return self._label

    @final
    def setLabel(self, label: Optional[str]) -> None:
        self._label = label

        if self.isRegistered():
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

    def _updateColor(self):
        self.configure(color=self._color.toRGBA8888())

    def update(self) -> None:
        super().update()
        self._updateColor()

    @final
    def getColor(self) -> Color:
        return self._color

    @final
    def setColor(self, color: Color) -> None:
        self._color = color

        if self.isRegistered():
            self._updateColor()


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
    def isEnabled(self) -> bool:
        if self.isRegistered():
            self._enabled = dpg.is_item_enabled(self.tag())

        return self._enabled

    @final
    def setEnabled(self, enabled: bool) -> None:
        self._enabled = enabled

        if self.isRegistered():
            self._updateEnabled()


@dataclass
class DpgDeletable(DpgItem, Deletable):
    _delete_subject: Subject[Deletable] = field(init=False, default_factory=Subject)

    def attachDeleteObserver(self, f: Callable[[Deletable], Any]) -> None:
        self._delete_subject.addListener(f)

    def detachDeleteObserver(self, f: Callable[[Deletable], Any]) -> None:
        self._delete_subject.removeListener(f)

    def delete(self) -> None:
        self._delete_subject.notify(self)
        dpg.delete_item(self.tag())


@dataclass(kw_only=True)
class DpgVisibility(DpgItem, Visibility):
    _visible: bool = True
    """Объект видимый"""

    def _updateVisibility(self) -> None:
        if self._visible:
            dpg.show_item(self.tag())
        else:
            dpg.hide_item(self.tag())

    def update(self) -> None:
        super().update()
        self._updateVisibility()

    @final
    def isVisible(self) -> bool:
        if self.isRegistered():
            self._visible = dpg.is_item_visible(self.tag())

        return self._visible

    @final
    def setVisibility(self, is_visible: bool) -> None:
        self._visible = is_visible

        if self.isRegistered():
            self._updateVisibility()


@dataclass(kw_only=True)
class DpgValued[T](DpgItem, Valued[T], ABC):
    """Виджет со значением на стороне DPG"""

    _value: T
    """Значение по умолчанию"""

    def _updateValue(self):
        dpg.set_value(self.tag(), self._value)

    def _getValue(self) -> T:
        return dpg.get_value(self.tag())

    def update(self) -> None:
        super().update()
        self._updateValue()

    @final
    def getValue(self) -> T:
        if self.isRegistered():
            self._value = self._getValue()

        return self._value

    @final
    def setValue(self, value: T) -> None:
        self._value = value

        if self.isRegistered():
            self._updateValue()


@dataclass(kw_only=True)
class DpgIntervaled[T](DpgItem, Intervaled[T]):
    """Виджет DPG имеющий диапазон и значение"""

    _interval_max: Optional[T]
    """Максимальное допустимое значение"""

    _interval_min: Optional[T]
    """Минимальное допустимое значение"""

    def _updateIntervalMax(self) -> None:
        if self._interval_max:
            self.configure(max_value=self._interval_max)

    def _updateIntervalMin(self) -> None:
        if self._interval_min:
            self.configure(min_value=self._interval_min)

    def update(self) -> None:
        super().update()
        self._updateIntervalMin()
        self._updateIntervalMax()

    @final
    def setIntervalMax(self, new_max: T) -> None:
        self._interval_max = new_max

        if self.isRegistered():
            self._updateIntervalMax()

    @final
    def setIntervalMin(self, new_min: T) -> None:
        self._interval_min = new_min

        if self.isRegistered():
            self._updateIntervalMin()

    @final
    def getIntervalMax(self) -> T:
        return self._interval_max

    @final
    def getIntervalMin(self) -> T:
        return self._interval_min


@dataclass(kw_only=True)
class _DpgHandlerable[F: Callable](DpgItem, Handlerable[F], ABC):
    _callback: Optional[F] = None
    """Обработчик обратного вызова"""

    @abstractmethod
    def _createCallbackWrapper(self) -> Callable[[Any], Any]:
        """Создать обёртку для передачи в DPG"""

    @final
    def setHandler(self, f: F) -> None:
        self._callback = f

        if self.isRegistered():
            self._updateCallback()

    def _updateCallback(self) -> None:
        self.configure(
            callback=(
                None
                if self._callback is None else
                self._createCallbackWrapper()
            )
        )

    def update(self) -> None:
        super().update()
        self._updateCallback()


class DpgValueHandlerable[T](DpgValued[T], _DpgHandlerable[Callable[[T], Any]]):
    """Объект DPG поддерживающий обратный вызов со значением"""

    def _createCallbackWrapper(self) -> Callable[[Any], Any]:
        return lambda _: self._callback(self.getValue())


class DpgSimpleHandlerable(_DpgHandlerable[Callable[[], Any]]):
    """Объект DPG поддерживающий обратный вызов"""

    def _createCallbackWrapper(self) -> Callable[[Any], Any]:
        return lambda _: self._callback()


@dataclass(kw_only=True)
class DpgWidthAdjustable[T: (int, float)](DpgItem, WidthAdjustable[T]):
    """Объект DPG способный управлять шириной"""

    _width: T = 0
    """Изначальная ширина"""

    @final
    def setWidth(self, width: T) -> None:
        self._width = width

        if self.isRegistered():
            self._updateWidth()

    @final
    def getWidth(self) -> T:
        if self.isRegistered():
            self._width = dpg.get_item_width(self.tag())

        return self._width

    def _updateWidth(self) -> None:
        self.configure(width=self._width)

    def update(self) -> None:
        super().update()
        self._updateWidth()


@dataclass(kw_only=True)
class DpgHeightAdjustable[T: (int, float)](DpgItem, HeightAdjustable):
    _height_key: ClassVar[str] = 'height'

    _height: T = 0
    """Изначальная высота"""

    def _updateHeight(self):
        self.configure(**{
            self._height_key: self._height
        })

    def update(self) -> None:
        super().update()
        self._updateHeight()

    @final
    def getHeight(self) -> T:
        if self.isRegistered():
            self._height = dpg.get_item_height(self.tag())

        return self._height

    @final
    def setHeight(self, height: T) -> None:
        self._height = height

        if self.isRegistered():
            self._updateHeight()


@dataclass(kw_only=True)
class DpgSizable[T: (int, float)](DpgWidthAdjustable[T], DpgHeightAdjustable[T], Sizable[T], DpgItem):
    """Виджет DPG имеющий размеры"""

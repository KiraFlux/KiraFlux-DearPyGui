from abc import ABC
from dataclasses import dataclass
from typing import Optional
from typing import final

from dearpygui import dearpygui as dpg

from kf_dpg.core.dpg.item import DpgTag
from kf_dpg.core.dpg.traits import DpgIntervaled
from kf_dpg.core.dpg.traits import DpgValueHandlerable
from kf_dpg.core.dpg.traits import DpgWidthAdjustable
from kf_dpg.core.dpg.widget import DpgWidget


@dataclass(kw_only=True)
class _Slider[T](DpgWidget, DpgValueHandlerable[T], DpgIntervaled[T], DpgWidthAdjustable, ABC):
    """Общий слайдер"""

    _label: str
    """Описание"""

    _units: Optional[str]
    """Единицы измерения"""


@final
@dataclass
class _IntSlider(_Slider[int]):
    """Dpg: slider_int"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        f = "%d"

        if self._units:
            f = f"{f} {self._units}"

        return dpg.add_slider_int(
            parent=parent_tag,
            label=self._label,
            format=f
        )


def IntSlider(
        label: str,
        *,
        default: int = 0,
        units: str = None,
        interval: tuple[int, int],

):
    """Целочисленный слайдер"""
    _min, _max = interval
    return _IntSlider(
        _interval_max=_max,
        _interval_min=_min,
        _value=default,
        _label=label,
        _units=units,
    )


@final
@dataclass
class _FloatSlider(_Slider[float]):
    """Dpg: slider_float"""

    _digits_after_comma: int
    """Цифр после запятой"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        f = f"%.{self._digits_after_comma}f"

        if self._units:
            f = f"{f} {self._units}"

        return dpg.add_slider_float(
            parent=parent_tag,
            label=self._label,
            format=f,
        )


def FloatSlider(
        label: str,
        *,
        default: float = 0,
        units: str = None,
        interval: tuple[float, float],
        digits: int = 2,

):
    """Вещественный слайдер"""
    _min, _max = interval
    return _FloatSlider(
        _interval_max=_max,
        _interval_min=_min,
        _value=default,
        _label=label,
        _units=units,
        _digits_after_comma=digits
    )

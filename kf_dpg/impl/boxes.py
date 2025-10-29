from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import final

from dearpygui import dearpygui as dpg

from kf_dpg.core.dpg.item import DpgTag
from kf_dpg.core.dpg.traits import DpgIntervaled
from kf_dpg.core.dpg.traits import DpgLabeled
from kf_dpg.core.dpg.traits import DpgSizable
from kf_dpg.core.dpg.traits import DpgValueHandlerable
from kf_dpg.core.dpg.traits import DpgWidthAdjustable
from kf_dpg.core.dpg.widget import DpgWidget
from rs.misc.color import Color


@final
@dataclass(kw_only=True)
class ColorInput(DpgWidget, DpgValueHandlerable[Color], DpgLabeled, DpgSizable[int]):
    """Виджет выбора цвета с расширенными настройками"""

    _alpha: bool = False
    """Показывать альфа-канал"""

    _side_preview: bool = False
    """Показывать большой превью-бокс"""

    _small_preview: bool = True
    """Показывать маленькое превью"""

    _inputs: bool = True
    """Показывать поля ввода"""

    _tooltip: bool = True
    """Показывать подсказку"""

    def _updateValue(self) -> None:
        """Обновить значение в DPG"""
        dpg.set_value(self.tag(), self._value.toRGBA8888())

    def _getValue(self) -> Color:
        return Color.fromRGBA8888(*super()._getValue())

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        """Создать элемент DPG с учетом всех параметров"""
        return dpg.add_color_picker(
            parent=parent_tag,
            no_alpha=not self._alpha,
            no_side_preview=not self._side_preview,
            no_small_preview=not self._small_preview,
            no_inputs=not self._inputs,
            no_tooltip=not self._tooltip,
            no_label=self._label is None,
            alpha_bar=self._alpha,
            picker_mode=dpg.mvColorPicker_wheel,
            alpha_preview=dpg.mvColorEdit_AlphaPreviewHalf,
            display_type=dpg.mvColorEdit_float,
        )


@dataclass(kw_only=True)
class _ValueInput[T](DpgWidget, DpgValueHandlerable[T], DpgWidthAdjustable[int], DpgLabeled, ABC):
    """Окно значения"""

    _readonly: bool
    """Поле только для ввода"""

    _on_enter: bool
    """Засчитывать изменение по Enter"""


@final
@dataclass(kw_only=True)
class _TextInput(_ValueInput[str], DpgSizable[int]):
    """Окно текста"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_input_text(
            parent=parent_tag,
            readonly=self._readonly,
            on_enter=self._on_enter,
        )


def TextInput(
        *,
        default: str = None,
        on_enter: bool = False,
):
    """Создать окно ввода текста"""
    return _TextInput(
        _readonly=False,
        _on_enter=on_enter,
        _value=default,
    )


def TextDisplay(
        label: str,
        *,
        default: str = None,
):
    """Создать окно вывода текста"""
    return _TextInput(
        _readonly=True,
        _on_enter=False,
        _value=default,
    )


@final
@dataclass(kw_only=True)
class _IntInput(_ValueInput[int], DpgIntervaled[int]):
    """Окно целого числа"""

    _step: int

    _step_fast: int

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        clamped = (self._interval_min != self._interval_max)

        return dpg.add_input_int(
            parent=parent_tag,

            label=self._label,
            readonly=self._readonly,

            step_fast=self._step_fast,
            step=self._step,

            min_clamped=clamped,
            max_clamped=clamped,
        )


def IntInput(
        default: int = 0,
        *,
        step: int = 1,
        step_fast: int = 1,
        interval_min: int = 0,
        interval_max: int = 0,
        on_enter: bool = False,
):
    """Окно ввода целого числа"""
    return _IntInput(
        _interval_max=interval_max,
        _interval_min=interval_min,
        _value=default,
        _readonly=False,
        _on_enter=on_enter,
        _step=step,
        _step_fast=step_fast,
    )


def IntDisplay(
        *,
        default: int = 0,
):
    """Окно вывода целого числа"""
    return _IntInput(
        _interval_max=0,
        _interval_min=0,

        _value=default,
        _readonly=True,
        _on_enter=False,

        _step=0,
        _step_fast=0
    )

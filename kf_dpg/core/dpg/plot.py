from __future__ import annotations

from dataclasses import dataclass
from typing import final

import dearpygui.dearpygui as dpg

from kf_dpg.core.dpg.container import DpgContainer
from kf_dpg.core.dpg.item import DpgTag
from kf_dpg.core.dpg.traits import DpgColored, DpgLabeled, DpgSizable, DpgValueHandlerable, DpgValued, DpgHasThickness, \
    DpgDeletable, DpgVisibility, DpgThemeable
from kf_dpg.core.dpg.widget import DpgWidget
from kf_dpg.misc.color import Color
from kf_dpg.misc.vector import Vector2D


@final
@dataclass(kw_only=True)
class LineSeries(DpgWidget, DpgThemeable, DpgLabeled, DpgValued[tuple[list[float], list[float]]]):
    """Линейная серия данных"""

    _loop: bool = False

    @classmethod
    def make(cls):
        return cls(_value=(list(), list()))

    def set_loop(self, loop: bool):
        self._loop = loop
        self._update_loop()

    def update(self) -> None:
        super().update()
        self._update_loop()

    def _update_loop(self):
        if self.is_registered():
            self.configure(loop=self._loop)

    def _create_tag(self, parent_tag: DpgTag) -> DpgTag:
        x, y = self.get_value()
        return dpg.add_line_series(
            x, y,
            parent=parent_tag,
            loop=self._loop
        )

    def _get_theme_component(self) -> int:
        return dpg.mvLineSeries

    def _get_color_target(self) -> int:
        return dpg.mvPlotCol_Line

    def _get_color_category(self) -> int:
        return dpg.mvThemeCat_Plots


@final
@dataclass(kw_only=True)
class DragLine(DpgWidget, DpgColored, DpgLabeled, DpgValueHandlerable[float], DpgHasThickness[float], DpgDeletable,
               DpgVisibility):
    """Перетаскиваемая линия"""

    @classmethod
    def make(cls, *, is_vertical: bool, value: float = 0, color: Color = Color.white()):
        return DragLine(
            _value=value,
            _color=color,
            _vertical=is_vertical,
        )

    _vertical: bool

    def _create_tag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_drag_line(
            parent=parent_tag,
            vertical=self._vertical,
            delayed=True,
        )


@final
@dataclass(kw_only=True)
class DragPoint(DpgWidget, DpgColored, DpgLabeled, DpgValueHandlerable[Vector2D[float]], DpgDeletable, DpgVisibility):
    """Перетаскиваемая точка"""

    def _create_tag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_drag_point(
            parent=parent_tag,
            default_value=self._value.toTuple()
        )

    def _get_value(self) -> Vector2D[float]:
        x, y, *_ = super()._get_value()
        return Vector2D(x, y)

    def _update_value(self):
        if self.is_registered():
            v = self._value  # Vector2D
            dpg.set_value(self.tag(), (v.x, v.y))


@final
@dataclass(kw_only=True)
class _PlotAxis(DpgWidget, DpgLabeled, DpgDeletable):
    """Ось графика"""

    _axis_type: int

    def _create_tag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_plot_axis(self._axis_type, parent=parent_tag)


@final
@dataclass(kw_only=True)
class _Plot(DpgContainer, DpgSizable[int], DpgLabeled, DpgDeletable):
    """Декартов график"""

    _y_axis: _PlotAxis

    def _create_tag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_plot(
            parent=parent_tag,
            equal_aspects=True,
        )

    def _register_item(self, item: DpgDeletable) -> None:
        if isinstance(item, LineSeries):
            item.register(self._y_axis)
        elif isinstance(item, (DragLine, DragPoint, _PlotAxis)):
            item.register(self)
        else:
            raise TypeError(f"Неподдерживаемый элемент: {type(item)}")


def Plot() -> _Plot:
    plot = _Plot(_y_axis=_PlotAxis(_axis_type=dpg.mvYAxis).with_label("Y"))
    plot.add(_PlotAxis(_axis_type=dpg.mvXAxis).with_label("X"))
    plot.add(plot._y_axis)
    return plot

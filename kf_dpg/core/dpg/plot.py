from __future__ import annotations

from dataclasses import dataclass
from typing import final

import dearpygui.dearpygui as dpg

from kf_dpg.core.dpg.container import DpgContainer
from kf_dpg.core.dpg.item import DpgTag
from kf_dpg.core.dpg.traits import DpgColored, DpgLabeled, DpgSizable, DpgValueHandlerable, DpgValued, DpgHasThickness, DpgDeletable, DpgVisibility
from kf_dpg.core.dpg.widget import DpgWidget
from kf_dpg.misc.vector import Vector2D


@final
@dataclass(kw_only=True)
class LineSeries(DpgWidget, DpgColored, DpgLabeled, DpgValued[tuple[list[float], list[float]]], DpgHasThickness[float], DpgDeletable, DpgVisibility):
    """Линейная серия данных"""

    def _create_tag(self, parent_tag: DpgTag) -> DpgTag:
        x, y = self.get_value()
        return dpg.add_line_series(x, y, parent=parent_tag)


@final
@dataclass(kw_only=True)
class DragLine(DpgWidget, DpgColored, DpgLabeled, DpgValueHandlerable[float], DpgHasThickness[float], DpgDeletable, DpgVisibility):
    """Перетаскиваемая линия"""

    _vertical: bool

    def _create_tag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_drag_line(
            parent=parent_tag,
            vertical=self._vertical
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
            current = super()._get_value()  # (x, y, x_radius, y_radius)
            v = self._value  # Vector2D
            new_value = (v.x, v.y, current[2], current[3])
            dpg.set_value(self.tag(), new_value)


@final
@dataclass(kw_only=True)
class _PlotAxis(DpgWidget, DpgLabeled, DpgDeletable):
    """Ось графика"""

    _axis_type: int
    _min_limit: float = 0.0
    _max_limit: float = 1.0

    def set_limits(self, min_val: float, max_val: float) -> None:
        self._min_limit = min_val
        self._max_limit = max_val
        if self.is_registered():
            dpg.set_axis_limits(self.tag(), min_val, max_val)

    def get_limits(self) -> tuple[float, float]:
        if self.is_registered():
            _min, _max = dpg.get_axis_limits(self.tag())
            return _min, _max
        return self._min_limit, self._max_limit

    def _create_tag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_plot_axis(self._axis_type, parent=parent_tag)

    def update(self) -> None:
        super().update()
        if self.is_registered():
            dpg.set_axis_limits(self.tag(), self._min_limit, self._max_limit)


@final
@dataclass(kw_only=True)
class _Plot(DpgContainer, DpgSizable[int], DpgLabeled, DpgDeletable):
    """Декартов график"""

    _x_axis: _PlotAxis
    _y_axis: _PlotAxis

    def _create_tag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_plot(
            parent=parent_tag,
            equal_aspects=True,
        )

    def _register_item(self, item: DpgDeletable) -> None:
        if isinstance(item, LineSeries):
            item.register(self._y_axis)
        elif isinstance(item, (DragLine, DragPoint)):
            item.register(self)
        else:
            raise TypeError(f"Неподдерживаемый элемент: {type(item)}")


def Plot() -> _Plot:
    return _Plot(
        _x_axis=_PlotAxis(_axis_type=dpg.mvXAxis).with_label("X"),
        _y_axis=_PlotAxis(_axis_type=dpg.mvYAxis).with_label("Y"),
    )

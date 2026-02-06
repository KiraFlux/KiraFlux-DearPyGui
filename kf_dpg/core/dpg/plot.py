from __future__ import annotations

from dataclasses import dataclass
from typing import final

import dearpygui.dearpygui as dpg

from kf_dpg.core.dpg.container import DpgContainer
from kf_dpg.core.dpg.item import DpgTag
from kf_dpg.core.dpg.traits import DpgColored, DpgLabeled, DpgSizable, DpgValueHandlerable, DpgValued, DpgHasThickness
from kf_dpg.core.dpg.widget import DpgWidget


@final
@dataclass(kw_only=True)
class LineSeries(DpgWidget, DpgColored, DpgLabeled, DpgValued[tuple[list[float], list[float]]], DpgHasThickness[float]):
    """Линейная серия данных"""

    def _create_tag(self, parent_tag: DpgTag) -> DpgTag:
        x, y = self.get_value()
        return dpg.add_line_series(x, y, parent=parent_tag)


@final
@dataclass(kw_only=True)
class DragLine(DpgWidget, DpgColored, DpgLabeled, DpgValueHandlerable[float], DpgHasThickness[float]):
    """Перетаскиваемая линия"""

    _horizontal: bool

    def _create_tag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_drag_line(
            axis=dpg.mvXAxis if self._horizontal else dpg.mvYAxis,
            default_value=self._value,
            parent=parent_tag
        )


@final
@dataclass(kw_only=True)
class _PlotAxis(DpgWidget, DpgLabeled):
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
class _Plot(DpgContainer, DpgSizable[int], DpgLabeled):
    """Декартов график"""

    _x_axis: _PlotAxis
    _y_axis: _PlotAxis

    _show_legend: bool
    _show_grid: bool

    def enable_legend(self, enabled: bool) -> None:
        self._show_legend = enabled
        self._update_legend_visibility()

    def is_legend_enabled(self) -> bool:
        return self._show_legend

    def enable_grid(self, enabled: bool) -> None:
        self._show_grid = enabled
        self._update_grid_visibility()

    def is_grid_enabled(self) -> bool:
        return self._show_grid

    def _create_tag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_plot(parent=parent_tag)

    def _register_item(self, item) -> None:
        if isinstance(item, LineSeries):
            if not self._y_axis:
                self.add_y_axis()
            item.register(self._y_axis)
        elif isinstance(item, DragLine):
            item.register(self)
        else:
            raise TypeError(f"Неподдерживаемый элемент: {type(item)}")

    def update(self) -> None:
        super().update()
        self._update_legend_visibility()
        self._update_grid_visibility()

    def _update_grid_visibility(self):
        if self.is_registered():
            dpg.configure_item(self.tag(), show_grid=self._show_grid)

    def _update_legend_visibility(self):
        if self.is_registered():
            dpg.configure_item(self.tag(), show_legend=self._show_legend)


def Plot(
        show_legend: bool = False,
        show_grid: bool = False,
) -> _Plot:
    return _Plot(
        _x_axis=_PlotAxis(_axis_type=dpg.mvXAxis).with_label("X"),
        _y_axis=_PlotAxis(_axis_type=dpg.mvYAxis).with_label("Y"),
        _show_legend=show_legend,
        _show_grid=show_grid,
    )

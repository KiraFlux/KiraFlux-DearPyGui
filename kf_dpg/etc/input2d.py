from typing import Callable, Final, Optional

from kf_dpg.abc.traits import Intervaled, Valued, Handlerable, Labeled
from kf_dpg.core.custom import CustomWidget
from kf_dpg.impl.boxes import IntInput, FloatInput
from kf_dpg.impl.containers import HBox, VBox
from kf_dpg.impl.text import Text
from kf_dpg.misc.vector import Vector2D


class IntInput2D(CustomWidget, Valued[Vector2D[int]], Intervaled[int]):

    def __init__(
            self,
            label: str,
            interval: tuple[int, int],
            *,
            on_change: Callable[[Vector2D[int]], None] = None,
            default: Vector2D[int] = Vector2D(0, 0),
            width: int = 500,
            step: int = 1,
            step_fast: int = 1
    ) -> None:

        self._on_change: Final = on_change

        if on_change is None:
            _on_change_x = None
            _on_change_y = None
        else:
            def _on_change_x(x):
                on_change(Vector2D(x, self._y.get_value()))

            def _on_change_y(y):
                on_change(Vector2D(self._x.get_value(), y))

        interval_min, interval_max = interval

        item_width = width // 3

        self._y = IntInput(
            default=default.y,
            step=step,
            step_fast=step_fast,
            interval_max=interval_max,
            interval_min=interval_min,
        ).with_width(item_width).with_handler(_on_change_y)

        self._x = IntInput(
            default=default.x,
            step=step,
            step_fast=step_fast,
            interval_max=interval_max,
            interval_min=interval_min,
        ).with_width(item_width).with_handler(_on_change_x)

        base = (
            HBox()
            .add(
                VBox()
                .add(self._x)
                .add(self._y)
            )
            .add(Text(label))
        )

        super().__init__(base)

    def get_interval_max(self) -> int:
        return self._x.get_interval_max()

    def get_interval_min(self) -> int:
        return self._x.get_interval_min()

    def set_interval_max(self, new_max: int) -> None:
        self._x.set_interval_max(new_max)
        self._y.set_interval_max(new_max)

    def set_interval_min(self, new_min: int) -> None:
        self._x.set_interval_min(new_min)
        self._y.set_interval_min(new_min)

    def set_value(self, value: Vector2D[int]) -> None:
        self._x.set_value(value.x)
        self._y.set_value(value.y)
        self._on_change(value)

    def get_value(self) -> Vector2D[int]:
        return Vector2D(
            self._x.get_value(),
            self._y.get_value()
        )


class FloatInput2D(CustomWidget, Valued[Vector2D[float]], Intervaled[float],
                   Handlerable[Callable[[Vector2D[float]], None]], Labeled):

    def __init__(
            self,
            *,
            default: Vector2D[float] = Vector2D(0, 0),
            step: float = 1,
            step_fast: float = 1
    ) -> None:
        self._on_change: Optional[Callable[[Vector2D[float]], None]] = None

        self._y = FloatInput(
            default=default.y,
            step=step,
            step_fast=step_fast,
        )

        self._x = FloatInput(
            default=default.x,
            step=step,
            step_fast=step_fast,
        )

        self._label_text = Text()
        super().__init__(
            HBox()
            .add(
                VBox()
                .add(self._x)
                .add(self._y)
            )
            .add(self._label_text)
        )

    def set_label(self, label: Optional[str]) -> None:
        self._label_text.set_value(label)

    def get_label(self) -> Optional[str]:
        return self._label_text.get_value()

    def set_handler(self, on_change: Optional[Callable[[Vector2D[float]], None]]) -> None:
        self._on_change = on_change

        if self._on_change is None:
            _on_change_x = None
            _on_change_y = None
        else:
            def _on_change_x(x):
                on_change(Vector2D(x, self._y.get_value()))

            def _on_change_y(y):
                on_change(Vector2D(self._x.get_value(), y))

        self._x.set_handler(_on_change_x)
        self._y.set_handler(_on_change_y)

    def get_interval_max(self) -> float:
        return self._x.get_interval_max()

    def get_interval_min(self) -> float:
        return self._x.get_interval_min()

    def set_interval_max(self, new_max: float) -> None:
        self._x.set_interval_max(new_max)
        self._y.set_interval_max(new_max)

    def set_interval_min(self, new_min: float) -> None:
        self._x.set_interval_min(new_min)
        self._y.set_interval_min(new_min)

    def set_value(self, value: Vector2D[float]) -> None:
        self._x.set_value(value.x)
        self._y.set_value(value.y)

        if self._on_change:
            self._on_change(value)

    def get_value(self) -> Vector2D[float]:
        return Vector2D(self._x.get_value(), self._y.get_value())

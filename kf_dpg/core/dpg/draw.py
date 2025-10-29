from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import ClassVar
from typing import final

import dearpygui.dearpygui as dpg

from kf_dpg.abc.entities import Canvas
from kf_dpg.abc.entities import Figure
from kf_dpg.core.dpg.container import DpgContainer
from kf_dpg.core.dpg.item import DpgItem
from kf_dpg.core.dpg.item import DpgTag
from kf_dpg.core.dpg.traits import DpgDeletable
from kf_dpg.core.dpg.traits import DpgHeightAdjustable
from kf_dpg.core.dpg.traits import DpgVisibility
from rs.lina.vector import Vector2D
from rs.misc.color import Color


class DpgFigure(DpgVisibility, DpgDeletable, Figure, ABC):
    """Фигура из списка рисования"""

    @final
    def register(self, canvas: Canvas[DpgTag]) -> None:
        self._onRegister(self._createTag(canvas.tag()))


@final
@dataclass
class DpgCanvas(Canvas[DpgTag], DpgContainer):
    """Список рисования"""

    width: int
    height: int

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_drawlist(
            parent=parent_tag,
            width=self.width,
            height=self.height,
        )

    def _registerItem(self, item: DpgFigure) -> None:
        item.register(self)


@dataclass(kw_only=True)
class SupportFillColor(DpgItem):
    """Фигура поддерживает заливку цветом"""

    _fill_color: Color = Color.white()

    @property
    def fill_color(self):
        """Цвет заливки"""
        return self._fill_color

    @fill_color.setter
    def fill_color(self, c: Color):
        self._fill_color = c

        if self.isRegistered():
            self._updateFillColor()

    def update(self) -> None:
        super().update()
        self._updateFillColor()

    def _updateFillColor(self) -> None:
        self.configure(fill=self.fill_color.toRGBA8888())


@dataclass(kw_only=True)
class SupportContourThickness(DpgItem):
    """Фигура поддерживает толщину контура"""

    _contour_thickness: float = 1.0

    @property
    def contour_thickness(self):
        """Толщина контура"""
        return self._contour_thickness

    @contour_thickness.setter
    def contour_thickness(self, x):
        self._contour_thickness = x

        if self.isRegistered():
            self._updateContourThickness()

    def update(self) -> None:
        super().update()
        self._updateContourThickness()

    def _updateContourThickness(self) -> None:
        self.configure(thickness=self.contour_thickness)


@dataclass(kw_only=True)
class SupportContourColor(DpgItem):
    """Фигура поддерживает цвет контура"""

    _contour_color: Color = Color.white()

    @property
    def contour_color(self):
        """Цвет контура"""
        return self._contour_color

    @contour_color.setter
    def contour_color(self, x):
        self._contour_color = x

        if self.isRegistered():
            self._updateContourColor()

    def _updateContourColor(self) -> None:
        self.configure(color=self._contour_color.toRGBA8888())

    def update(self) -> None:
        super().update()
        self._updateContourColor()


@dataclass(kw_only=False)
class SupportTwoPositionsConstruct(DpgItem, ABC):
    """Фигура задаётся двумя координатами"""

    _position_1: Vector2D[float] = Vector2D(0, 0)

    _position_2: Vector2D[float] = Vector2D(0, 0)

    @property
    def position_1(self):
        """Первая координата"""
        return self._position_1

    @position_1.setter
    def position_1(self, x):
        self._position_1 = x

        if self.isRegistered():
            self._updatePosition1()

    @property
    def position_2(self):
        """Вторая координата"""
        return self._position_2

    @position_2.setter
    def position_2(self, x):
        self._position_2 = x

        if self.isRegistered():
            self._updatePosition2()

    @classmethod
    @abstractmethod
    def _keyPosition1(cls) -> str:
        """Получить ключ kwarg конфигурации первой позиции"""

    @classmethod
    @abstractmethod
    def _keyPosition2(cls) -> str:
        """Получить ключ kwarg конфигурации второй позиции"""

    def _updatePosition1(self) -> None:
        self.configure(**{
            self._keyPosition1(): self.position_1.toTuple()
        })

    def _updatePosition2(self) -> None:
        self.configure(**{
            self._keyPosition2(): self.position_2.toTuple()
        })

    def update(self) -> None:
        super().update()
        self._updatePosition1()
        self._updatePosition2()


@final
@dataclass
class Rectangle(DpgFigure, SupportTwoPositionsConstruct, SupportFillColor, SupportContourColor, SupportContourThickness):
    """Прямоугольник"""

    _rounding: float = 0

    @property
    def rounding(self):
        """Скругление в пикселях"""
        return self._rounding

    @rounding.setter
    def rounding(self, x):
        self._rounding = x

        if self.isRegistered():
            self._updateRounding()

    def _updateRounding(self) -> None:
        self.configure(rounding=self._rounding)

    def update(self) -> None:
        super().update()
        self._updateRounding()

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.draw_rectangle(
            (0, 0),
            (0, 0),
            parent=parent_tag,
        )

    @classmethod
    def _keyPosition1(cls) -> str:
        return 'pmin'

    @classmethod
    def _keyPosition2(cls) -> str:
        return 'pmax'


@final
@dataclass
class Line(DpgFigure, SupportTwoPositionsConstruct, SupportFillColor, SupportContourThickness):
    """Линия"""

    @classmethod
    def _keyPosition1(cls) -> str:
        return 'p1'

    @classmethod
    def _keyPosition2(cls) -> str:
        return 'p2'

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.draw_line(
            (0, 0),
            (0, 0),
            parent=parent_tag,
        )


@dataclass(kw_only=False)
class Positioned(DpgItem):
    """Фигура поддерживает определение одной координатой"""

    _position_key: ClassVar[str] = 'pos'

    _position: Vector2D[float]
    """Позиция"""

    @property
    def position(self):
        """Первая координата"""
        return self._position

    @position.setter
    def position(self, x):
        self._position = x

        if self.isRegistered():
            self._updatePosition()

    def _updatePosition(self):
        self.configure(**{
            self._position_key: self.position.toTuple()
        })

    def update(self) -> None:
        super().update()
        self._updatePosition()


@final
@dataclass
class Circle(DpgFigure, Positioned, SupportContourColor, SupportContourThickness, SupportFillColor):
    """Окружность"""

    _position_key: ClassVar[str] = 'center'
    _radius: float

    @property
    def radius(self):
        """Радиус в пикселях"""
        return self._radius

    @radius.setter
    def radius(self, x):
        self._radius = x

        if self.isRegistered():
            self._updateRadius()

    def _updateRadius(self) -> None:
        self.configure(radius=self.radius)

    def update(self) -> None:
        super().update()
        self._updateRadius()

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.draw_circle(
            (0, 0),
            0,
            parent=parent_tag,
        )


@final
class TextFigure(DpgFigure, Positioned, SupportFillColor, DpgHeightAdjustable):
    """Нарисованный текст"""

    _height_key: ClassVar = 'size'

    def __init__(
            self,
            text: str,
            position: Vector2D,
            fill_color: Color = Color.white(),
            height: float = 20.0
    ):
        # Инициализируем родительские классы с правильными параметрами
        DpgFigure.__init__(self)
        Positioned.__init__(self, _position=position)
        SupportFillColor.__init__(self, _fill_color=fill_color)
        DpgHeightAdjustable.__init__(self, _height=height)

        # Инициализируем специфичные для TextFigure поля
        self._text = text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, x):
        self._text = x
        if self.isRegistered():
            self._updateText()

    def _updateText(self) -> None:
        self.configure(text=self.text)

    def update(self) -> None:
        super().update()
        self._updateText()

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.draw_text(
            self.position.toTuple(),
            self.text,
            parent=parent_tag,
            size=self.getHeight()
        )
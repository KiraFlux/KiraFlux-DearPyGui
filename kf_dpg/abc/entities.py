from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Self, final


class Container[T](ABC):
    """Способен содержат элементы"""

    @abstractmethod
    def add(self, item: T) -> Self:
        """Добавить элемент"""


class Item[T](ABC):
    """Элемент системы"""

    @abstractmethod
    def tag(self) -> Optional[T]:
        """Получить тег элемента"""

    @final
    def is_registered(self) -> bool:
        """Элемент уже зарегистрирован"""
        return self.tag() is not None


class Font[T](Item[T], ABC):
    """Шрифт"""

    @abstractmethod
    def _register(self) -> None:
        """Регистрация шрифта"""


class Widget[T](Item[T], ABC):
    """Виджет"""

    @abstractmethod
    def _create_tag(self, parent_tag: T) -> T:
        """Создать элемент"""

    @abstractmethod
    def set_font(self, font: Font) -> None:
        """Установить шрифт"""

    @final
    def withFont(self, font: Font) -> Self:
        """Установить шрифт и вернуть себя"""
        self.set_font(font)
        return self

    @abstractmethod
    def register(self, parent: Widget[T]) -> None:
        """Регистрация виджета"""


class Figure[T](Item[T], ABC):
    """Фигура"""

    @abstractmethod
    def _create_tag(self, parent_tag: T) -> T:
        """Создать элемент"""

    def register(self, canvas: Canvas[T]) -> None:
        """Регистрация фигуры"""


class Canvas[T](Widget[T], Container[Figure[T]], ABC):
    """Холст для размещения фигур"""

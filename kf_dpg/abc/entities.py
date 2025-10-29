from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Optional
from typing import Self
from typing import final


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
    def isRegistered(self) -> bool:
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
    def _createTag(self, parent_tag: T) -> T:
        """Создать элемент"""

    @abstractmethod
    def setFont(self, font: Font) -> None:
        """Установить шрифт"""

    @final
    def withFont(self, font: Font) -> Self:
        """Установить шрифт и вернуть себя"""
        self.setFont(font)
        return self

    @abstractmethod
    def register(self, parent: Widget[T]) -> None:
        """Регистрация виджета"""


class Figure[T](Item[T], ABC):
    """Фигура"""

    @abstractmethod
    def _createTag(self, parent_tag: T) -> T:
        """Создать элемент"""

    def register(self, canvas: Canvas[T]) -> None:
        """Регистрация фигуры"""


class Canvas[T](Widget[T], Container[Figure[T]], ABC):
    """Холст для размещения фигур"""

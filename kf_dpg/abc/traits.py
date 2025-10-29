from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Callable
from typing import Optional
from typing import Self
from typing import final

from rs.lina.vector import Vector2D
from rs.misc.color import Color


class Colored(ABC):
    """Обладает цветом"""

    @abstractmethod
    def setColor(self, color: Color) -> None:
        """Изменить цвет"""

    @abstractmethod
    def getColor(self) -> Color:
        """Получить актуальный цвет"""


class Intervaled[T](ABC):
    """Обладает интервалом"""

    type Interval = tuple[T, T]
    """Диапазон значений"""

    @abstractmethod
    def getIntervalMax(self) -> T:
        """Получить максимальное допустимое значение"""

    @abstractmethod
    def setIntervalMax(self, new_max: T) -> None:
        """Установить минимальное допустимое значение"""

    @abstractmethod
    def getIntervalMin(self) -> T:
        """Получить минимальное допустимое значение"""

    @abstractmethod
    def setIntervalMin(self, new_min: T) -> None:
        """Установить минимальное допустимое значение"""

    @final
    def getInterval(self) -> Interval:
        """Получить диапазона"""
        return (
            self.getIntervalMin(),
            self.getIntervalMax()
        )

    @final
    def setInterval(self, interval: Interval) -> None:
        """Установить диапазон"""
        new_min, new_max = interval
        self.setIntervalMin(new_min)
        self.setIntervalMax(new_max)

    @final
    def withInterval(self, interval: Interval) -> Self:
        """Установить интервал и вернуть себя"""
        self.setInterval(interval)
        return self


class Valued[T](ABC):
    """Обладает значением"""

    @abstractmethod
    def getValue(self) -> T:
        """Получить актуальное значение"""

    @abstractmethod
    def setValue(self, value: T) -> None:
        """Установить значение"""

    @final
    def withValue(self, value: T) -> Self:
        """Установить значение и вернуть себя"""
        self.setValue(value)
        return self


class WidthAdjustable[T: (int, float)](ABC):
    """Обладает шириной"""

    @abstractmethod
    def getWidth(self) -> T:
        """Получить актуальную ширину"""

    @abstractmethod
    def setWidth(self, width: T) -> None:
        """Установить ширину"""

    @final
    def withWidth(self, width: T) -> Self:
        """Установить ширину и вернуть"""
        self.setWidth(width)
        return self


class HeightAdjustable[T: (int, float)](ABC):
    """Обладает высотой"""

    @abstractmethod
    def getHeight(self) -> T:
        """Получить актуальную высоту"""

    @abstractmethod
    def setHeight(self, height: T) -> None:
        """Установить ширину"""

    @final
    def withHeight(self, height: T) -> Self:
        """Установить ширину и вернуть себя"""
        self.setHeight(height)
        return self


class Sizable[T: (int, float)](HeightAdjustable, WidthAdjustable, ABC):
    """Обладает размерами (шириной и высотой)"""

    @final
    def getSize(self) -> Vector2D[T]:
        """Получить актуальный размер"""
        return Vector2D(
            self.getWidth(),
            self.getHeight()
        )

    @final
    def setSize(self, size: Vector2D[T]) -> None:
        """Установить размер"""
        self.setWidth(size.x)
        self.setHeight(size.y)

    @final
    def withSize(self, size: Vector2D[T]) -> Self:
        """Установить размер и вернуть себя"""
        self.setSize(size)
        return self


class Toggleable(ABC):
    """Обладает свойством включения и выключения"""

    @abstractmethod
    def setEnabled(self, enabled: bool) -> None:
        """Установить включенность объекта"""

    @abstractmethod
    def isEnabled(self) -> bool:
        """Включен объект"""

    @final
    def enable(self) -> None:
        """Включить"""
        self.setEnabled(True)

    @final
    def disable(self) -> None:
        """Отключить"""
        self.setEnabled(False)


class Visibility(ABC):
    """Обладает способностью быть видимым или скрытым"""

    @abstractmethod
    def setVisibility(self, is_visible: bool) -> None:
        """Установить видимость объекта"""

    @abstractmethod
    def isVisible(self) -> bool:
        """Объект видимый"""

    @final
    def show(self) -> None:
        """Показать"""
        self.setVisibility(True)

    @final
    def hide(self) -> None:
        """Скрыть"""
        self.setVisibility(False)


class Deletable(ABC):
    """Обладает возможностью быть удаленным"""

    @abstractmethod
    def attachDeleteObserver(self, f: Callable[[Deletable], Any]) -> None:
        """Добавить наблюдатель при удалении объекта"""

    @abstractmethod
    def detachDeleteObserver(self, f: Callable[[Deletable], Any]) -> None:
        """Удалить наблюдателя при удалении объекта"""

    @abstractmethod
    def delete(self) -> None:
        """Удалить"""


class Handlerable[F: Callable](ABC):
    """Обладает обработчиком"""

    @abstractmethod
    def setHandler(self, f: Optional[F]) -> None:
        """Установить обработчик обратного вызова"""

    @final
    def withHandler(self, f: Optional[F]) -> Self:
        """Установить обработчик обратного вызова и вернуть себя"""
        self.setHandler(f)
        return self


class Labeled(ABC):
    """Обладаем меткой (label)"""

    @abstractmethod
    def setLabel(self, label: Optional[str]) -> None:
        """Установить метку объекта"""

    @abstractmethod
    def getLabel(self) -> Optional[str]:
        """Получить текущую метку объекта"""

    @final
    def withLabel(self, label: Optional[str]) -> Self:
        """Установить метку объекта и вернуть текущий экземпляр"""
        self.setLabel(label)
        return self

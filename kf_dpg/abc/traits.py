from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Optional, Self, final

from kf_dpg.misc.color import Color
from kf_dpg.misc.vector import Vector2D


class Colored(ABC):
    """Обладает цветом"""

    @abstractmethod
    def set_color(self, color: Color) -> None:
        """Изменить цвет"""

    @abstractmethod
    def get_color(self) -> Color:
        """Получить актуальный цвет"""


class Intervaled[T](ABC):
    """Обладает интервалом"""

    type Interval = tuple[T, T]
    """Диапазон значений"""

    @abstractmethod
    def get_interval_max(self) -> T:
        """Получить максимальное допустимое значение"""

    @abstractmethod
    def set_interval_max(self, new_max: T) -> None:
        """Установить минимальное допустимое значение"""

    @abstractmethod
    def get_interval_min(self) -> T:
        """Получить минимальное допустимое значение"""

    @abstractmethod
    def set_interval_min(self, new_min: T) -> None:
        """Установить минимальное допустимое значение"""

    @final
    def get_interval(self) -> Interval:
        """Получить диапазона"""
        return (
            self.get_interval_min(),
            self.get_interval_max()
        )

    @final
    def set_interval(self, interval: Interval) -> None:
        """Установить диапазон"""
        new_min, new_max = interval
        self.set_interval_min(new_min)
        self.set_interval_max(new_max)

    @final
    def with_interval(self, interval: Interval) -> Self:
        """Установить интервал и вернуть себя"""
        self.set_interval(interval)
        return self


class Valued[T](ABC):
    """Обладает значением"""

    @abstractmethod
    def get_value(self) -> T:
        """Получить актуальное значение"""

    @abstractmethod
    def set_value(self, value: T) -> None:
        """Установить значение"""

    @final
    def with_value(self, value: T) -> Self:
        """Установить значение и вернуть себя"""
        self.set_value(value)
        return self


class WidthAdjustable[T: (int, float)](ABC):
    """Обладает шириной"""

    @abstractmethod
    def get_width(self) -> T:
        """Получить актуальную ширину"""

    @abstractmethod
    def set_width(self, width: T) -> None:
        """Установить ширину"""

    @final
    def with_width(self, width: T) -> Self:
        """Установить ширину и вернуть"""
        self.set_width(width)
        return self


class HeightAdjustable[T: (int, float)](ABC):
    """Обладает высотой"""

    @abstractmethod
    def get_height(self) -> T:
        """Получить актуальную высоту"""

    @abstractmethod
    def set_height(self, height: T) -> None:
        """Установить ширину"""

    @final
    def with_height(self, height: T) -> Self:
        """Установить ширину и вернуть себя"""
        self.set_height(height)
        return self


class Sizable[T: (int, float)](HeightAdjustable, WidthAdjustable, ABC):
    """Обладает размерами (шириной и высотой)"""

    @final
    def get_size(self) -> Vector2D[T]:
        """Получить актуальный размер"""
        return Vector2D(
            self.get_width(),
            self.get_height()
        )

    @final
    def set_size(self, size: Vector2D[T]) -> None:
        """Установить размер"""
        self.set_width(size.x)
        self.set_height(size.y)

    @final
    def with_size(self, size: Vector2D[T]) -> Self:
        """Установить размер и вернуть себя"""
        self.set_size(size)
        return self


class Toggleable(ABC):
    """Обладает свойством включения и выключения"""

    @abstractmethod
    def set_enabled(self, enabled: bool) -> None:
        """Установить включенность объекта"""

    @abstractmethod
    def is_enabled(self) -> bool:
        """Включен объект"""

    @final
    def enable(self) -> None:
        """Включить"""
        self.set_enabled(True)

    @final
    def disable(self) -> None:
        """Отключить"""
        self.set_enabled(False)


class Visibility(ABC):
    """Обладает способностью быть видимым или скрытым"""

    @abstractmethod
    def set_visibility(self, is_visible: bool) -> None:
        """Установить видимость объекта"""

    @abstractmethod
    def is_visible(self) -> bool:
        """Объект видимый"""

    @final
    def show(self) -> None:
        """Показать"""
        self.set_visibility(True)

    @final
    def hide(self) -> None:
        """Скрыть"""
        self.set_visibility(False)


class Deletable(ABC):
    """Обладает возможностью быть удаленным"""

    @abstractmethod
    def attach_delete_observer(self, f: Callable[[Deletable], Any]) -> None:
        """Добавить наблюдатель при удалении объекта"""

    @abstractmethod
    def detach_delete_observer(self, f: Callable[[Deletable], Any]) -> None:
        """Удалить наблюдателя при удалении объекта"""

    @abstractmethod
    def delete(self) -> None:
        """Удалить"""


class Handlerable[F: Callable](ABC):
    """Обладает обработчиком"""

    @abstractmethod
    def set_handler(self, f: Optional[F]) -> None:
        """Установить обработчик обратного вызова"""

    @final
    def with_handler(self, f: Optional[F]) -> Self:
        """Установить обработчик обратного вызова и вернуть себя"""
        self.set_handler(f)
        return self


class Labeled(ABC):
    """Обладаем меткой (label)"""

    @abstractmethod
    def set_label(self, label: Optional[str]) -> None:
        """Установить метку объекта"""

    @abstractmethod
    def get_label(self) -> Optional[str]:
        """Получить текущую метку объекта"""

    @final
    def with_label(self, label: Optional[str]) -> Self:
        """Установить метку объекта и вернуть текущий экземпляр"""
        self.set_label(label)
        return self

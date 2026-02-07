"""Модальное диалоговое окно"""
from abc import ABC, abstractmethod
from typing import Callable, Optional, final

import dearpygui.dearpygui as dpg
from kf_dpg.abc.entities import Widget
from kf_dpg.abc.traits import Labeled
from kf_dpg.core.custom import CustomWidget
from kf_dpg.impl.buttons import Button
from kf_dpg.impl.containers import VBox, Window
from kf_dpg.impl.misc import Separator, Spacer
from kf_dpg.impl.text import Text


class ModalDialog(CustomWidget, Labeled):
    """Модальный диалог"""

    def __init__(self):
        self._window = Window(
            _auto_size=True,
            _modal=True,
        )
        super().__init__(self._window)

    def get_label(self) -> Optional[str]:
        return self._window.get_label()

    def set_label(self, label: Optional[str]) -> None:
        self._window.set_label(label)

    def show(self) -> None:
        """Показать диалог с центрированием"""
        super().show()
        self._center_window()

    def _center_window(self) -> None:
        """Центрировать окно на экране с учётом реального размера"""
        if not self._window.is_registered():
            return

        dpg.split_frame()

        # Получаем реальный размер окна
        window_width = dpg.get_item_width(self._window.tag())
        window_height = dpg.get_item_height(self._window.tag())

        # Получаем размеры viewport'а
        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()

        # Вычисляем позицию для центрирования
        x_pos = (viewport_width - window_width) // 2
        y_pos = (viewport_height - window_height) // 2

        dpg.set_item_pos(self._window.tag(), [x_pos, y_pos])


class ConfirmDialog(ModalDialog):
    """Диалог подтверждения"""

    def __init__(self, *, ok_button_label: str = "Ok"):
        super().__init__()

        self._text = Text()
        self._button = Button()

        (
            self._window
            .add(
                VBox()
                .add(self._text)
                .add(Separator())
                .add(Spacer().with_height(20))
                .add(
                    self._button
                    .with_label(ok_button_label)
                    .with_width(-1)
                )
            )
        )

    def begin(
            self,
            text: str,
            *,
            on_confirm: Callable[[], None]
    ) -> None:
        """
        Запустить процедуру окна
        :param text:
        :param on_confirm:
        """

        def _f():
            on_confirm()
            self.hide()

        self._text.set_value(text)
        self._button.set_handler(_f)

        self.show()


class EditDialog[T](ModalDialog, ABC):
    """Модальный диалог редактирования"""

    @classmethod
    @abstractmethod
    def _get_title(cls, value: T) -> str:
        """Получить заголовок из значения"""

    def __init__(self, content: Widget) -> None:
        super().__init__()

        self.__value: Optional[T] = None

        (
            self._window
            .add(content)
            .add(Separator())
            .add(Spacer().with_height(30))
            .add(
                Button()
                .with_label("Применить")
                .with_width(-1)
                .with_handler(self._apply)
            )
        )

    def _apply(self) -> None:
        self.hide()

        if self.__value is not None:
            self.apply(self.__value)

    def apply(self, value: T) -> None:
        """Применить изменения"""

    def begin(self, value: T) -> None:
        self.show()
        self.__value = value
        self._window.set_label(self._get_title(value))

    @final
    def create_edit_button(self, value: T) -> Button:
        return (
            Button()
            .with_handler(lambda: self.begin(value))
        )

from __future__ import annotations

from threading import Thread
from typing import Sequence
from typing import final

from dearpygui import dearpygui as dpg

from kf_dpg.core.dpg.font import DpgFont
from kf_dpg.impl.containers import Window


class App:
    """Приложение Dear Py Gui"""

    def __init__(self, window: Window):
        self.window = window

    @final
    def run(self, title: str, width: int, height: int, *, user_tasks: Sequence[Thread] = ()) -> None:
        """Запуск"""

        x = (1920 - width) // 2
        y = (1080 - height) // 2

        dpg.create_context()

        DpgFont.load()

        dpg.create_viewport(
            title=title,
            width=width,
            height=height,
            x_pos=x,
            y_pos=y,
        )

        Window.registerAll()

        for task in user_tasks:
            task.start()

        tag = self.window.tag()
        dpg.set_primary_window(tag, True)

        dpg.setup_dearpygui()

        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    @staticmethod
    def setTitle(title: str) -> None:
        """Установить заголовок окна"""
        dpg.set_viewport_title(title)

    @staticmethod
    def setSize(width: int, height: int) -> None:
        """Установить размер окна"""
        dpg.set_viewport_width(width)
        dpg.set_viewport_height(height)

    @classmethod
    def getSize(cls) -> tuple[int, int]:
        """Получить размер окна"""
        return (
            cls.getWidth(),
            cls.getHeight()
        )

    @staticmethod
    def getWidth() -> int:
        """Получить ширину окна"""
        return dpg.get_viewport_width()

    @staticmethod
    def getHeight() -> int:
        """Получить высоту окна"""
        return dpg.get_viewport_height()

    @staticmethod
    def setPosition(x: float, y: float) -> None:
        """Установить позицию окна"""
        dpg.set_viewport_pos([x, y])

    @staticmethod
    def getPosition() -> tuple[float, float]:
        """Получить позицию окна"""
        x, y = dpg.get_viewport_pos()
        return x, y

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from typing import Self
from typing import final

from kf_dpg.abc.entities import Container
from kf_dpg.abc.traits import Deletable
from kf_dpg.core.dpg.item import DpgTag
from kf_dpg.core.dpg.widget import DpgWidget


@dataclass
class DpgContainer[T: Deletable](DpgWidget, Container[T], ABC):
    _items: dict[int, T] = field(init=False, default_factory=dict)
    _deleted: bool = field(init=False, default=False)

    @abstractmethod
    def _register_item(self, item: T) -> None:
        """Регистрация элемента"""

    @final
    def add(self, item: T) -> Self:
        item_id = id(item)
        self._items[item_id] = item

        # Подписываемся на удаление элемента
        item.attach_delete_observer(self._on_item_deleted)

        if self.is_registered():
            self._register_item(item)

        return self

    def _on_item_deleted(self, item: Deletable) -> None:
        if self._deleted:
            return

        if id(item) in self._items:
            item.detach_delete_observer(self._on_item_deleted)
            del self._items[id(item)]

    @final
    def delete(self) -> None:
        if self._deleted:
            return

        self._deleted = True

        for item in list(self._items.values()):
            item.detach_delete_observer(self._on_item_deleted)
            item.delete()

        self._items.clear()
        super().delete()

    def _on_register(self, tag: DpgTag) -> None:
        super()._on_register(tag)
        for item in self._items.values():
            self._register_item(item)

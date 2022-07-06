from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')


class ModelStorageService(ABC, Generic[T]):

    @abstractmethod
    def get_last(self) -> T:
        pass

    @abstractmethod
    def save(self, model: T) -> T:
        pass

    @abstractmethod
    def get(self, model_id: str) -> T:
        pass

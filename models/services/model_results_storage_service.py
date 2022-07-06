from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List

T = TypeVar('T')


class ModelResultsStorageService(ABC, Generic[T]):

    @abstractmethod
    def get_all(self) -> List[T]:
        pass

    @abstractmethod
    def get(self, model_id: str) -> T:
        pass

    @abstractmethod
    def save(self, model: T) -> T:
        pass

    @abstractmethod
    def remove_all(self):
        pass

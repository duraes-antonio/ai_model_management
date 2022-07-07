from abc import ABC, abstractmethod
from typing import TypeVar, Optional

from models.entity import Entity

T = TypeVar('T')


class ModelStorageService(ABC):

    @abstractmethod
    def save(self, model_file_path: str) -> None:
        pass

    @abstractmethod
    def download(self, model_id: str) -> Optional[Entity]:
        pass

    @abstractmethod
    def download_last(self) -> Optional[Entity]:
        pass

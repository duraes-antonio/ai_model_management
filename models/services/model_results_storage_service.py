from abc import ABC, abstractmethod
from typing import TypeVar, List, Dict

T = TypeVar('T')


class ModelResultsStorageService(ABC):

    @abstractmethod
    def get_all(self) -> List[Dict]:
        pass

    @abstractmethod
    def get(self, result_id: str) -> Dict:
        pass

    @abstractmethod
    def save(self, result: Dict) -> Dict:
        pass

    @abstractmethod
    def remove_all(self):
        pass

from typing import List, Generic

from models.services.model_results_storage_service import ModelResultsStorageService, T


class LocalResultsStorageService(ModelResultsStorageService[T], Generic[T]):

    def get_all(self) -> List[T]:
        pass

    def get(self, model_id: str) -> T:
        pass

    def save(self, model: T) -> T:
        pass

    def remove_all(self):
        pass

from typing import TypeVar, Generic, List, Dict

from base.abstractions import BaseServiceProtocol

class BaseService(BaseServiceProtocol):
    def __init__(self, model):
        self._model = model

    def get_all(self) -> List[dict]:
        all_objects = list(self._model.objects.values())
        return all_objects

    def create(self, data: Dict) -> None:
        return self._model.objects.create(**data)

    def update(self, data: dict) -> None:
        return self._model.objects.filter(data=data).update(**data)

    def delete(self, model_id: int) -> None:
        instance = self._model.objects.get(id=model_id)
        instance.delete()

    def get_by(self, **filters: dict) -> List:
        return list(self._model.objects.filter(**filters))

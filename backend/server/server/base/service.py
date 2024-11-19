from typing import TypeVar, Generic, List, Dict

from base.abstractions import BaseServiceProtocol
from django.db import models


T = TypeVar("T", bound=models.Model)

class BaseService(Generic[T]):
    model = T

    def get_all(self) -> List[dict]:
        return list(self.model.objects.values())

    def create(self, data: Dict) -> None:
        return self.model.objects.create(**data)

    def update(self, data: dict) -> None:
        return self.model.objects.filter(data=data).update(**data)

    def delete(self, model_id: int) -> None:
        instance = self.model.objects.get(id=model_id)
        instance.delete()
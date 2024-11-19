from typing import Protocol, List
from typing import TypeVar, Generic
from django.db import models

T = TypeVar("T", bound=models.Model)

class BaseServiceProtocol[T] (Protocol):

    model = T

    def get_all(self) -> List: ...

    def create(self, data) -> None: ...

    def update(self, data) -> None: ...

    def delete(self, model_id: int) -> None: ...

    def getby(self, **filters: dict) -> List: ...
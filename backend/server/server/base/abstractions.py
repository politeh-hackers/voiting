from typing import Protocol, List
from typing import TypeVar, Generic
from django.db import Error, models

T = TypeVar("T", bound=models.Model)

class BaseServiceProtocol(Protocol[T]):

    model: T

    def get_all(self) -> List: ...

    def create(self, data) -> None: ...

    def update(self, data) -> None: ...

    def delete(self, model_id: int) -> None: ...

    def getby(self, **filters: dict) -> List: ...

class BaseValidateProtocol():

    def validate(self, data) -> None: ...  

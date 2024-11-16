from typing import Protocol, List

from django.db.models import QuerySet


class BaseServiceProtocol(Protocol):
    def get_all(self) -> List: ...

    def create(self, data) -> None: ...

    def update(self, data) -> None: ...

    def delete(self, model_id: int) -> None: ...


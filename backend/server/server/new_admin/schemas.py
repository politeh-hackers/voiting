from dataclasses import dataclass
import json


@dataclass(slots=True)
class MediaTagSchema:
    id: int
    name: str

    def __repr__(self):
        return json.dumps(self.__class__.__dict__)

@dataclass(slots=True)
class CreateMediaTagSchema:
    name: str
from typing import TypeVar, Generic, List, Dict
from django.db import models
import uuid

T = TypeVar("T", bound=models.Model)


class BaseService(Generic[T]):
    
    model: T

    def __init__(self, model: T):
        self.model = model

    def get_all(self) -> List[dict]:
        return list(self.model.objects.values())

    def create(self, data):
        instance = self.model.objects.create(**data)
        return instance

    def update(self, model_id: uuid.UUID, data: Dict) -> None:
        self.model.objects.filter(id=model_id).update(**data)

    def delete(self, model_id: uuid.UUID) -> None:
        instance: T = self.model.objects.get(id=model_id)
        instance.delete()








# class BaseValidationService:

#     name_regex = re.compile(r'^[A-Za-zА-Яа-яЁё\s-]+$')  
#     phone_regex = re.compile(r'^\+375\(\d{2}\)\d{3}-\d{2}-\d{2}$')  


#     def validate_appeal_fields(self, data):

#         self.validate_phone(data.get('phone'))


#         self.validate_length(data.get('official_response'), 500, Constants.MAX_LEN_TEXT)
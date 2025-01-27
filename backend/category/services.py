from django.core.exceptions import ValidationError
from base.service import BaseService
from .models import Category
from base.enums import FilterErrorMessages

class CategoryService(BaseService): 

    def __init__(self, model=Category):
        self.model = model




import re
from datetime import datetime
from django.forms import ImageField

from django.utils import timezone
from django.core.exceptions import ValidationError
from base.service import BaseService, BaseValidationService
from pages.models import Actual, Appeal, Media, MediaTag, ActualTag

    
class MediaService(BaseService):
    def __init__(self, model=Media):
        self.model = model
        self.validator = BaseValidationService()

    def validate(self, data: Media):
        self.validator.validate_common_fields(data)
        self.validator.validate_media_actual_fields(data)
        return data

class ActualService(BaseService):
    def __init__(self, model=Actual):
        self.model = model
        self.validator = BaseValidationService()

    def validate(self, data: Actual):
        self.validator.validate_common_fields(data)
        self.validator.validate_media_actual_fields(data)
        return data

class AppealService(BaseService):
    def __init__(self, model=Appeal):
        self.model = model
        self.validator = BaseValidationService()

    def validate(self, data: Appeal):
        self.validator.validate_common_fields(data)
        self.validator.validate_appeal_fields(data)
        return data

class CategoryService(BaseService): pass
from base.service import BaseService
from .models import Actual

class ActualService(BaseService):

    def __init__(self, model=Actual):
        self.model = model

    def validate(self, data: Actual):
        # self.validator.validate_common_fields(data)
        # self.validator.validate_media_actual_fields(data)
        return data
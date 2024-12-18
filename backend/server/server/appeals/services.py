from base.service import BaseService
from .models import Appeal

class AppealService(BaseService):

    def __init__(self, model=Appeal):
        self.model = model
        # self.validator = BaseValidationService()

    def validate(self, data: Appeal):
        # self.validator.validate_common_fields(data)
        # self.validator.validate_appeal_fields(data)
        return data
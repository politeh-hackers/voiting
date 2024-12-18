from base.service import BaseService
from .models import Media, MediaTag

class MediaService(BaseService):

    def __init__(self, model=Media):
        self.model = model
        # self.validator = BaseValidationService()

    # def validate(self, data: dict):
    #     """
    #     Validates the input data using the assigned schema and returns a JSON response in case of validation errors.
    #     :param data: Dictionary containing data to validate.
    #     :return: Validated data or JsonResponse with errors.
    #     """
    #     validation_result = BaseValidationService.validate_or_error(self.validator, data)
    #     if isinstance(validation_result, dict):  # Если это словарь с ошибками
    #         return JsonResponse(validation_result, status=400)  # Возвращаем ошибки
    #     return validation_result  # Возвращаем валидированные данные

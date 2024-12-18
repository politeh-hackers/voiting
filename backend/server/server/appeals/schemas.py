from pydantic import Field
from base.schemas import BaseValidationSchema
from base.constants import Constants

class AppealFieldsSchema(BaseValidationSchema):
        
        first_name: str = Field(
            ..., 
            min_length=4, 
            max_length=Constants.MAX_LEN_NAME_FIELD, 
            description=f"Поле должно содержать от 4 до {Constants.MAX_LEN_NAME_FIELD}"
        )
        last_name: str = Field(
            ..., 
            min_length=4, 
            max_length=Constants.MAX_LEN_NAME_FIELD, 
            description=f"Поле должно содержать от 4 до {Constants.MAX_LEN_NAME_FIELD}"
        )
        patronymic: str = Field(
            ..., 
            min_length=4, 
            max_length=Constants.MAX_LEN_NAME_FIELD, 
            description=f"Поле должно содержать от 4 до {Constants.MAX_LEN_NAME_FIELD}"
        )
        text: str = Field(
            ..., 
            min_length=Constants.MIN_LEN_TEXT, 
            max_length=Constants.MAX_LEN_TEXT, 
            description=f"Поле должно содержать от {Constants.MIN_LEN_TEXT} до {Constants.MAX_LEN_TEXT}"
        )
        official_responce: str = Field(
            ..., 
            min_length=Constants.MIN_LEN_TEXT, 
            max_length=Constants.MAX_LEN_TEXT, 
            description=f"Поле должно содержать от {Constants.MIN_LEN_TEXT} до {Constants.MAX_LEN_TEXT}"
        )

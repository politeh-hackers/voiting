from pydantic import BaseModel, Field
from base.constants import Constants

class AppealClientFieldsSchema(BaseModel):
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
        location: str = Field(
            ...
        )
        phone: str = Field(
            ...
        )


class AppealAdminFieldsSchema(BaseModel):
        official_responce: str = Field(
            ..., 
            min_length=Constants.MIN_LEN_TEXT, 
            max_length=Constants.MAX_LEN_TEXT, 
            description=f"Поле должно содержать от {Constants.MIN_LEN_TEXT} до {Constants.MAX_LEN_TEXT}"
        )
        status: str = Field(
            ...
        )
        on_website: bool = Field(
            ...
        )
        category: str = Field(
            ...
        )
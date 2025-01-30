from pydantic import BaseModel, Field, constr
from typing import List, Optional, Union
from base.constants import Constants

class AppealCreateSchema(BaseModel):
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
    phone: str = Field(
        ..., 
        min_length=4, 
        max_length=Constants.MAX_LEN_NAME_FIELD, 
        description=f"Поле должно содержать от 4 до {Constants.MAX_LEN_NAME_FIELD}"
    )
    location: str = Field(
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
    category: str = Field(
        ...
    )

class AppealUpdateSchema(BaseModel):
    official_response: Optional[Union[constr(min_length=500, max_length=3000), None]] = Field(
        None,
        description="Поле может быть пустым или содержать от 500 до 3000 символов."
    )
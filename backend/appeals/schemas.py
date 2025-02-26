from pydantic import BaseModel, Field, constr
from typing import List, Optional, Union
from base.constants import Constants

class AppealCreateSchema(BaseModel):
    first_name: str = Field(
        ..., 
        min_length=1, 
        max_length=Constants.MAX_LEN_NAME_FIELD, 
        description=f"Поле должно содержать от 1 до {Constants.MAX_LEN_NAME_FIELD}"
    )
    last_name: str = Field(
        ..., 
        min_length=1, 
        max_length=Constants.MAX_LEN_NAME_FIELD, 
        description=f"Поле должно содержать от 1 до {Constants.MAX_LEN_NAME_FIELD}"
    )
    patronymic: str = Field(
        ..., 
        min_length=1, 
        max_length=Constants.MAX_LEN_NAME_FIELD, 
        description=f"Поле должно содержать от 1 до {Constants.MAX_LEN_NAME_FIELD}"
    )
    phone: str = Field(
        ..., 
        min_length=12, 
        max_length=Constants.MAX_LEN_NAME_FIELD, 
        description=f"Поле должно содержать от 12 до {Constants.MAX_LEN_NAME_FIELD}"
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
    photos: Optional[List[str]] = Field(None)

class AppealUpdateSchema(BaseModel):
    official_response: Optional[str] = Field(
        None,
        description="Поле может быть пустым или содержать от 500 до 3000 символов."
    )
    status: Optional[str] = Field(None)
    on_website: Optional[bool] = Field(None)
    date_responce: Optional[str] = Field(None)
from pydantic import BaseModel, Field
from typing import List, Optional
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
    official_response: Optional[str] = Field(
        None, 
        min_length=Constants.MIN_LEN_TEXT, 
        max_length=Constants.MAX_LEN_TEXT, 
        description=f"Поле должно содержать от {Constants.MIN_LEN_TEXT} до {Constants.MAX_LEN_TEXT}"
    )
    first_name: Optional[str] = Field(None)
    last_name: Optional[str] = Field(None)
    patronymic: Optional[str] = Field(None)
    phone: Optional[str] = Field(None)
    location: Optional[str] = Field(None)
    text: Optional[str] = Field(None)
    category: Optional[str] = Field(None)
    status: Optional[str] = Field(None)
    on_website: Optional[bool] = Field(None)

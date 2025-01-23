from pydantic import BaseModel, Field
from typing import List, Optional
from base.constants import Constants

<<<<<<< HEAD
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
        photos: list = Field(
            ...,
            min_length=1, 
            max_length=Constants.MAX_LEN_NAME_FIELD, 
            description=f"Поле должно содержать от 4 до {Constants.MAX_LEN_NAME_FIELD}"
        )
=======
class AppealBaseSchema(BaseModel):
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
    # photos: Optional[str] = Field(
    #     None, 
    #     description="Может отсутствовать или быть несколько"
    # )
>>>>>>> d6e09b93a979ce0e7578a00d4ed6e3dd625eb21d

class AppealCreateSchema(AppealBaseSchema):    
    pass

class AppealUpdateSchema(AppealBaseSchema):
    official_response: Optional[str] = Field(
        None, 
        min_length=Constants.MIN_LEN_TEXT, 
        max_length=Constants.MAX_LEN_TEXT, 
        description=f"Поле должно содержать от {Constants.MIN_LEN_TEXT} до {Constants.MAX_LEN_TEXT}"
    )
    status: str = Field(...)
    on_website: bool = Field(...)
    category: str = Field(...)

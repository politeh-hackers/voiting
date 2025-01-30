from pydantic import BaseModel, Field
from base.constants import Constants
from datetime import date

class MediaActualFieldsSchema(BaseModel):
        slug: str = Field(
            ...,
            min_length=Constants.MIN_LEN_H1,
            max_length=Constants.MAX_LEN_H1,
            description=f"Поле должно содержать от {Constants.MIN_LEN_H1} до {Constants.MAX_LEN_H1}"
        )
        header: str = Field(
            ..., 
            min_length=Constants.MIN_LEN_HEADER, 
            max_length=Constants.MAX_LEN_HEADER, 
            description=f"Поле должно содержать от 4 до {Constants.MAX_LEN_HEADER}")
        content: str = Field(
            ..., 
            min_length=Constants.MIN_LEN_TEXT, 
            max_length=Constants.MAX_LEN_TEXT, 
            description=f"Поле должно содержать от {Constants.MIN_LEN_TEXT} до {Constants.MAX_LEN_TEXT}")
        summary: str = Field(
            ..., 
            min_length=Constants.MIN_LEN_HEADER, 
            max_length=Constants.MAX_LEN_HEADER, 
            description=f"Поле должно содержать от {Constants.MIN_LEN_HEADER} до {Constants.MAX_LEN_HEADER}")
        main_photo: str = Field(
            ..., 
            description="Главное фото должно быть обязательно")
        date_created: date = Field(
            ..., 
            description="Поле даты должно быть обязательно")
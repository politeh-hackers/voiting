from pydantic import Field, BaseModel
from base.constants import Constants
from datetime import date

class BiographySchema(BaseModel):
        header: str = Field(
            ..., 
            min_length=Constants.MIN_LEN_HEADER, 
            max_length=Constants.MAX_LEN_HEADER, 
            description=f"Поле должно содержать от {Constants.MIN_LEN_HEADER} до {Constants.MAX_LEN_HEADER}")
        content: str = Field(
            ..., 
            min_length=Constants.MIN_LEN_TEXT, 
            max_length=Constants.MAX_LEN_TEXT, 
            description=f"Поле должно содержать от {Constants.MIN_LEN_TEXT} до {Constants.MAX_LEN_TEXT}")
        main_photo: str = Field(
            ..., 
            description="Главное фото должно быть обязательно")
        date_created: date = Field(
            ..., 
            description="Поле даты должно быть обязательно")
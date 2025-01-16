from pydantic import BaseModel, Field
from base.constants import Constants


class BaseValidationSchema(BaseModel):
        # h1: str = Field(
        #     ..., 
        #     min_length=Constants.MIN_LEN_H1, 
        #     max_length=Constants.MAX_LEN_H1, 
        #     description=f"Поле должно содержать от {Constants.MIN_LEN_H1} до {Constants.MAX_LEN_H1}"
        # )
        # title: str = Field(
        #     ..., 
        #     min_length=Constants.MIN_LEN_TITLE, 
        #     max_length=Constants.MAX_LEN_TITLE, 
        #     description=f"Поле должно содержать от {Constants.MIN_LEN_TITLE} до {Constants.MAX_LEN_TITLE}"
        # )
        # description: str = Field(
        #     ..., 
        #     min_length=Constants.MIN_LEN_DESCRIPTION, 
        #     max_length=Constants.MAX_LEN_DESCRIPTION, 
        #     description=f"Поле должно содержать от {Constants.MIN_LEN_DESCRIPTION} до {Constants.MAX_LEN_DESCRIPTION}"
        # )
        header: str = Field(
                ..., 
                min_length=Constants.MIN_LEN_HEADER, 
                max_length=Constants.MAX_LEN_HEADER, 
                description=f"Поле должно содержать от 4 до {Constants.MAX_LEN_HEADER}"
            )
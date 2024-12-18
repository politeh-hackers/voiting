from pydantic import BaseModel, Field, ValidationError
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

    @staticmethod
    def format_validation_errors(e: ValidationError):
        formatted_errors = []
        for error in e.errors():
            field = '.'.join(str(loc) for loc in error['loc'])
            message = error['msg']
            formatted_errors.append({
                'field': field,
                'message': message,
                'input': error.get('input', ''),
                'context': error.get('ctx', {}),
                'url': error.get('url', '')
            })
        return formatted_errors
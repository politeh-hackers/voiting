from pydantic import BaseModel, Field

class CategorySchema(BaseModel):
        name: str = Field(
            ..., 
            min_length=4, 
            max_length=100, 
            description=f"Поле должно содержать от 4 до 100")
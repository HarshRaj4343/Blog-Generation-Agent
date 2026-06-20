from pydantic import BaseModel, Field

class BlogPlan(BaseModel):
    sections: list[str] = Field(min_length=5, max_length=7)

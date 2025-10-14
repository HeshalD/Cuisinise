from pydantic import BaseModel

class RecipeQuery(BaseModel):
    query: str
    top_k: int = 5

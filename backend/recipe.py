from pydantic import BaseModel

class Recipe(BaseModel):
    Name:str
    PrepTime:int
    NumIngredients:int
    Ingredients:list[str]
    Calories:float
    TotalFat:float
    Sugar:float 
    Sodium:float 
    Protein:float
    SaturatedFat:float
    Carbohydrates:float
    RecipeInstructions:list[str]
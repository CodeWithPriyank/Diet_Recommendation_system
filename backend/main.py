from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from model import recommend, recommend_recipes
import pandas as pd
from recipe import Recipe

data = pd.read_csv('../data/filtered_data.csv')

app = FastAPI()

class params(BaseModel):
    n_neighbors:int=5
    return_distance:bool=False

class UserInput(BaseModel):
    nutrition_input: list[float]=[]
    ingredients: list[str]=[]
    food_type:str
    params:Optional[params]

class Output(BaseModel):
    output: Optional[List[Recipe]] = None

@app.get("/")
def home():
    return {"health_check": "OK"}

@app.post("/recommend", response_model=Output)
def create_recommendations(user: UserInput):
    df = recommend(data, user.nutrition_input, user.food_type, user.ingredients, user.params.dict())
    output = recommend_recipes(df)
    if output is None:
        return {"output": None}
    else:
        return {"output": output}
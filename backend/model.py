import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from recipe import Recipe

# perform feature scaling
def scale(df):
    scaler=StandardScaler()
    data=scaler.fit_transform(df.iloc[:,7:14].to_numpy())
    return data, scaler

# utilizes the K-nearest neighbors algorithm to identify the nearest neighbors
def knn_algo(data):
    knn = NearestNeighbors(metric='cosine',algorithm='brute')
    knn.fit(data)
    return knn

# construct a pipeline model
def build_pipeline(knn,scaler,params):
    transformer = FunctionTransformer(knn.kneighbors,kw_args=params)
    pipeline=Pipeline([('std_scaler',scaler),('NN',transformer)])
    return pipeline

# filter data according to user requirements
def filter_data(df, ingredient_filter, max_nutrition, food_type):
    extract_data=df.copy()
    for column,maximum in zip(extract_data.columns[7:13],max_nutrition):
        extract_data = extract_data[extract_data[column]<maximum]
    if food_type != None:
        extract_data = extract_data[extract_data[food_type]==True]
    if ingredient_filter!=None:
        for ingredient in ingredient_filter:
            extract_data = extract_data[extract_data['ingredients'].str.contains(ingredient,regex=False)]
    return extract_data

# apply pipeline model on input data
def model_pipeline(pipeline, input, data):
    input = np.array(input).reshape(1, -1)
    return data.iloc[pipeline.transform(input)[0]]

# recommend user based on their input requirements
def recommend(df, input, food_type, ingredients=[], params={'n_neighbors':5, 'return_distance':False}):
    extract_data=filter_data(df, ingredients, input, food_type)
    if extract_data.empty:
        return None
    else:
        prep_data,scaler=scale(extract_data)
        neigh=knn_algo(prep_data)
        pipeline=build_pipeline(neigh, scaler, params)
        return model_pipeline(pipeline, input, extract_data)

# generate recommended recipes
def recommend_recipes(df):
    recipes = []
    if df is not None:
        for _,row in df.iterrows():
            recipe = Recipe(
                Name=row['name'],
                PrepTime=row['minutes'],
                NumIngredients=row['n_ingredients'],
                Ingredients=eval(row['ingredients']),
                Calories=row['calories'],
                TotalFat=row['total fat'],
                Sugar=row['sugar'],
                Sodium=row['sodium'],
                Protein=row['protein'],
                SaturatedFat=row['saturated fat'],
                Carbohydrates=row['carbohydrates'],
                RecipeInstructions=eval(row['steps'])
            )
            recipes.append(recipe.dict())
    else:
        return None
    return recipes
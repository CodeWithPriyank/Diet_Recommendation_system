import streamlit as st
import pandas as pd
import plotly.express as px
from recommender import Recommender

st.set_page_config(
    page_title="Diet Recommender System",
    page_icon=":green_salad:",
)

st.write(
    """
    # Diet Recommender System :green_salad:
    This web application utilized content-based filtering to recommend a diet plan based on the user's preferences such as calories, protein, fat, sodium and carbohydrates.
    Besides that, it could also show the nutritional information for each food items, as well as the recipes to make them. The frontend is made with
    Steamlit and the backend is built with FastAPI framework. The dataset is obtained from [Kaggle](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions?select=RAW_recipes.csv)
    which consists of 180K+ recipes covering user interactions and uploads on Food.com.
    """
)

st.write("""-----""")
st.write(
    """
    #### Content-based Filtering
    Content-based filtering is a recommendation system that suggests items based on the user's preferences. In this case, the user can input the amount of calories, protein, fat, sodium and carbohydrates they want in their diet. The recommendation engine will then suggest food items that meet the user's requirements.
    By offering personalized recommendations, a content-based food recommendation engine assists users in making healthier eating decisions and enhancing their overall well-being.
    """
)

nutritions = ['Calories', 'TotalFat', 'Sugar', 'Sodium', 'Protein', 'SaturatedFat', 'Carbohydrates']
if 'recommended' not in st.session_state:
    st.session_state.recommended = False
    st.session_state.recommendations = None

class Recommendation:
    def __init__(self, nutrition_list, ingredient, food_type, recommendations):
        self.nutrition_list=nutrition_list
        self.ingredient=ingredient
        self.food_type=food_type
        self.recommendations=recommendations
        pass

    def generate(self,):
        params = {'n_neighbors':self.recommendations, 'return_distance':False}
        ingredients = self.ingredient.split(',')
        generator = Recommender(self.nutrition_list, ingredients, self.food_type, params)
        recommend = generator.recommend()
        recommend=recommend.json()['output']
        return recommend
    
class Recipes:
    def __init__(self):
        self.nutritions=nutritions
    
    # display recommended recipes
    def recommend_recipes(self, recommendations):
        st.subheader('Recommended food & recipes: :fork_and_knife:')
        if recommendations != None:
            for recipe in recommendations:
                recipe_name = recipe['Name'].title()
                expander = st.expander(recipe_name)
                nutritions_df = pd.DataFrame({value:[recipe[value]] for value in nutritions})

                expander.markdown(f"""
                    Preparation Time: {recipe['PrepTime']}min
                """)
                expander.markdown(f'<h5 style="color:#5C61FF; text-align: center;">Nutritional Values (g):</h5>', unsafe_allow_html=True)                   
                expander.dataframe(nutritions_df)
                expander.markdown(f'<h5 style="color:#5C61FF; text-align: center;">Ingredients:</h5>', unsafe_allow_html=True)
                for ingredient in recipe['Ingredients']:
                    expander.markdown(f"""
                        - {ingredient}
                    """)
                expander.markdown(f'<h5 style="color:#5C61FF; text-align: center;">Recipe Instructions:</h5>', unsafe_allow_html=True)    
                for i, instruction in enumerate(recipe['RecipeInstructions'], start=1):
                    expander.markdown(f"""
                        {i}. {instruction.capitalize()}
                    """)
        # display message if no recipes are found
        else:
            st.error('Sorry, we couldn\'t find any matching recipes according to your input :smiling_face_with_tear:')

    # plot pie chart for nutritional values
    def plot_nutrition_pie(self, recipe):
        if recipe:
            nutritions_df = pd.DataFrame({value: [recipe[value]] for value in nutritions})
            fig = px.pie(nutritions_df.melt(), names='variable', values='value', title='Nutritional Values Percentage')
            st.plotly_chart(fig)

    # plot bar chart for nutritional values
    def plot_nutrition_bar(self, recommendations):
        if recommendations:
            data = {nutrition: [] for nutrition in nutritions}
            recipe_names = []
            for recipe in recommendations:
                recipe_names.append(recipe['Name'])
                for nutrition in nutritions:
                    data[nutrition].append(recipe[nutrition])
            df = pd.DataFrame(data, index=recipe_names)
            df = df.reset_index().melt(id_vars='index', value_vars=nutritions)
            df.columns = ['Recipe', 'Nutrient', 'Value']
            fig = px.bar(df, x='Recipe', y='Value', color='Nutrient', barmode='group', title='Comparison Of Nutritional Values Among All Recipes Recommended')
            fig.update_layout(yaxis_title="Value (g)")
            st.plotly_chart(fig)

recipes = Recipes()

# recommendation form for user to input preferred nutrition values
with st.form("recommend_form"):
    st.write("#### Enter your preferred maximum nutritional values below : ")
    Calories = st.slider("Calories", 50, 5000, 500)
    TotalFat = st.slider("Total fat", 50, 5000, 250)
    Sugar = st.slider("Sugar", 50, 5000, 1000)
    Sodium = st.slider("Sodium", 50, 5000, 450)
    Protein = st.slider("Protein", 50, 5000, 800)
    SaturatedFat = st.slider("Saturated fat", 50, 5000, 800)
    Carbohydrates = st.slider("Carbohydrates", 50, 5000, 1000)
    option = st.selectbox(
        "Which type of food would you prefer?",
        ("Non-Vegan", "Vegan", "Non-Vegan dessert", "Healthy", "Vegan dessert")
    )

    st.write("#### Recommendation Options (Optional)")
    ingredient = st.text_input('Specify the ingredients that you would like to include in the recommendations', placeholder='Eggs, Milk (separated by ",")')

    nutritions_values = [Calories, TotalFat, Sugar, Sodium, Protein, SaturatedFat, Carbohydrates]
    recommendations = st.slider("Number of recommendations", 1, 20, 5)
    recommended = st.form_submit_button("Recommend Me :)")

# display loading spinner and update session state with generated recommendations
if recommended:
    with st.spinner('Generating recommendations...'):
        recommendations = Recommendation(nutritions_values, ingredient, option, recommendations)
        recommendations = recommendations.generate()
        st.session_state.recommendations=recommendations
    st.session_state.recommended=True 

if st.session_state.recommended:
    with st.container():
        recipes.recommend_recipes(st.session_state.recommendations)

    # only display visualization if recommendations are generated
    if st.session_state.recommendations:
        st.write("### Visualization Of Nutritional Values:")
        recipe_names = [recipe['Name'] for recipe in st.session_state.recommendations]
        selected_recipe_name = st.selectbox("Select a recipe", recipe_names)

        selected_recipe = next(recipe for recipe in st.session_state.recommendations if recipe['Name'] == selected_recipe_name)
        # plot pie chart and bar chart for nutritional values
        recipes.plot_nutrition_pie(selected_recipe)
        recipes.plot_nutrition_bar(st.session_state.recommendations)
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched
import requests

st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")

cnx = st.connection("snowflake")
session = cnx.session()
fruits_df = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col("SEARCH_ON"))
pd_df = fruits_df.to_pandas()


name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

ingredients_list = st.multiselect("Choose upto 5 ingredients:", fruits_df.select(col("FRUIT_NAME")), max_selections=5)
time_to_insert = st.button("Submit Order")
my_insert_stmt = ""

if ingredients_list:
    ingredients_string = " ".join(ingredients_list)
    my_insert_stmt = f"""
    insert into smoothies.public.orders(ingredients, name_on_order)
    values ('{ingredients_string}', '{name_on_order}')
    """

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


    for fruit_chosen in ingredients_list:
        st.subheader(f"{fruit_chosen} Nutrition Information")
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{search_on}")
        st.dataframe(data = fruityvice_response.json(), use_container_width = True)




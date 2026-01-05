# # Import python packages
# import streamlit as st
# from snowflake.snowpark.functions import col
# import requests

# # Write directly to the app
# st.title(":cup_with_straw: Customize Your Smoothie:cup_with_straw:")
# st.write(
#   """Choose the fruits you want in your custom smoothie!
#   """
# )

# name_on_order = st.text_input('Name on Smoothie: ')
# st.write('The name on your smoothie will be: ', name_on_order)

# cnx = st.connection("snowflake")
# session = cnx.session()

# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# # st.dataframe(data=my_dataframe, use_container_width=True)

# ingredients_list = st.multiselect(
#     'Choose upto 5 ingredients: '
#     , my_dataframe
#     , max_selections = 5
# )

# if ingredients_list:
#     ingredients_string =''

#     for fruit_chosen in ingredients_list:
#         ingredients_string += fruit_chosen + ' '
#         st.subheader(fruit_chosen + 'Nutrition Information')
#         smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
#         sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

#     my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
#             values ('""" + ingredients_string + """','""" + name_on_order + """')"""

#     st.write(my_insert_stmt)
#     # st.stop()
    
#     time_to_insert = st.button('Submit Order')
    
#     if time_to_insert:
#         session.sql(my_insert_stmt).collect()
    
#         st.success('Your Smoothie is ordered! '+ name_on_order , icon="✅")



# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie:cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothie!
  """
)

name_on_order = st.text_input('Name on Smoothie: ')
st.write('The name on your smoothie will be: ', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

# --- BEFORE ---
# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

# --- AFTER: get a list[str] of fruit names ---  # <<< CHANGE
fruit_rows = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME")).collect()  # <<< CHANGE
fruit_options = [r["FRUIT_NAME"] for r in fruit_rows]  # e.g., ['Tangerine','Kiwi','Mango','Lime','Ximenia']  # <<< CHANGE

# Use the list of strings in the multiselect  # <<< CHANGE
ingredients_list = st.multiselect(
    'Choose upto 5 ingredients: ',
    fruit_options,                 # <<< CHANGE (was my_dataframe)
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        # Cosmetic: add a space before 'Nutrition Information'  # (optional)
        st.subheader(fruit_chosen + ' Nutrition Information')

        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen, ' is ', search_on, '.')
        
        # Normalize the path a bit (strip spaces); optional but helpful  # <<< CHANGE
        fruit_path = fruit_chosen.strip()  # <<< CHANGE
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_path)

        # Display one table per fruit (this stays inside the loop)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    # Trim trailing space in the ingredients string  # <<< CHANGE
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string.strip() + """','""" + name_on_order + """')"""  # <<< CHANGE

    st.write(my_insert_stmt)
    # st.stop()

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! ' + name_on_order, icon="✅")









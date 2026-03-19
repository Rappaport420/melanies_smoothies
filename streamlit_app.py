# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests  
#from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title("Custome Smothies or whatever...")

cnx = st. connection("snowflake")
session = cnx. session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)

smoothie_name = st.text_input("Name on Smoothie")
st.write("Name on Smoothie will be: ", smoothie_name)

ingedient_list = st.multiselect(
    "Choose 5 ingredientes",
    my_dataframe,
    max_selections= 5,
)


if ingedient_list:
    #st.write("You selected:", ingedient_list)
    #st.text(ingedient_list)
    string_fruits = ''

    for chosen_fruit in ingedient_list:
        string_fruits += chosen_fruit + ' '
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{chosen_fruit}")  
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    #st.write(string_fruits)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + string_fruits + """', '""" + smoothie_name + """')"""

    #st.write(my_insert_stmt)
    #st.stop()

    #st.write(my_insert_stmt)

    time_to_insert = st.button('Submit')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")



        

        

    

    
        




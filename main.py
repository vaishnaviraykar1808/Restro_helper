import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

st.title(":female-cook: Restaurant Name Generator")
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")

def generate_restaurant_name_and_items(cuisine):
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    prompt_template_name = PromptTemplate(
        input_variables=['cuisine'],
        template="""I want to open a resturant for {cuisine} food. Suggest a fency name for this."""
    )
    name_chain = LLMChain(llm=llm, prompt=prompt_template_name,output_key="restaurant_name")

    prompt_template_item = PromptTemplate(input_variables=['restaurant_name'],
    template="""Suggest some menu items for {restaurant_name}. Return it is as a comma separated list."""
    )

    food_items_chain = LLMChain(llm=llm, prompt=prompt_template_item, output_key="menu_items")
    
  
    chain = SequentialChain(
    chains=[name_chain, food_items_chain],
    input_variables=['cuisine'],
    output_variables=['restaurant_name', 'menu_items'])
    response = chain({'cuisine': cuisine}) 
    return response

with st.form("myform"):
    cuisine=st.text_input('''Enter Restaurent Type''')
    st.caption('For eg - Indian , Street Food , Chinease')
    submitted = st.form_submit_button("Submit")
    
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        response=generate_restaurant_name_and_items(cuisine)
        st.header(response['restaurant_name'].strip())
        menu_items=response['menu_items'].strip().split(",")
        st.write("Menu Items :")
        for item in menu_items:
            st.write("🔸",item)
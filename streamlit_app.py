import streamlit as st          
import altair as alt          
import pandas as pd          

st.title("IS445 HW6: Illinois State Building Inventory")             

URL = "https://raw.githubusercontent.com/UIUC-iSchool-DataViz/is445_data/main/building_inventory.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(URL)          
    df = df[(df["Year Constructed"] > 1800) & (df["Square Footage"] >0)]
    return df                

df = load_data()
st.write("Number of buildings:", len(df))

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

st.header("Which counties have the most state building space?")

options = ["All"] + sorted(df["Usage Description"].unique().tolist())
choice = st.selectbox("Choose a usage type:", options)

if choice == "All":
    sub = df
else:
    sub = df[df["Usage Description"] == choice]

county = sub.groupby("County", as_index=False)["Square Footage"].sum()
county = county.sort_values("Square Footage", ascending=False).head(15)

chart_b = alt.Chart(county).mark_bar().encode(
    x=alt.X("Square Footage:Q", title="Total Square Footage"),
    y=alt.Y("County:N", sort="-x", title="County"),
    tooltip=["County", "Square Footage"]
)
st.altair_chart(chart_b, use_container_width=True)

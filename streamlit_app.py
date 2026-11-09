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
st.write("For this visualization, I wanted to show which Illinois counties hold the most state building space. I was surprised to see that Champaign County ranks second, right behind Cook County, and I think this is mostly because of the University of Illinois campus. I used a horizontal bar chart because some county names are long and are easier to read on the y axis. I also sorted the bars from largest to smallest so the ranking is clear right away, and I only showed the top 15 counties since there are over 100 counties and showing all of them would make the chart too crowded. The dropdown menu lets the viewer filter by usage type to see how the ranking changes for different kinds of buildings. If I had more time, I would like to turn this into a map of Illinois so the viewer can see where the space is located geographically.")
st.altair_chart(chart_b, use_container_width=True)
st.header("When were state buildings built, and what are they used for?")
st.write("Drag across the top chart to select decades. The bottom chart updates.")

df["Decade"] = (df["Year Constructed"] // 10) * 10

brush = alt.selection_interval(encodings=["x"])

top = alt.Chart(df).mark_bar().encode(
    x=alt.X("Decade:O", title="Decade Constructed"),
    y=alt.Y("count():Q", title="Number of Buildings")
).add_params(brush)

bottom = alt.Chart(df).mark_bar(color="orange").encode(
    x=alt.X("sum(Square Footage):Q", title="Total Square Footage"),
    y=alt.Y("Usage Description:N", sort="-x", title="Usage Type"),
    tooltip=["Usage Description", "sum(Square Footage)"]
).transform_filter(brush)

st.altair_chart(alt.vconcat(top, bottom), use_container_width=True)
st.write("This visualization shows when Illinois state buildings were built and what they are used for. The top chart shows that the most buildings were constructed in the 1970s, and the number drops sharply in the 2010s. When I dragged over the 1960s and 1970s, the bottom chart showed that Assembly buildings had the largest total square footage in that period. I used an ordinal axis for the decades because they have a natural order. I also used different colors for the two charts, blue for the number of buildings and orange for square footage, so it is clear that they show different measures. I added the drag selection so the viewer can pick a time period and compare the building types directly. If I had more time, I would change the bottom chart to show percentages so it is easier to compare different decades, and I would like to explore the data further.")

st.header("Overlap with Homework #5")
st.write("My Homework #5 used the UFO sightings dataset. This homework uses a different dataset (the Illinois building inventory) and different plots, so no plots or text are reused from Homework #5.")

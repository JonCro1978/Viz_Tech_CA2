import streamlit as st
import pandas as pd
import plotly.express as px


# Setting up the title page 


st.set_page_config(
    page_title="Fremont Bridge Dashboard",
    page_icon="🚴",
    layout="wide"
)

#setting the data frame and to columns to be read & the totals 

DATE_COLUMN = "Date"

DATA_PATH = r"C:\Users\unake\OneDrive\Desktop\JCCCTstuff\Fremont_Bridge_Bicycle_Counter.csv"

TOTAL_COL = "Fremont Bridge Sidewalks, south of N 34th St Total"
WEST_COL = "Fremont Bridge Sidewalks, south of N 34th St Cyclist West Sidewalk"
EAST_COL = "Fremont Bridge Sidewalks, south of N 34th St Cyclist East Sidewalk"


# Loadin the data to the cache, so that the app does not re-read the app every time the app re-runs 
#removal of unwanted spaces from the colums 
#tidying up the date field to datetime type to extract hour, month and year

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip()
    df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN])

    # Create a Total column
    df["Total"] = df[WEST_COL] + df[EAST_COL]

    return df


data = load_data()

# Titles

st.title("🚴 Fremont Bridge Bicycle Dashboard")

st.write(
    "Interactive dashboard showing hourly, monthly and yearly bicycle crossings."
)


# Checkbox to show hide raw data frame


if st.checkbox("Show Raw Data"):
    st.write(data)


# Setting the page up into 3 columns on the first row to show the widgets and labeling same 

col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(data))
col2.metric("Total Crossings", f"{int(data['Total'].sum()):,}")
col3.metric("Average Hourly Crossings", round(data["Total"].mean(), 1))

#First divider - mid section 

st.divider()

# Hourly average code, setting hourly group and datetime to hour, creating average 

hourly = (
    data.groupby(data[DATE_COLUMN].dt.hour)["Total"]
    .mean()
    .reset_index()
)

#Plotly express creating the bar chart

fig_hour = px.bar(
    hourly,
    x="Date",
    y="Total",
    title="Average Bicycle Crossings by Hour",
    color="Total",
    color_continuous_scale="Viridis"
)

fig_hour.update_layout(
    xaxis_title="Hour",
    yaxis_title="Average Crossings"
)

# Monthly crossings area set up 


data["Month"] = data[DATE_COLUMN].dt.month

monthly = (
    data.groupby("Month")["Total"]
    .sum()
    .reset_index()
)
#Plotly express area chart

fig_month = px.area(
    monthly,
    x="Month",
    y="Total",
    title="Monthly Bicycle Crossings",
    color_discrete_sequence=["green"]
)

fig_month.update_layout(
    xaxis_title="Month",
    yaxis_title="Total Crossings"
)

#Yearly data 

data["Year"] = data[DATE_COLUMN].dt.year

yearly = (
    data.groupby("Year")["Total"]
    .sum()
    .reset_index()
)


#Code for plotly 

fig_year = px.line(
    yearly,
    x="Year",
    y="Total",
    markers=True,
    title="Yearly Bicycle Crossings"
)

fig_year.update_traces(line=dict(width=4))

#East vs West line graph
#Grouped data by data column by datetime hour, east and west sidewalk data sets

eastwest = (
    data.groupby(data[DATE_COLUMN].dt.hour)[[WEST_COL, EAST_COL]]
    .mean()
    .reset_index()
)

fig_side = px.line(
    eastwest,
    x="Date",
    y=[WEST_COL, EAST_COL],
    title="Average Crossings by Sidewalk"
)

#Dashboard layout design, setting the columns for the widgets to sit in, divider then lower row columns

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_hour, use_container_width=True)

with col2:
    st.plotly_chart(fig_month, use_container_width=True)

st.divider()

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(fig_year, use_container_width=True)

with col4:
    st.plotly_chart(fig_side, use_container_width=True)

#Data Summary details & addition of the checkbox 

if st.checkbox("Show Dataset Summary"):
    st.write(data.describe())

#Data description columns from the values below:
value_cols = [
    "Fremont Bridge Sidewalks, south of N 34th St Total",
    "Fremont Bridge Sidewalks, south of N 34th St Cyclist West Sidewalk",
    "Fremont Bridge Sidewalks, south of N 34th St Cyclist East Sidewalk"
]

#Making the long dataframe for the graph to span the dashbaord, date remains the key field, setting the X and Y axis 
long_df = data.melt(
    id_vars="Date",
    value_vars=value_cols,
    var_name="Channel",
    value_name="Crossings"
)

fig = px.line(
    long_df,
    x="Date",
    y="Crossings",
    color="Channel",
    markers=False,
    title="Crossings by sidewalk over time"
)

fig.update_layout(
    xaxis_title="Date and time",
    yaxis_title="Crossings",
    legend_title="Series"
)

st.plotly_chart(fig, use_container_width=True)

# df has columns: "date", "channel", "count"

#References

#https://www.geeksforgeeks.org/change-color-of-bars-in-matplotlib-bar-chart
#https://www.geeksforgeeks.org/python-plotly-tutorial
#https://www.geeksforgeeks.org/python/introduction-to-streamlit-in-python
#https://plotly.com/python/plotly-express
#https://docs.streamlit.io/develop/api-reference/charts/st.plotly_chart
#https://plotly.com/python/plotly-express
#https://plotly.com/python/bar-charts
#https://plotly.com/python/line-charts
#https://plotly.com/python/line-charts
#https://plotly.com/python/filled-area-plots

#UXD for YOUNG ADULTS 
#1.	Define goals, directions and instructions explicitly 
#2.	Rely more on search than discovery; make things handy 
#3.	Usability and accessibility are critical, but that doesn’t mean the Visualization can’t be clever! 
#4.	Lay lesser emphasis on research and study; get to the answers quickly 



import streamlit as st
import pandas as pd
from database import db_conn

# Function to fetch data using parameterized queries
def get_data_from_db(query, params=None):
    conn = db_conn()
    cursor = conn.cursor()
    cursor.execute(query, params)  # Using parameterized queries
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

# Function to display filtered competitors data
def display_filtered_data(country=None, min_rank=None, max_rank=None, min_points=None):
    query = """
    SELECT c.name, c.country, cr.ranking, cr.points, cr.competetions_played
    FROM competitors c
    JOIN competitor_rankings cr ON c.competitor_id = cr.competitor_id
    WHERE 1=1
    """
    params = []
    
    # Adding filters to the query
    if country and country != "All":
        query += " AND c.country = %s"
        params.append(country)
    if min_rank:
        query += " AND cr.ranking >= %s"
        params.append(min_rank)
    if max_rank:
        query += " AND cr.ranking <= %s"
        params.append(max_rank)
    if min_points:
        query += " AND cr.points >= %s"
        params.append(min_points)
    
    data = get_data_from_db(query, tuple(params))  # Ensure params are passed as tuple
    df = pd.DataFrame(data, columns=["Name", "Country", "Rank", "Points", "Competitions Played"])
    st.dataframe(df)
    
    return df

# Streamlit UI
st.title("Search and Filter Competitors")

# Filter by Country (Dropdown)
country_query = "SELECT DISTINCT country FROM competitors"
countries = [country[0] for country in get_data_from_db(country_query)]
country = st.selectbox("Select Country", ["All"] + countries)

# Filter by Rank Range
min_rank = st.number_input("Min Rank", min_value=1, max_value=1000, value=1, step=1)
max_rank = st.number_input("Max Rank", min_value=1, max_value=1000, value=1000, step=1)

# Filter by Points
min_points = st.number_input("Min Points", min_value=0, max_value=10000, value=0, step=10)

# Display filtered data
df = display_filtered_data(country if country != "All" else None, min_rank, max_rank, min_points)


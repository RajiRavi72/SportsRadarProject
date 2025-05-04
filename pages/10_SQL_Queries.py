import streamlit as st
import pandas as pd
from database import db_conn
 

conn = db_conn()

# Utility function to execute queries and return DataFrame
def run_query(query):
    return pd.read_sql(query, conn)

st.title("📊 SQL Query Explorer")
st.write("Explore predefined SQL queries with dynamic filters and visualizations.")

# 1. Using Categories and Competitions
st.header("📁 Categories & Competitions")

with st.expander("1. List all competitions with their category name"):
    query = """
        SELECT c.competition_name, cat.category_name
        FROM Competitions c
        JOIN Categories cat ON c.category_id = cat.category_id
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

with st.expander("2. Count competitions per category"):
    query = """
        SELECT cat.category_name, COUNT(*) AS competition_count
        FROM Competitions c
        JOIN Categories cat ON c.category_id = cat.category_id
        GROUP BY cat.category_name
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

with st.expander("3. All competitions of type 'doubles'"):
    query = "SELECT * FROM Competitions WHERE type = 'doubles'"
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

with st.expander("4. Competitions in selected category"):
    categories_df = run_query("SELECT DISTINCT category_name FROM Categories ORDER BY category_name;")
    category_list = categories_df['category_name'].tolist()
    selected_category = st.selectbox("Select Category", category_list, key="cat_filter")

    query = """
        SELECT c.competition_name
        FROM Competitions c
        JOIN Categories cat ON c.category_id = cat.category_id
        WHERE cat.category_name = %s
    """
    df = pd.read_sql(query, conn, params=[selected_category])
    st.dataframe(df, use_container_width=True)

with st.expander("5. Parent competitions and their sub-competitions"):
    query = """
        SELECT parent.competition_name AS parent_name, child.competition_name AS sub_competition
        FROM Competitions child
        JOIN Competitions parent ON child.parent_id = parent.competition_id
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

with st.expander("6. Distribution of competition types by category"):
    query = """
        SELECT cat.category_name, c.type, COUNT(*) AS count
        FROM Competitions c
        JOIN Categories cat ON c.category_id = cat.category_id
        GROUP BY cat.category_name, c.type
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

with st.expander("7. Top-level competitions (no parent)"):
    query = "SELECT * FROM Competitions WHERE parent_id IS NULL"
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

# 2. Complexes & Venues
st.header("🏟️ Complexes & Venues")

with st.expander("1. All venues with their complex name"):
    query = """
        SELECT v.venue_name, c.complex_name
        FROM Venues v
        JOIN Complexes c ON v.complex_id = c.complex_id
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

with st.expander("2. Venue count per complex"):
    query = """
        SELECT c.complex_name, COUNT(*) AS venue_count
        FROM Venues v
        JOIN Complexes c ON v.complex_id = c.complex_id
        GROUP BY c.complex_name
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

with st.expander("3. Venues in selected country"):
    country_df = run_query("SELECT DISTINCT country_name FROM Venues ORDER BY country_name;")
    country_list = country_df['country_name'].dropna().tolist()
    selected_country = st.selectbox("Select Country", country_list, key="venue_country")

    query = "SELECT * FROM Venues WHERE country_name = %s"
    df = pd.read_sql(query, conn, params=[selected_country])
    st.dataframe(df, use_container_width=True)

with st.expander("4. Venues and their timezones"):
    query = "SELECT venue_name, country_name, time_zone FROM Venues"
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

with st.expander("5. Complexes with more than one venue"):
    query = """
        SELECT c.complex_name, COUNT(*) AS venue_count
        FROM Venues v
        JOIN Complexes c ON v.complex_id = c.complex_id
        GROUP BY c.complex_name
        HAVING venue_count > 1
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

with st.expander("6. Venues grouped by country"):
    query = "SELECT country_name, COUNT(*) AS venue_count FROM Venues GROUP BY country_name"
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

with st.expander("7. Venues for selected complex"):
    complex_df = run_query("SELECT DISTINCT complex_name FROM Complexes ORDER BY complex_name;")
    complex_list = complex_df['complex_name'].dropna().tolist()
    selected_complex = st.selectbox("Select Complex", complex_list, key="complex_filter")

    query = """
        SELECT v.venue_name 
        FROM Venues v 
        JOIN Complexes c ON v.complex_id = c.complex_id 
        WHERE c.complex_name = %s
    """
    df = pd.read_sql(query, conn, params=[selected_complex])
    st.dataframe(df, use_container_width=True)

# 3. Rankings & Competitors
st.header("🏅 Rankings & Competitors")

with st.expander("1. All competitors with their rank and points"):
    query = """
        SELECT c.name, r.ranking, r.points
        FROM Competitor_Rankings r
        JOIN Competitors c ON r.competitor_id = c.competitor_id
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

with st.expander("2. Top 5 ranked competitors"):
    query = """
        SELECT c.name, r.ranking
        FROM Competitor_Rankings r
        JOIN Competitors c ON r.competitor_id = c.competitor_id
        WHERE r.ranking <= 5
        ORDER BY r.ranking
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

with st.expander("3. Competitors with stable rank (movement = 0)"):
    query = """
        SELECT c.name, r.ranking, r.movement
        FROM Competitor_Rankings r
        JOIN Competitors c ON r.competitor_id = c.competitor_id
        WHERE r.movement = 0
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

with st.expander("4. Total points by selected country"):
    country_df = run_query("SELECT DISTINCT country FROM Competitors WHERE country IS NOT NULL ORDER BY country;")
    competitor_country = st.selectbox("Select Country", country_df['country'], key="competitor_country")

    query = """
        SELECT SUM(r.points) AS total_points
        FROM Competitor_Rankings r
        JOIN Competitors c ON r.competitor_id = c.competitor_id
        WHERE c.country = %s
    """
    df = pd.read_sql(query, conn, params=[competitor_country])
    st.dataframe(df, use_container_width=True)

with st.expander("5. Competitor count per country"):
    query = "SELECT country, COUNT(*) AS count FROM Competitors GROUP BY country"
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

with st.expander("6. Competitor(s) with highest points"):
    query = """
        SELECT c.name, r.points
        FROM Competitor_Rankings r
        JOIN Competitors c ON r.competitor_id = c.competitor_id
        WHERE r.points = (SELECT MAX(points) FROM Competitor_Rankings)
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

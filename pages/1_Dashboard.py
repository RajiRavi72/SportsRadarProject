import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from database import db_conn
 

# Streamlit page config
st.set_page_config(page_title="Tennis Dashboard", layout="wide")

st.title("🎾 Tennis Analytics Dashboard")

# Fetch summary statistics
def get_summary_stats():
    conn =  db_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM competitors;")
    total_competitors = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT country) FROM competitors;")
    total_countries = cursor.fetchone()[0]

    cursor.execute("""
        SELECT MAX(points) FROM competitor_rankings;
    """)
    max_points = cursor.fetchone()[0]

    conn.close()
    return total_competitors, total_countries, max_points

# Country-wise competitor count
def get_country_competitor_distribution():
    conn =  db_conn()
    query = """
        SELECT country, COUNT(*) as count
        FROM competitors
        GROUP BY country
        ORDER BY count DESC
        LIMIT 15;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df.rename(columns={"count": "Competitor Count", "country": "Country"})

# Top competitors by points
def get_top_competitors():
    conn =  db_conn()
    query = """
        SELECT c.name AS Name, cr.points AS Points
        FROM competitors c
        JOIN competitor_rankings cr ON c.competitor_id = cr.competitor_id
        ORDER BY cr.points DESC
        LIMIT 10;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Main dashboard
total_competitors, total_countries, max_points = get_summary_stats()

# Display metrics
col1, col2, col3 = st.columns(3)
col1.metric("👥 Total Competitors", total_competitors)
col2.metric("🌍 Countries Represented", total_countries)
col3.metric("🏆 Highest Points", max_points)

st.markdown("---")

# Charts
col4, col5 = st.columns(2)

# Competitors by country (top 15)
with col4:
    st.subheader("Top 15 Countries by Number of Competitors")
    country_df = get_country_competitor_distribution()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(
        x="Competitor Count", 
        y="Country", 
        data=country_df, 
        ax=ax, 
        hue="Country", 
        palette="viridis", 
        legend=False
    )
    st.pyplot(fig)

# Top 10 competitors by points
with col5:
    st.subheader("Top 10 Competitors by Points")
    top_competitors_df = get_top_competitors()
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.barplot(
        x="Points", 
        y="Name", 
        data=top_competitors_df, 
        ax=ax2, 
        hue="Name", 
        palette="coolwarm", 
        legend=False
    )
    st.pyplot(fig2)
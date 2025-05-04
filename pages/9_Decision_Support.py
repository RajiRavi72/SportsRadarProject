import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from database import db_conn

st.title("🎯 Decision Support")
st.markdown("""
This page offers strategic insights using data to assist in making informed decisions about player performance and tournament dynamics.
""")

# Filters
st.subheader("🔍 Apply Filters")
col1, col2 = st.columns(2)

conn = db_conn()

# Get filter options from DB
countries = pd.read_sql("SELECT DISTINCT country FROM competitors ORDER BY country", conn)['country'].tolist()
selected_country = col1.selectbox("Filter by Country", options=["All"] + countries)

# Apply filters to SQL queries
country_filter = f"WHERE c.country = '{selected_country}'" if selected_country != "All" else ""

# Most Stable Competitors (Movement = 0)
st.subheader("📌 Most Stable Competitors (No Rank Movement) for the selected country")
st.markdown("These are competitors whose ranks have not changed recently (movement = 0).")
query_stable = f'''
SELECT c.name AS Competitor, cr.movement AS Movement
FROM competitors c
JOIN competitor_rankings cr ON c.competitor_id = cr.competitor_id
{country_filter} AND cr.movement = 0
ORDER BY cr.points DESC
LIMIT 10;
'''.replace("WHERE  AND", "WHERE")  # Handle edge case when country_filter is empty


stable_df = pd.read_sql(query_stable, conn) 

if stable_df.empty:
    st.info("No stable competitors found (Movement = 0).")
else:
    names = stable_df['Competitor'].tolist()
    st.write("These competitors have not changed in ranking recently:")
    for name in names:
        st.markdown(f"**{name}**")

# Highest Point Earners
st.subheader("🏅 Top 10 Highest Point Earners for the selected country")
query_points = f'''
SELECT c.name AS Competitor, cr.points AS Points
FROM competitors c
JOIN competitor_rankings cr ON c.competitor_id = cr.competitor_id
{country_filter}
ORDER BY cr.points DESC
LIMIT 10;
'''
points_df = pd.read_sql(query_points, conn)

if points_df.empty:
    st.info("No competitors found for the selected country.")
else:
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    sns.barplot(y="Competitor", x="Points",hue="Points", data=points_df, ax=ax1, palette="flare", legend = False)
    ax1.set_title("Top 10 Competitors by Points for the selected country")
    st.pyplot(fig1)

conn.close()

# Highest Competitions Played
st.subheader("🏅 Top 10 Highest Competitions Played for the selected country")
query_points = f'''
SELECT c.name AS Competitor, cr.competetions_played AS NumOfCompetitions
FROM competitors c
JOIN competitor_rankings cr ON c.competitor_id = cr.competitor_id
{country_filter}
ORDER BY cr.competetions_played DESC
LIMIT 10;
'''
conn = db_conn()
NumOfCompetetions_df = pd.read_sql(query_points, conn)
conn.close()

if NumOfCompetetions_df.empty:
    st.info("No competitors found for the selected country.")
else:
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.barplot(y="Competitor", x="NumOfCompetitions",hue="NumOfCompetitions", data=NumOfCompetetions_df, ax=ax2, palette="flare", legend = False)
    ax2.set_title("Top 10 Competitors by Number of Competitions Played for the selected countryr")
    st.pyplot(fig2)



# --- Top 10 Complexes with Highest Number of Venues ---
st.subheader("Top 10 Complexes with the Most Venues for the selected country")
venue_country_filter = f"WHERE v.country_name = '{selected_country}'" if selected_country != "All" else ""

# SQL query
query = f"""
SELECT 
    cx.complex_name AS Complex, 
    COUNT(v.venue_id) AS VenueCount
FROM complexes cx
JOIN venues v ON cx.complex_id = v.complex_id
{venue_country_filter}
GROUP BY cx.complex_id, cx.complex_name
ORDER BY VenueCount DESC
LIMIT 10;
""".replace("WHERE  AND", "WHERE")

# Execute and fetch
conn = db_conn()
df_complexes = pd.read_sql(query, conn)
conn.close()

# Plot
if df_complexes.empty:
    st.info("No venues found for the selected filter.")
else:
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=df_complexes, x='VenueCount', y='Complex',hue='VenueCount', palette='crest', ax=ax, legend = False)
    ax.set_title("Top 10 Complexes with Most Venues for the selected Filter")
    ax.set_xlabel("Number of Venues")
    ax.set_ylabel("Complex")
    st.pyplot(fig)


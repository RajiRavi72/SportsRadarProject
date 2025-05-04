import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from database import db_conn

# Title
st.title("🏆 Leaderboards")

# Query: Top-Ranked Competitors
def get_top_ranked_competitors():
    conn =  db_conn()
    query = """
        SELECT c.name, c.country, r.ranking, r.points
        FROM competitor_rankings r
        JOIN competitors c ON r.competitor_id = c.competitor_id
        ORDER BY r.ranking ASC
        LIMIT 10
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Query: Competitors with Highest Points
def get_highest_points_competitors():
    conn =  db_conn()
    query = """
        SELECT c.name, c.country, r.points, r.ranking
        FROM competitor_rankings r
        JOIN competitors c ON r.competitor_id = c.competitor_id
        ORDER BY r.points DESC
        LIMIT 10
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Top Ranked
st.subheader("📊 Top-Ranked Competitors")
ranked_df = get_top_ranked_competitors()
st.dataframe(ranked_df)

# Bar Chart - Top Ranked
fig1, ax1 = plt.subplots()
sns.barplot(y="name", x="ranking", hue="ranking", data=ranked_df, ax=ax1, palette="crest", legend=False)
ax1.set_xlabel("Ranking")
ax1.set_ylabel("Competitor")
ax1.invert_yaxis()
st.pyplot(fig1)

# Highest Points
st.subheader("💯 Competitors with Highest Points")
points_df = get_highest_points_competitors()
st.dataframe(points_df)

# Bar Chart - Highest Points
fig2, ax2 = plt.subplots()
sns.barplot(y="name", x="points", hue="points", data=points_df, ax=ax2, palette="flare", legend=False)
ax2.set_xlabel("Points")
ax2.set_ylabel("Competitor")
ax2.invert_yaxis()
st.pyplot(fig2)

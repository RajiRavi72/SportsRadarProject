import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from database import db_conn
 

st.set_page_config(page_title="Country-wise Analysis", layout="wide")
st.title("🌍 Country-wise Competitor Analysis")

# Get data
def get_country_stats():
    conn =db_conn()
    query = """
        SELECT country, COUNT(*) AS competitor_count, 
               ROUND(AVG(cr.points), 2) AS avg_points
        FROM competitors c
        JOIN competitor_rankings cr ON c.competitor_id = cr.competitor_id
        GROUP BY country
        ORDER BY competitor_count DESC
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = get_country_stats()

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filters")
selected_country = st.sidebar.selectbox("Select a Country", ["All"] + sorted(df["country"].unique()))
top_n = st.sidebar.slider("Top N Countries to Display", min_value=5, max_value=len(df), value=10)

# Apply filters
if selected_country != "All":
    filtered_df = df[df["country"] == selected_country]
else:
    filtered_df = df.nlargest(top_n, 'competitor_count')

# Show table
st.dataframe(filtered_df, use_container_width=True)

# --- Visualization ---
st.subheader("📊 Competitor Count by Country")
fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(data=filtered_df, x="competitor_count", hue="competitor_count", y="country", ax=ax1, palette="Blues_d")
ax1.set_xlabel("Competitor Count")
ax1.set_ylabel("Country")
for container in ax1.containers:
    ax1.bar_label(container, label_type='edge', fontsize=8)
st.pyplot(fig1)

df_sorted = filtered_df.sort_values(by='avg_points', ascending=False)
st.subheader("📈 Average Points by Country")
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(data=df_sorted, x="avg_points", hue= "avg_points",y="country", ax=ax2, palette="Purples_d")
ax2.set_xlabel("Average Points")
ax2.set_ylabel("Country")
for container in ax2.containers:
    ax2.bar_label(container, label_type='edge', fontsize=8)
st.pyplot(fig2)

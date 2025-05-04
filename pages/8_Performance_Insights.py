import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from database import db_conn

# Set page configuration
st.set_page_config(page_title="Performance Insights", layout="wide")

st.title("🎾 Performance Insights: Singles vs Doubles Participation")


# Fetch participation data
def fetch_participation_data():
    conn =  db_conn()
    cursor = conn.cursor()

    query = """
        SELECT
            comp.gender,
            comp.type AS competition_type,
            COUNT(DISTINCT cr.competitor_id) AS participant_count
        FROM competitor_rankings cr
        JOIN competitions comp ON cr.competitor_id = comp.competition_id
        GROUP BY comp.gender, comp.type
        ORDER BY comp.gender, comp.type
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    df = pd.DataFrame(rows, columns=["Gender", "Competition Type", "Participants"])
    return df

# Plotting function
def plot_participation(df):
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data=df, x="Competition Type", y="Participants", hue="Gender", palette="Set2")
    ax.set_title("Participation by Gender and Competition Type")
    ax.set_ylabel("Number of Participants")
    ax.set_xlabel("Competition Type")
    plt.tight_layout()
    st.pyplot(plt)

# Main
try:
    data_df = fetch_participation_data()
    st.dataframe(data_df, use_container_width=True)

    st.subheader("📊 Visual Insights")
    plot_participation(data_df)

except Exception as e:
    st.error(f"An error occurred: {e}")

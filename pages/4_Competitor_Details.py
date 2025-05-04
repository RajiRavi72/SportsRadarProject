import streamlit as st
import pandas as pd
from database import db_conn
 

conn = db_conn()
cursor = conn.cursor(dictionary=True)

st.set_page_config(page_title="Competitor Details Viewer")
st.title("🎾 Competitor Details Viewer")

# Fetch merged competitor data
query = """
SELECT 
    c.competitor_id,
    c.name,
    c.country,
    c.country_code,
    c.abbreviation,
    r.ranking,
    r.movement,
    r.points,
    r.competetions_played
FROM competitors c
LEFT JOIN competitor_rankings r ON c.competitor_id = r.competitor_id;
"""
cursor.execute(query)
rows = cursor.fetchall()
df = pd.DataFrame(rows)

# Dropdown to select a competitor
competitor_name = st.selectbox("Select a Competitor", df["name"].unique())

# Show details for the selected competitor
comp_data = df[df["name"] == competitor_name].iloc[0]

st.subheader("📋 Competitor Profile")
st.markdown(f"""
- **Name**: {comp_data['name']}
- **Country**: {comp_data['country']} ({comp_data['country_code']})
- **Abbreviation**: {comp_data['abbreviation']}
- **Ranking**: {comp_data['ranking']}
- **Points**: {comp_data['points']}
- **Competitions Played**: {comp_data['competetions_played']}
- **Movement**: {comp_data['movement']}
""")

import streamlit as st
st.set_page_config(page_title="Tennis Game Analytics Project", layout="wide")

st.title("🎾 Tennis Game Analytics Project Introduction")

# Problem Statement


st.header("🧠 Game Analytics: Unlocking Tennis Data with SportRadar API")
st.markdown("""
The project aims to develop a comprehensive solution for managing, visualizing, and analyzing tennis competition data sourced from the **SportRadar API**.

This application:
- Parses raw JSON data from the API,
- Stores it in a structured MySQL database, and
- Provides intuitive and interactive insights through visualizations and SQL analysis.
""")
st.subheader("🔄 Data Pipeline Overview")
st.graphviz_chart("""
digraph {
    API -> "Raw JSON"
    "Raw JSON" -> "MySQL DB"
    "MySQL DB" -> "Streamlit App"
    "Streamlit App" -> "Visuals & Insights"
}
""")
st.markdown("""
The tool is designed to help:
- **Sports enthusiasts** understand tournament structures,
- **Analysts** uncover event trends, and
- **Organizations** make data-driven decisions.
""")

# Business Use Cases
st.header("💼 Business Use Cases")

st.markdown("""
1. **🔍 Event Explorer**  
   Enable users to explore and navigate the hierarchy of competitions — for example, viewing all events under a major tournament like *ATP Vienna*.  
   This helps users understand how parent-child relationships exist between events.

   Visualize the distribution of events based on various parameters such as:
   - Event type (singles/doubles)
   - Gender (men/women)
   - Competition level (ATP, WTA, ITF, etc.)  
   These insights help spot seasonal patterns or shifts in participation.

3. **📈 Performance Insights**  
   Analyze player participation across singles and doubles formats to understand:
   - Event overlap,
   - Player specialization,
   - Popularity of certain formats.

4. **🧩 Decision Support**  
   Provide actionable insights to:
   - Sports bodies,
   - Organizers, or
   - Sponsors  
   for better **resource allocation**, **scheduling**, and **marketing strategies**.
""")

# Features
st.header("✨ Special Features of the Application")
st.markdown("""
 
1.	**Dashboard:**
○	Summary statistics like:
■	Total number of competitors.
■	Number of countries represented.
■	Highest points scored by a competitor.
            
2.	**Search and Filter Competitors:**
○	Allow users to search for a competitor by name.
■	Filtering competitors by rank range, country, or points threshold.
            
3.	**Competitor Details Viewer:**
○	Displaying detailed information about a selected competitor, including:
■	Rank, movement, competitions played, and country.
            
4.	**Country-Wise Competitor Analysis:**
○	List of countries with the total number of competitors and their average points.
            
5.	**Leaderboards:** 
■	Top-ranked competitors.
■	Competitors with the highest points.


""")


st.title("👤 Creator Information")

st.markdown("""
- **Name:** Rajalakshmi Ravishankar  
- **Course:** IIT-M Pravartak AI/ML  
- **Project:** Game Analytics : Unlocking Tennis Data using SportRadar API  
- **GitHub/LinkedIn:** https://www.linkedin.com/in/rajalakshmi-ravishankar/  
""")
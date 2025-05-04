# 🎾 Game Analytics: Unlocking Tennis Data with SportRadar API

## 📌 Overview
This Streamlit application provides interactive insights into professional tennis using real-time data from the **SportRadar API**. It empowers analysts, coaches, and fans with tools to explore events, rankings, venues, and trends—all in one dashboard.

---

## 🚀 Features

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

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io)  
- **Backend**: Python, MySQL  
- **Visualization**: Seaborn, Matplotlib  
- **Data Source**: [SportRadar API](https://developer.sportradar.com/)

---

## 🗃️ Database Schema

Key tables used:
- `competitors`
- `competitor_rankings`
- `competitions`
- `categories`
- `venues`
- `complexes`

---

## 📦 Installation & Running Locally

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/tennis-analytics.git
    cd tennis-analytics
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up your database:**

   - Ensure your MySQL server is running.
   - Update your `database.py` connection credentials accordingly.
   - Load the schema and data from your SQL files (if provided).

4. **Launch the app:**

    ```bash
    streamlit run Home.py
    ```

---

## 📸 Screenshots

| 📍 Homepage | 🎯 Decision Support | 🏟️ Venue Insights |
|------------|--------------------|-------------------|
| (images/Home_Page_ss.png) | (images/Decision_Support_ss.png) | (images/Venue_Insights_ss.png)|

---

## 🧑‍💻 Author

**Rajalakshmi Ravishankar**  
[LinkedIn](https://www.linkedin.com/in/rajalakshmi-ravishankar/) | [GitHub](https://github.com/RajiRavi72)

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---


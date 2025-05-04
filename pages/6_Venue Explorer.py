import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from database import db_conn

st.set_page_config(page_title="Venue Explorer", layout="wide")
st.title("📍 Venue Explorer")

conn = db_conn()

# Load full venue data
query = """
SELECT 
    v.venue_id,
    v.venue_name,
    v.city_name,
    v.country_name,
    v.country_code,
    v.time_zone,
    v.complex_id,
    cx.complex_name
FROM venues v
LEFT JOIN complexes cx ON v.complex_id = cx.complex_id
"""
df = pd.read_sql(query, conn)
conn.close()

selected_country = "All"
selected_city = "All"
selected_timezone = "All"


filtered_df = df.copy()
if selected_country != "All":
    filtered_df = filtered_df[filtered_df["country_name"] == selected_country]

if selected_city != "All":
    filtered_df = filtered_df[filtered_df["city_name"] == selected_city]

if selected_timezone != "All":
    filtered_df = filtered_df[filtered_df["time_zone"] == selected_timezone]

# --- DISPLAY FILTERED VENUE TABLE ---
st.subheader("🏟️ Venue List")
st.dataframe(filtered_df[["venue_name", "city_name", "country_name", "time_zone", "complex_name"]])

# --- Filter by Time Zone ---
st.subheader("🔎 Explore Venues by Time Zone")
selected_tz = st.selectbox("Select a Time Zone to view its Venues", options=["All"] + sorted(df["time_zone"].unique()))

if selected_tz != "All":
    tz_filtered = df[df["time_zone"] == selected_tz]
    st.write(f"Total Venues in **{selected_tz}**: {len(tz_filtered)}")
    st.dataframe(tz_filtered[["venue_name", "city_name", "country_name", "complex_name"]])
else:
    st.info("Select a time zone to view venue details.")

# --- Filter by Complex Name ---
st.subheader("🏗️ Explore Venues by Complex")
selected_complex = st.selectbox("Select a Complex to view its Venues", options=["All"] + sorted(df["complex_name"].dropna().unique()))

if selected_complex != "All":
    cx_filtered = df[df["complex_name"] == selected_complex]
    st.write(f"Total Venues in **{selected_complex}**: {len(cx_filtered)}")
    st.dataframe(cx_filtered[["venue_name", "city_name", "country_name", "time_zone"]])
else:
    st.info("Select a complex to view venue details.")

# --- Filter by Country ---
st.subheader("🌍 Explore Venues by Country")
selected_country = st.selectbox("Select a Country to view its Venues", options=["All"] + sorted(df["country_name"].unique()))

if selected_country != "All":
    country_filtered = df[df["country_name"] == selected_country]
    st.write(f"Total Venues in **{selected_country}**: {len(country_filtered)}")
    st.dataframe(country_filtered[["venue_name", "city_name", "complex_name", "time_zone"]])
else:
    st.info("Select a country to view venue details.")

# --- Explore Venues by City ---
st.subheader("🏙️ Explore Venues by City")

# Create dropdown with all available cities
selected_city = st.selectbox(
    "Select a City to view its Venues", 
    options=["All"] + sorted(df["city_name"].unique())
)

# Filter data based on selected city
if selected_city != "All":
    city_df = df[df["city_name"] == selected_city]
    st.write(f"Total venues in **{selected_city}**: {len(city_df)}")
    st.dataframe(city_df[["venue_name", "country_name", "complex_name", "time_zone"]])
else:
    st.info("Select a city from the dropdown to view its venues.")

# --- CHART 2: Top 10 Cities with Most Venues ---
st.subheader("🏙️ Top 10 Cities with Most Venues")
city_count = df['city_name'].value_counts().nlargest(10).reset_index()
city_count.columns = ['City', 'Venue Count']

fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.barplot(data=city_count, y='City', x='Venue Count', hue ='City', palette='magma', ax=ax2, legend = False)
ax2.set_title("Top 10 Cities with Most Venues")
ax2.set_xlabel("Number of Venues")
ax2.set_ylabel("City")
for container in ax2.containers:
    ax2.bar_label(container, label_type='edge', fontsize=8)

st.pyplot(fig2)

conn = db_conn()
query = """
SELECT v.venue_id, v.venue_name, v.city_name, v.country_name, 
       v.time_zone, cx.complex_name
FROM venues v
LEFT JOIN complexes cx ON v.complex_id = cx.complex_id
"""
df = pd.read_sql(query, conn)
conn.close()

st.subheader("🌍 Top 10 Countries with Most Venues")
country_counts = df['country_name'].value_counts().head(10)
fig1, ax1 = plt.subplots()
sns.barplot(x=country_counts.values, y=country_counts.index, hue= country_counts.index, palette="viridis", ax=ax1, legend = False)
ax1.set_xlabel("Number of Venues")
ax1.set_ylabel("Country")
for container in ax1.containers:
    ax1.bar_label(container, label_type='edge', fontsize=8)

st.pyplot(fig1)

st.subheader("🏟️ Top 10 Complexes with Most Venues")
complex_counts = df['complex_name'].value_counts().head(10)
fig2, ax2 = plt.subplots()
sns.barplot(x=complex_counts.values, y=complex_counts.index, hue =complex_counts.index,  palette="magma", ax=ax2, legend = False)
ax2.set_xlabel("Number of Venues")
ax2.set_ylabel("Complex")
for container in ax2.containers:
    ax2.bar_label(container, label_type='edge', fontsize=8)

st.pyplot(fig2)

st.subheader("🕓 Top 10 Time Zones with Most Venues")
tz_counts = df['time_zone'].value_counts().head(10)
fig3, ax3 = plt.subplots()
sns.barplot(x=tz_counts.values, y=tz_counts.index, hue =tz_counts.index,  palette="crest", ax=ax3, legend = False)
ax3.set_xlabel("Number of Venues")
ax3.set_ylabel("Time Zone")
for container in ax3.containers:
    ax3.bar_label(container, label_type='edge', fontsize=8)

st.pyplot(fig3)




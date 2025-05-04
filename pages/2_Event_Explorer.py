import streamlit as st
from graphviz import Digraph
import pandas as pd
from database import db_conn
import matplotlib.pyplot as plt
import seaborn as sns

# Fetch all competition hierarchy data
def get_competitions():
    conn =  db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT competition_id, competition_name, parent_id FROM competitions;")
    results = cursor.fetchall()
    conn.close()
    return results

# Get top-level competitions that have children
def get_top_level_with_children():
    conn =  db_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT c1.competition_id, c1.competition_name
        FROM competitions c1
        JOIN competitions c2 ON c1.competition_id = c2.parent_id
        WHERE c1.parent_id IS NULL;
    """)
    results = cursor.fetchall()
    conn.close()
    return results

# Get ALL competitions that have children (regardless of level)
def get_all_with_children():
    conn = db_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT c1.competition_id, c1.competition_name
        FROM competitions c1
        JOIN competitions c2 ON c1.competition_id = c2.parent_id;
    """)
    results = cursor.fetchall()
    conn.close()
    return results

# Database connection
def get_data():
    conn =  db_conn()
    query = """
    SELECT c.competition_id, c.competition_name, c.gender, c.type, cat.category_name
    FROM competitions c
    JOIN categories cat ON c.category_id = cat.category_id
    """
    df = pd.read_sql(query, conn)

    type_counts_dict = df['type'].value_counts().to_dict()
    # print(type_counts_dict)

    conn.close()
    return df

df = get_data()

# Generate Graphviz diagram
def generate_graphviz(data, selected_competition_id):
    nodes = {comp_id: name for comp_id, name, _ in data}
    children_map = {}
    for comp_id, name, parent_id in data:
        if parent_id is not None:
            children_map.setdefault(parent_id, []).append(comp_id)

    def add_nodes_edges(dot, current_id):
        for child_id in children_map.get(current_id, []):
            dot.edge(nodes[current_id], nodes[child_id])
            add_nodes_edges(dot, child_id)

    dot = Digraph()
    dot.attr(rankdir='TB')
    if selected_competition_id in nodes:
        dot.node(nodes[selected_competition_id])
        add_nodes_edges(dot, selected_competition_id)
    return dot

# Streamlit UI
st.title("🎾 Event Explorer")
st.subheader(" Understand Competition Hierarchies and the Distribution of Competitions across Categories, Type and Gender ")

st.subheader("Competition Hierarchies")
st.markdown("""
This helps visualize the hierarchy of tennis competitions. 
Use the checkbox below to explore **only top-level competitions** or **all competitions** that act as parents.
""")

# Checkbox to toggle
top_level_only = st.checkbox("Show only top-level competitions with children", value=True)

# Fetch options based on toggle
if top_level_only:
    options = get_top_level_with_children()
else:
    options = get_all_with_children()

# Dropdown menu
if not options:
    st.warning("No competitions with child events found.")
else:
    comp_names = {name: cid for cid, name in options}
    selected_name = st.selectbox("Select a competition to explore:", list(comp_names.keys()))
    selected_id = comp_names[selected_name]

    # Fetch all data and build graph
    data = get_competitions()
    graph = generate_graphviz(data, selected_id)
    st.graphviz_chart(graph.source)

# Distribution Chart : By Category
st.subheader("Distribution of Competitions by Category")
st.markdown("""
This helps visualize the Distribution of Tennis Competitions by Category.  
""")
fig3, ax3 = plt.subplots(figsize=(12, 6))  # Wider figure

df['wrapped_category'] = df['category_name'].apply(lambda x: '\n'.join(x.split(' ')))
category_order = df['wrapped_category'].value_counts().index
sns.countplot(data=df, x='wrapped_category',hue='wrapped_category', order=category_order, palette='pastel', ax=ax3, legend = False)

ax3.set_xlabel("Category")
ax3.set_ylabel("Number of Competitions")
ax3.set_title("Distribution of Competitions by Category")
ax3.tick_params(axis='x', rotation=45)  

# Annotate each bar with its count
for container in ax3.containers:
    ax3.bar_label(container, label_type='edge', fontsize=8)

st.pyplot(fig3)

# Layout in columns
col1, col2 = st.columns(2)

# Chart 1: By Type
with col1:
    st.subheader("Distribution of Competitions by Type")
    fig1, ax1 = plt.subplots()
    sns.countplot(data=df, x='type',hue='type', palette='Set2', ax=ax1, legend=False)
    ax1.set_xlabel("Type")
    ax1.set_ylabel("Number of Competitions")
    for container in ax1.containers:
        ax1.bar_label(container, label_type='edge', fontsize=8)

    st.pyplot(fig1)

# Chart 2: By Gender
with col2:
    st.subheader("Distribution of Competitions by Gender")
    fig2, ax2 = plt.subplots()
    sns.countplot(data=df, x='gender', hue='gender', palette='cool', ax=ax2, legend =False)
    ax2.set_xlabel("Gender")
    ax2.set_ylabel("Number of Competitions")
    for container in ax2.containers:
        ax2.bar_label(container, label_type='edge', fontsize=8)
        
    st.pyplot(fig2)
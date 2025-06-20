import streamlit as st
import sqlite3
import pandas as pd
import os

# --- CONFIGURATION ---
CREATE_SQL = "create.sql"
QUERY_FOLDER = "."

# --- DATABASE SETUP ---
@st.cache_resource
def init_db():
    conn = sqlite3.connect("file:shared_db?mode=memory&cache=shared", uri=True, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    # Load schema
    with open("create.sql", "r", encoding="utf-8") as f:
        cursor.executescript(f.read())

    # Load each insert file
    insert_files = [
        "product_category_translation_insert.sql",
        "products_insert.sql",
        "product_dimensions_insert.sql",
        "sellers_insert.sql",
        "geolocation_insert.sql",
        "customers_insert.sql",
        "orders_insert.sql",
        "order_items_insert.sql",
        "order_payments_insert.sql",
        "order_reviews_insert.sql"
    ]

    for file in insert_files:
        with open(file, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())

    return conn


conn = init_db()
cursor = conn.cursor()

st.title("📊 SQL Coursework Showcase")
st.markdown("Showcasing data modeling and query language skills using SQLite and Streamlit.")

# --- TABLE BROWSER ---
st.header("🔍 Explore Tables")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall() if not row[0].startswith("sqlite_")]
selected_table = st.selectbox("Choose a table to view:", tables)

table_df = pd.read_sql_query(f"SELECT * FROM {selected_table}", conn)
st.dataframe(table_df)

# --- QUERY RUNNER ---
st.header("📜 Run Sample Queries")
query_files = sorted([f for f in os.listdir(QUERY_FOLDER) if f.startswith("query") and f.endswith(".sql")])
selected_query_file = st.selectbox("Select a query to run:", query_files)

if st.button("Run Query"):
    with open(selected_query_file, "r") as f:
        query = f.read()
    st.code(query, language="sql")
    try:
        # Use cursor.execute for non-SELECTs
        if query.strip().lower().startswith("select"):
            df = pd.read_sql_query(query, conn)
            st.success("Query executed successfully!")
            st.dataframe(df)
        else:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            st.success("Query executed successfully (no output).")
    except Exception as e:
        st.error(f"Failed to execute query: {e}")

# --- FOOTER ---
st.markdown("---")
st.markdown("Made with 💻 using Streamlit and SQLite")
github_repo_url = "https://github.com/anandhkirupa/CSE-521-DMQL-Final-Project"
powerBI_dashboard_url = "https://app.powerbi.com/view?r=eyJrIjoiZDAxYzI4YjUtOTk0NC00NzdmLWIwZjctZGJhNjFhOGQ0ZGI1IiwidCI6Ijk2NDY0YThhLWY4ZWQtNDBiMS05OWUyLTVmNmI1MGEyMDI1MCIsImMiOjN9 "
st.markdown(f"[![Check out GitHub page]({github_repo_url})]({github_repo_url})")
st.markdown(f"[![Check out PowerBI Dashboard]({powerBI_dashboard_url})]({powerBI_dashboard_url})")

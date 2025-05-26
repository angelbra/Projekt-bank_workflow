import streamlit as st
import pandas as pd
import sqlite3

st.title("Bankdata rapport")

# Läs CSV direkt (du kan byta till din egen filväg)
customers_csv = "sebank_customers_with_accounts.csv"
transactions_csv = "transactions.csv"

# Visa kunder från CSV
st.header("Kunddata")
try:
    df_customers = pd.read_csv(customers_csv)
    st.dataframe(df_customers.head(10))
except Exception as e:
    st.error(f"Kunde inte läsa kunddata: {e}")

# Visa transaktioner från CSV
st.header("Transaktionsdata")
try:
    df_transactions = pd.read_csv(transactions_csv)
    st.dataframe(df_transactions.head(10))
except Exception as e:
    st.error(f"Kunde inte läsa transaktionsdata: {e}")

# Eller läs från SQLite databas
st.header("Sammanfattning från databasen")
try:
    conn = sqlite3.connect("bank_data.db")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM customers")
    antal_kunder = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM transactions")
    antal_transaktioner = c.fetchone()[0]

    st.write(f"Totalt antal kunder i databasen: {antal_kunder}")
    st.write(f"Totalt antal transaktioner i databasen: {antal_transaktioner}")

    conn.close()
except Exception as e:
    st.error(f"Kunde inte ansluta till databasen: {e}")

# This code is a simplified version of the original bank workflow using Streamlit for visualization.
# The original code was a Prefect workflow for processing bank data, but this version focuses on loading and displaying the data in a web app.
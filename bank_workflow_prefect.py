from prefect import flow, task
import pandas as pd
import sqlite3
from sqlite3 import Error
import os



BASE_DIR = os.path.dirname(__file__)  # Mappen där filen ligger

ACCOUNTS_CSV = os.path.join(BASE_DIR, "accounts.csv")
VALID_TRANSACTIONS_CSV = os.path.join(BASE_DIR, "valid_transactions.csv")
INVALID_TRANSACTIONS_CSV = os.path.join(BASE_DIR, "invalid_transactions.csv")
KUNDER_UTAN_ACCOUNT_CSV = os.path.join(BASE_DIR, "kunder_utan_account.csv")
DATABASE = os.path.join(BASE_DIR, "bank_data.db")




## 1. read_customers och read_transactions läser CSV-filerna till Pandas DataFrames.
@task
def read_customers():
    print("Läser kunddata från CSV...")
    df = pd.read_csv(ACCOUNTS_CSV)
    print(f"Antal kunder: {len(df)}")
    return df

@task
def read_valid_transactions():
    print("Läser giltiga transaktionsdata från CSV...")
    df = pd.read_csv(VALID_TRANSACTIONS_CSV)
    print(f"Antal giltiga transaktioner: {len(df)}")
    return df

@task
def read_invalid_transactions():
    print("Läser ogiltiga transaktionsdata från CSV...")
    df = pd.read_csv(INVALID_TRANSACTIONS_CSV)
    print(f"Antal ogiltiga transaktioner: {len(df)}")
    return df


## 2. create_db skapar en SQLite databasfil 
## och två tabeller: kunder och transaktioner.

@task
def create_database():
    print("Skapar SQLite databas och tabeller...")
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Skapa tabell för kunder
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            Customer TEXT,
            Address TEXT,
            Phone TEXT,
            Personnummer TEXT,
            BankAccount TEXT PRIMARY KEY
        )
        """)

        # Skapa tabell för transaktioner
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS valid_transactions (
            transaction_id TEXT PRIMARY KEY,
            timestamp TEXT,
            amount REAL,
            currency TEXT,
            sender_account TEXT,
            receiver_account TEXT,
            sender_country TEXT,
            sender_municipality TEXT,
            receiver_country TEXT,
            receiver_municipality TEXT,
            transaction_type TEXT,
            notes TEXT
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS invalid_transactions (
            transaction_id TEXT PRIMARY KEY,
            timestamp TEXT,
            amount REAL,
            currency TEXT,
            sender_account TEXT,
            receiver_account TEXT,
            sender_country TEXT,
            sender_municipality TEXT,
            receiver_country TEXT,
            receiver_municipality TEXT,
            transaction_type TEXT,
            notes TEXT
        )
        """)
        ## INVALID TRANSACTIONS TABLE
        conn.commit()
        conn.close()
        print("Databas och tabeller skapade.")
    except Error as e:
        print(f"Fel vid skapande av databas: {e}")
    finally:
        if conn:
            conn.close()

## 3. save_customers_to_db och save_transaction
## lägger in kund och transktionsdata i databasen

@task
def save_customers_to_db(customers_df):
    print("Laddar kunddata till databasen...")
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("BEGIN")  # Starta transaktion
        customers_df.to_sql('customers', conn, if_exists='replace', index=False)
        conn.commit()
        print("Kunddata inlagd.")
    except Error as e:
        if conn:
            conn.rollback()
        print(f"Fel vid insättning av kunddata: {e}")
    finally:
        if conn:
            conn.close()

    
@task
def save_transactions_to_db(valid_df, invalid_df):
    print("Laddar transaktionsdata till databasen...")
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        valid_df.to_sql('valid_transactions', conn, if_exists='replace', index=False)
        invalid_df.to_sql('invalid_transactions', conn, if_exists='replace', index=False)
        conn.commit()
        print("Transaktionsdata inlagd.")
    except Error as e:
        if conn:
            conn.rollback()
        print(f"Fel vid insättning av transaktionsdata: {e}")
    finally:
        if conn:
            conn.close()


## 4. validate_transactions validerar att alla transaktioner har giltiga konto.
##validate_transactions kollar att alla konton i transaktionerna 
##finns i kund-tabellen. Om inte, visas vilka konton som är felaktiga.



@task
def generera_rapport(transactions_df):
    print("🧾 Rapport med Pandas (från fil)...")
    total = len(transactions_df)
    total_amount = transactions_df["amount"].sum()
    top_countries = transactions_df["sender_country"].value_counts().head(3)
    print(f"Totalt antal transaktioner: {total}")
    print(f"Total summa: {total_amount} {transactions_df['currency'].iloc[0]}")
    print("Topp 3 avsändarländer:")
    print(top_countries)

## Rapport med SQL (efter att datan sparats i databasen)
@task
def generate_report():
    print("🧾 Rapport från databasen...")
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM customers")
        customer_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM valid_transactions")

        transaction_count = cursor.fetchone()[0]

        print(f"Totalt antal kunder i databasen: {customer_count}")
        print(f"Totalt antal transaktioner i databasen: {transaction_count}")
    except Error as e:
        print(f"Fel vid rapportgenerering: {e}")
    finally:
        if conn:
            conn.close()
         

## 5. bank_workflow är en prefect flow som kör alla steg i rätt ordning automatiskt.

@flow
def bank_workflow():
    customers_df = read_customers()
    create_database()
    save_customers_to_db(customers_df)

    valid_transactions_df = read_valid_transactions()
    invalid_transactions_df = read_invalid_transactions()
    save_transactions_to_db(valid_transactions_df, invalid_transactions_df)

    generera_rapport(valid_transactions_df)  # 📊 Rapport från giltiga transaktioner
    generate_report()   

if __name__ == "__main__":
    bank_workflow()




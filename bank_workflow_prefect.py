from prefect import flow, task
import pandas as pd
import sqlite3
from sqlite3 import Error

# Sökvägar till dina CSV-filer
TRANSACTIONS_CSV = r"C:\Users\Angelica\OneDrive\Escritorio\code\Datakvalitet\Projekt-bank_workflow\transactions.csv"
CUSTOMERS_CSV = r"C:\Users\Angelica\OneDrive\Escritorio\code\Datakvalitet\Projekt-bank_workflow\sebank_customers_with_accounts.csv"
DATABASE = "bank_data.db"

## 1. read_customers och read_transactions läser CSV-filerna till Pandas DataFrames.
@task
def read_customers():
    print("Läser kunddata från CSV...")
    df = pd.read_csv(CUSTOMERS_CSV)
    print(f"Antal kunder: {len(df)}")
    return df

@task
def read_transactions():
    print("Läser transaktionsdata från CSV...")
    df = pd.read_csv(TRANSACTIONS_CSV)
    print(f"Antal transaktioner: {len(df)}")
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
        CREATE TABLE IF NOT EXISTS transactions (
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

        conn.commit()
        conn.close()
        print("Databas och tabeller skapade.")
    except Error as e:
        print(f"Fel vid skapande av databas: {e}")

## 3. save_customers_to_db och save_transaction
## lägger in kund och transktionsdata i databasen

@task
def save_customers_to_db(customers_df):
    print("Laddar kunddata till databasen...")
    try:
        conn = sqlite3.connect(DATABASE)
        customers_df.to_sql('customers', conn, if_exists='replace', index=False)
        print("Kunddata inlagd.")
    except Error as e:
        print(f"Fel vid insättning av kunddata: {e}")
    finally:
        conn.close()

@task
def save_transactions_to_db(transactions_df):
    print("Laddar transaktionsdata till databasen...")
    try:
        conn = sqlite3.connect(DATABASE)
        transactions_df.to_sql('transactions', conn, if_exists='replace', index=False)
        print("Transaktionsdata inlagd.")
    except Error as e:
        print(f"Fel vid insättning av transaktionsdata: {e}")
    finally:
        conn.close()

## 4. validate_transactions validerar att alla transaktioner har giltiga konto.
##validate_transactions kollar att alla konton i transaktionerna 
##finns i kund-tabellen. Om inte, visas vilka konton som är felaktiga.

@task
def validera_transaktioner(transactions_df, customers_df):
    print("Validerar transaktioner mot kundkonton...")
    # Vi antar att 'sender_account' och 'receiver_account' ska finnas i kundernas BankAccount
    giltiga_konton = set(customers_df['BankAccount'])
    transactions_df['valid'] = transactions_df.apply(
        lambda row: row['sender_account'] in giltiga_konton and row['receiver_account'] in giltiga_konton,
        axis=1
    )
    ogiltiga_transaktioner = transactions_df[transactions_df['valid'] == False]
    print(f"Antal ogiltiga transaktioner: {len(ogiltiga_transaktioner)}")
    # Returnera bara giltiga transaktioner
    return transactions_df[transactions_df['valid'] == True].drop(columns=['valid'])


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
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM customers")
    customer_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM transactions")
    transaction_count = cursor.fetchone()[0]

    print(f"Totalt antal kunder i databasen: {customer_count}")
    print(f"Totalt antal transaktioner i databasen: {transaction_count}")
    conn.close()


## 5. bank_workflow är en prefect flow som kör alla steg i rätt ordning automatiskt.

@flow
def bank_workflow():
    customers_df = read_customers()
    transactions_df = read_transactions()
    create_database()
    save_customers_to_db(customers_df)
    save_transactions_to_db(transactions_df)
    valid_transactions = validera_transaktioner(transactions_df, customers_df)
    generera_rapport(transactions_df)  # 📊 Rapport från CSV-filen
    generate_report()   

if __name__ == "__main__":
    bank_workflow()



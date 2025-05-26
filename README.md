# Automatiserat arbetsflöde för banktransaktioner

Detta projekt automatiserar validering, behandling och lagring av banktransaktioner med hjälp av **Prefect** – ett workflow management-verktyg i Python.
Det inkluderar datavalidering, databaslagring, transaktionsbearbetning och rapportgenerering.


---

## Workflow Automation & Orchestration

- **Roll:** DevOps / Workflow Engineer  
- **Verktyg:**
- Prefect
- Python
- Pandas
- SQLite

- **Huvudfil:** `Bank Workflow Prefect.py`


---

## Funktioner

1. Läser kund- och transaktionsdata från CSV
2. Skapar SQLite-databas med två tabeller
3. Sparar data i databasen
4. Validerar transaktioner (kontrollerar giltiga konton)
5. Genererar rapport med Pandas (från CSV)
6. Genererar rapport med SQL (från databasen)

---

## Leverabler

| Filtyp         | Filnamn                    | Beskrivning                          |
|----------------|----------------------------|--------------------------------------|
| Python-script  | `Bank_workflow_prefect.py` | Huvudfil för arbetsflödet            |
| Textfil        | `reporte.txt`              | Genererad rapport                    |
| Dokumentation  | `README.md`                | Projektbeskrivning och instruktioner |
| execution logs |   Loggfil.txt              | körlogg - logg från arbetsflödet     |
|  Python-paket  |  requirements.txt          |  snabbt installera alla beroenden    |
| notebook       |  db innehål.ipynb          | sammanfattning db innehåll           |

---

# Projekt-bank_workflow

Detta projekt implementerar ett automatiserat arbetsflöde med **Prefect** för att bearbeta bankdata.

## Funktionalitet

- Läser kund- och transaktionsdata från CSV-filer
- Skapar och laddar data till en SQLite-databas
- Validerar transaktioner mot kundtabellen
- Genererar rapporter både från CSV-filer och från databasen
- Felhantering med rollback vid databasoperationer

## Krav

- Python 3.8 eller senare
- Prefect
- Pandas
- SQLite

## Användning
källor: 
transactions.csv — innehåller alla transaktioner (pengar som skickas eller tas emot).
sebank_customers_with_accounts.csv — innehåller kunddata och kontoinformation.

github källor: 
https://github.com/WeeHorse/python-bank-project-start/blob/main/data/transactions.csv
https://github.com/WeeHorse/python-bank-project-start/blob/main/data/sebank_customers_with_accounts.csv


virtuella miljö:

 -  .\venv\Scripts\activate    # Windows PowerShell
 -   
 -   körlogg (execution logs) : python bank_workflow_prefect.p

## Installera beroenden
För att installera de nödvändiga paketen, kör följande kommando i terminalen:

pip install -r requirements.txt


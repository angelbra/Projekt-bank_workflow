# Automatiserat arbetsflöde för banktransaktioner

Detta projekt automatiserar validering, behandling och lagring av banktransaktioner med hjälp av **Prefect** – ett workflow management-verktyg i Python.

---

## Workflow Automation & Orchestration

- **Roll:** DevOps / Workflow Engineer  
- **Verktyg:** Prefect  
- **Huvudfil:** `Bank Workflow Prefect.py`

---

## Funktioner

- Läser transaktionsdata från en CSV-fil  
- Validerar datan (tar bort felaktiga rader)  
- Identifierar misstänkta transaktioner  
- Sparar datan i en PostgreSQL-databas  
- Skapar en rapport med statistik över transaktionerna

---

## Leverabler

| Filtyp         | Filnamn                    | Beskrivning                          |
|----------------|----------------------------|--------------------------------------|
| Python-script  | `Bank_Workflow_Prefect.py` | Huvudfil för arbetsflödet            |
| Textfil        | `reporte.txt`              | Genererad rapport                    |
| Dokumentation  | `README.md`                | Projektbeskrivning och instruktioner |
| execution logs |   Loggfil.txt              |    körlogg (execution logs)          |

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


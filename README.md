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

| Filtyp         | Filnamn                    | Beskrivning                            |
|----------------|----------------------------|--------------------------------------|
| Python-script  | `Bank Workflow Prefect.py` | Huvudfil för arbetsflödet             |
| Textfil        | `reporte.txt`              | Genererad rapport                      |
| Dokumentation  | `README.md`                | Projektbeskrivning och instruktioner  |
| Logg-exempel   | (exempel-loggfil)          | Exempel på logg från arbetsflödet     |

---

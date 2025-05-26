# Använd en basbild med Python
FROM python:3.11-slim

# Skapa en mapp i "sandboxen" som heter /app
WORKDIR /app

# Kopiera dependencies (bibliotek du ska använda)
COPY requirements.txt .

# Installera biblioteken
RUN pip install --no-cache-dir -r requirements.txt

# Kopiera resten av projektet
COPY . .

# Kommando för att köra ditt Prefect-flöde
CMD ["python", "bank_workflow_prefect.py"]

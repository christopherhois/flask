import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def connect_db():
    try:
        client = MongoClient(os.environ['MONGO_URI'], serverSelectionTimeoutMS=5000)
        # Teste die Verbindung
        client.admin.command('ping')
        print('MongoDB verbunden')
        return client
    except Exception as e:
        print(f'Fehler: {e}')
        exit(1)

# Beispiel für den Export der Funktion
if __name__ == '__main__':
    connect_db()
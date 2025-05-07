from django.conf import settings
from pymongo import MongoClient


def get_mongo_client():
    try:
        client = MongoClient(settings.MONGO_URI)
        print("✅ Conectado ao MongoDB")
        return client
    except Exception as e:
        print(f"❌ Erro ao conectar ao MongoDB: {e}")
        return None


mongo_client = get_mongo_client()
db = mongo_client.analytics_db if mongo_client else None

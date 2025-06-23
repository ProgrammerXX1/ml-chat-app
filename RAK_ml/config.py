import os

# Адрес Weaviate берётся из переменной среды или по умолчанию
WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")

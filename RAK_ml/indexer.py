from sentence_transformers import SentenceTransformer
import weaviate
import uuid
from typing import List
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from .config import WEAVIATE_URL

# Инициализация клиента Weaviate и модели эмбеддингов
client = weaviate.Client(WEAVIATE_URL)
# client = weaviate.Client("http://localhost:8080")
embedding_model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2")

def embed_and_store(chunks: List[str], namespace: str = "DocumentChunk"):
    existing_classes = [cls["class"] for cls in client.schema.get()["classes"]]
    if namespace not in existing_classes:
        client.schema.create_class({
            "class": namespace,
            "vectorizer": "none",
            "properties": [{"name": "text", "dataType": ["text"]}]
        })

    for chunk in chunks:
        clean_chunk = chunk.encode("utf-8", errors="ignore").decode("utf-8")
        vector = embedding_model.encode(clean_chunk).tolist()
        client.data_object.create(
            data_object={"text": clean_chunk},
            class_name=namespace,
            uuid=str(uuid.uuid4()),
            vector=vector
        )

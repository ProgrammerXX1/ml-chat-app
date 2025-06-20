import weaviate
from sentence_transformers import SentenceTransformer
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Инициализация клиента Weaviate и модели эмбеддингов
client = weaviate.Client("http://localhost:8080")
embedding_model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2")

def retrieve_relevant_chunks(query: str, namespace: str = "DocumentChunk", top_k: int = 3):
    # Генерация эмбеддинга для запроса
    vector = embedding_model.encode(query).tolist()

    # Поиск похожих чанков в Weaviate
    result = client.query.get(namespace, ["text"])\
        .with_near_vector({"vector": vector})\
        .with_limit(top_k).do()

    # Возврат текста найденных чанков
    return [item["text"] for item in result["data"]["Get"].get(namespace, [])]

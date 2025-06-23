from RAK_ml.file_reader import read_file
from RAK_ml.chunking import chunk_text
from RAK_ml.indexer import embed_and_store
from RAK_ml.retriever import retrieve_relevant_chunks
from RAK_ml.qa_chain import generate_answer
from RAK_ml.llm import AVAILABLE_MODELS

def process_document(filepath: str, namespace: str = "DocumentChunk") -> int:
    """
    Чтение документа, чанкинг и индексация в Weaviate.
    Возвращает количество чанков.
    """
    text = read_file(filepath)
    chunks = chunk_text(text)
    embed_and_store(chunks, namespace)
    return len(chunks)

def get_available_models() -> list:
    """
    Список доступных моделей из AVAILABLE_MODELS.
    """
    return list(AVAILABLE_MODELS.keys())

def answer_query(question: str, model_name: str, namespace: str = "DocumentChunk") -> str:
    """
    Генерация ответа на основе вопроса, выбранной модели и пространства.
    """
    chunks = retrieve_relevant_chunks(question, namespace=namespace)
    return generate_answer(question, chunks, model_name)

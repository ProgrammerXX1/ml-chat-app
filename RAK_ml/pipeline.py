from rak_ml.file_reader import read_file
from rak_ml.chunking import chunk_text
from rak_ml.indexer import embed_and_store
from rak_ml.retriever import retrieve_relevant_chunks
from rak_ml.qa_chain import generate_answer
from rak_ml.llm import AVAILABLE_MODELS

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

def answer_query(question: str, model_name: str = "llama3:latest", filepath: str = None) -> str:
    if filepath:
        print(f"📄 Загружаю файл: {filepath}")
        text = read_file(filepath)
        chunks = chunk_text(text)
        print(f"📥 Индексация в Weaviate...")
        embed_and_store(chunks)

    relevant_chunks = retrieve_relevant_chunks(question)
    print(f"📚 Найдено релевантных чанков: {len(relevant_chunks)}")
    answer = generate_answer(question, relevant_chunks, model_name)
    return answer
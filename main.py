
import argparse
from file_reader import read_file
from chunking import chunk_text
from indexer import embed_and_store
from retriever import retrieve_relevant_chunks
from qa_chain import generate_answer

def main():
    parser = argparse.ArgumentParser(description="RAG-интерфейс для документов")
    parser.add_argument("--file", type=str, required=True, help="Путь к файлу (.txt, .pdf, .docx)")
    parser.add_argument("--question", type=str, required=True, help="Вопрос к содержимому файла")
    parser.add_argument("--provider", type=str, default="openai", help="LLM-провайдер: openai | groq | ollama")
    args = parser.parse_args()

    print("📥 Чтение файла...")
    text = read_file(args.file)

    print("✂️ Чанкинг текста...")
    chunks = chunk_text(text)

    print("📡 Индексация в Weaviate...")
    embed_and_store(chunks)

    print("🔍 Извлечение релевантных чанков...")
    relevant_chunks = retrieve_relevant_chunks(args.question)

    print(f"🧠 Генерация ответа от {args.provider.upper()}...")
    answer = generate_answer(args.question, relevant_chunks, provider=args.provider)

    print("\n✅ Ответ:")
    print(answer)

if __name__ == "__main__":
    main()

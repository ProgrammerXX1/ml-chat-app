import subprocess
from RAK_ml.file_reader import read_file
from RAK_ml.chunking import chunk_text
from RAK_ml.indexer import embed_and_store
from RAK_ml.retriever import retrieve_relevant_chunks
from RAK_ml.qa_chain import generate_answer

def list_ollama_models():
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    lines = result.stdout.strip().splitlines()[1:]  # Пропускаем заголовок
    models = [line.split()[0] for line in lines]
    return models

def select_model(models):
    print("\n📦 Доступные модели (ollama list):")
    for i, name in enumerate(models, start=1):
        print(f"{i}. {name}")
    print()
    while True:
        try:
            choice = int(input("Выбери номер модели → "))
            if 1 <= choice <= len(models):
                return models[choice - 1]
        except ValueError:
            pass
        print("❌ Неверный выбор. Попробуй ещё.")

def main():
    filepath = "example.txt"  # ← Заменить путь вручную при необходимости
    print(f"📄 Загружаю файл: {filepath}")
    text = read_file(filepath)

    print("✂️ Разбивка на чанки...")
    chunks = chunk_text(text)
    print(f"🔢 Всего чанков: {len(chunks)}")

    print("📥 Индексация в Weaviate...")
    embed_and_store(chunks)

    models = list_ollama_models()
    model = select_model(models)
    print(f"✅ Выбрана модель: {model}\n")

    while True:
        question = input("🧠 Вопрос (или 'exit' для выхода): ").strip()
        if question.lower() in {"exit", "выход"}:
            break
        if question.lower() == "/model":
            model = select_model(models)
            print(f"✅ Модель сменена на: {model}")
            continue
        relevant_chunks = retrieve_relevant_chunks(question)
        print(f"📚 Найдено релевантных чанков: {len(relevant_chunks)}")
        answer = generate_answer(question, relevant_chunks, model)
        print(f"\n🤖 Ответ:\n{answer}\n")

if __name__ == "__main__":
    main()

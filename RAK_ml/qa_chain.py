import json
import re
from deep_translator import GoogleTranslator
from langdetect import detect
from .llm import get_llm

# 🔧 Безопасное извлечение JSON из произвольного текста
def extract_json(text: str) -> dict:
    try:
        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            raise ValueError("Не найден JSON-блок")
        return json.loads(match.group(0))
    except Exception as e:
        print("⚠️ Ошибка разбора ответа от LLM:\n")
        print(text)
        print(f"\n✉️ Исключение: {e}")
        return {
            "answer": "⚠️ Ошибка разбора ответа. Пожалуйста, переформулируйте запрос или уточните контекст.",
            "analysis": "",
            "sources": []
        }

# 📘 Перевод на русский
def translate_to_russian(text: str) -> str:
    return GoogleTranslator(source='auto', target='ru').translate(text)

# 🌐 Определение английского языка
def is_english(text: str) -> bool:
    try:
        return detect(text) == "en"
    except:
        return False

# 🧠 Основная функция генерации ответа
def generate_answer(question: str, chunks: list, provider: str = "openai") -> str:
    llm = get_llm(provider)
    context = "\n\n".join(chunks)

    prompt = f"""
Ты — эксперт-аналитик нормативных документов Республики Казахстан и внутренних нормативных документов АО «НК «ҚТЖ», обладающий способностью системно анализировать правовые и регламентные акты, выявлять взаимосвязи между пунктами и главами, и объяснять сложные положения понятным языком.

## Цель
Дай полный, точный и понятный ответ, строго опираясь на нормативные документы.
Ты должен анализировать не как поисковик, а как квалифицированный консультант, способный:
- находить все возможные причины или нормы, влияющие на вопрос;
- сохранять оригинальную структуру и нумерацию документов;
- объяснять так, чтобы пользователь понял, что и как ему делать.

## Алгоритм работы
1. Внимательно и глубоко проанализируй context в связи с question.
2. Выдели точные цитаты (sources), не сокращай их и не редактируй.
3. Объясни, почему был сделан такой вывод (analysis).
4. Сформулируй полезный ответ (answer).
5. Если вопрос вне тематики — верни:
   {{"analysis":"","sources":[],"answer":"Извините, я могу помогать только по вопросам нормативных документов."}}
6. Если релевантных данных нет — верни:
   {{"analysis":"","sources":[],"answer":"Пожалуйста, попробуйте обратиться позже."}}

## Ответ должен быть строго в следующем JSON-формате:
{{
  "answer": "...",     
  "analysis": "...",    
  "sources": [{{"filename": "...", "page": ..., "citation": "..."}}]
}}

Контекст:
{context}

Вопрос: {question}
Ответ:
"""

    raw = llm.chat(prompt)
    parsed = extract_json(raw)

    answer = parsed.get("answer", "").strip()
    analysis = parsed.get("analysis", "").strip()
    sources = parsed.get("sources", [])

    sources_str = ", ".join(
        f'{src.get("filename", "??")} стр. {src.get("page", "?")}'
        for src in sources
    ) or "неизвестен"

    output = f"""✅ Ответ: {answer}

🧠 Анализ: {analysis}

📄 Источники: {sources_str}
"""

    return translate_to_russian(output) if is_english(output) else output

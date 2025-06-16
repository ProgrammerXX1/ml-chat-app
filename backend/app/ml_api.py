import requests

_uploaded_text: str = ""  # глобальное хранилище

def store_uploaded_text(text: str):
    global _uploaded_text
    _uploaded_text = text.strip()

def get_ml_response(user_input: str) -> str:
    if not _uploaded_text:
        return "Сначала загрузите файл."

    prompt = f"""Вот контекст из документа:
{_uploaded_text}

Вопрос: {user_input}
Ответ:"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",  # или llama2
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        return response.json().get("response", "Нет ответа").strip()
    except Exception as e:
        return f"Ошибка ML API: {e}"

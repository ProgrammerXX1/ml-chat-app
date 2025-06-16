# backend/app/ml_api.py

import requests

# Version 3
def get_ml_response(user_input: str) -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",  # или llama2
                "prompt": user_input,
                "stream": False
            },
            timeout=20
        )

        print("Ollama ответ:", response.json())  # 👈 лог в консоль
        return response.json().get("response", "Нет ответа").strip()

    except Exception as e:
        return f"Ошибка при обращении к Ollama: {e}"



# Version 2
# def get_ml_response(user_input: str) -> str:
#     try:
#         response = requests.post(
#             "http://127.0.0.1:8001/predict",
#             json={"message": user_input},
#             timeout=5
#         )
#         return response.json().get("answer", "Нет ответа от ML API")
#     except Exception as e:
#         return f"Ошибка при запросе к ML API: {e}"

# Version 1
# Тут пример для результата без запроса к ML 
# from fastapi import FastAPI
# def get_ml_response(user_input: str) -> str:
#     # Здесь будет вызов к LLM
#     return f"Echo: {user_input}"


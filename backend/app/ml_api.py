# backend/app/ml_api.py

import requests

def get_ml_response(user_input: str) -> str:
    try:
        response = requests.post(
            "http://127.0.0.1:8001/predict",
            json={"message": user_input},
            timeout=5
        )
        return response.json().get("answer", "Нет ответа от ML API")
    except Exception as e:
        return f"Ошибка при запросе к ML API: {e}"


# from fastapi import FastAPI
# def get_ml_response(user_input: str) -> str:
#     # Здесь будет вызов к LLM
#     return f"Echo: {user_input}"


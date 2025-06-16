# backend/app/ml_api.py
def get_ml_response(user_input: str) -> str:
    # Здесь будет вызов к LLM
    return f"Echo: {user_input}"

# backend/app/ml_api.py
# from fastapi import FastApi
# from pydantic import BaseModel
# import requests
# app = FastAPI()
# class ChatInput(BaseModel):
#     message: str
# def get_ml_response(user_input: str) -> str:
#     # Здесь будет вызов к LLM
#     response = requests.post(
#         "http://localhost:8001/predict",
#         json={"message": input.message}
#     )
#     return {"ml_response": response.json()}

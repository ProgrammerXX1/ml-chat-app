from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Request(BaseModel):
    message: str

@app.post("/predict")
def predict(request: Request):
    return {"answer": f"ML получил: {request.message}"}

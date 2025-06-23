import subprocess
import json
import requests

import os
from dotenv import load_dotenv

# Загружаем .env, если он есть
load_dotenv()

# Получаем URL из переменной среды или используем локальный по умолчанию
OLLAMA_SERVER_URL = os.getenv("OLLAMA_SERVER_URL", "http://localhost:11434")

class OllamaProvider:
    def __init__(self, model: str = "llama3", server_url=OLLAMA_SERVER_URL):
        self.model = model
        self.server_url = server_url

    def chat(self, prompt: str) -> str:
        try:
            response = requests.post(
                f"{self.server_url}/api/generate",
                json={"model": self.model, "prompt": prompt},
                timeout=60,
                stream=True  # 🧠 важный параметр!
            )
            response.raise_for_status()

            full_text = ""
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    try:
                        chunk = json.loads(line)
                        full_text += chunk.get("response", "")
                    except json.JSONDecodeError:
                        continue  # игнорируем мусор

            return full_text or "⚠️ Пустой ответ от модели"

        except Exception as e:
            return f"⚠️ Ошибка при запросе к серверу модели: {e}"



# 🧩 Допустимые модели, которые ты загрузил
AVAILABLE_MODELS = {
    "llama3 18gb": "llama3:latest",
    "mistral 4.1gb": "mistral:latest",
    "qwen7b 4.5gb": "qwen:7b",
    "qwen14b 8.2gb": "qwen:14b",
    "gemma2b 1.7gb": "gemma:2b",
    "deepseek6.7b 3.8gb": "deepseek-coder:6.7b",
    "deepseek33b 18 gb": "deepseek-coder:33b",
    "deepseekLite 3.8gb": "deepseek-coder:latest",
    "phi 1.6gb":"phi:latest",
    "gamma:2b 1.7gb":"gamma:2b"
}

# 🔧 Другие провайдеры (заглушки)
class OpenAIProvider:
    def chat(self, prompt: str) -> str:
        return "🔧 OpenAIProvider не реализован. Используйте Ollama."

class GroqProvider:
    def chat(self, prompt: str) -> str:
        return "🔧 GroqProvider не реализован. Используйте Ollama."

# 🔌 Унифицированный доступ
def get_llm(provider_name: str):
    # Если это ключ из AVAILABLE_MODELS → получаем реальное имя
    model = AVAILABLE_MODELS.get(provider_name, provider_name)

    if model in ollama_installed_models():
        return OllamaProvider(model)

    raise ValueError(f"Неизвестный провайдер или модель: {provider_name}")
def ollama_installed_models():
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().splitlines()
        if len(lines) <= 1:
            return []
        return [line.split()[0] for line in lines[1:]]
    except Exception as e:
        print(f"⚠️ Ошибка при вызове `ollama list`: {e}")
        return []
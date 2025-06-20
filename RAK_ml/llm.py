import subprocess
import json

# ✅ Класс OllamaProvider с возможностью выбора модели
class OllamaProvider:
    def __init__(self, model: str = "llama3:latest"):
        self.model = model

    def chat(self, prompt: str) -> str:
        try:
            result = subprocess.run(
                ["ollama", "run", self.model],
                input=prompt.encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=180
            )
            if result.returncode != 0:
                return f"⚠️ Ошибка выполнения ollama run: {result.stderr.decode('utf-8')}"
            return result.stdout.decode("utf-8").strip()
        except subprocess.TimeoutExpired:
            return "⚠️ Время ожидания ответа от Ollama истекло."

# 🧩 Допустимые модели, которые ты загрузил
AVAILABLE_MODELS = {
    "llama3": "llama3:latest",
    "mistral": "mistral:latest",
    "qwen7b": "qwen:7b",
    "qwen14b": "qwen:14b",
    "gemma2b": "gemma:2b",
    "deepseek6.7b": "deepseek-coder:6.7b",
    "deepseek33b": "deepseek-coder:33b",
    "deepseekLite": "deepseek-coder:latest"
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
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    return [line.split()[0] for line in result.stdout.strip().splitlines()[1:]]

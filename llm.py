import os
import requests

class GroqProvider:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = "llama3-8b-8192"
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"

    def chat(self, prompt):
        response = requests.post(
            self.api_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2
            }
        )
        return response.json()["choices"][0]["message"]["content"]

class OpenAIProvider:
    def __init__(self):
        import openai
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def chat(self, prompt):
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content

class OllamaProvider:
    def __init__(self):
        self.api_url = "http://localhost:11434/api/generate"

    def chat(self, prompt):
        response = requests.post(
            self.api_url,
            json={"model": "llama3", "prompt": prompt, "stream": False}
        )
        return response.json()["response"]

def get_llm(provider: str):
    if provider == "groq":
        return GroqProvider()
    elif provider == "openai":
        return OpenAIProvider()
    elif provider == "ollama":
        return OllamaProvider()
    else:
        raise ValueError(f"Unknown provider: {provider}")

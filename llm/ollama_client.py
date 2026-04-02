import requests
import json
import os
import re
from dotenv import load_dotenv


load_dotenv()

class OllamaClient:

    def __init__(self, model="mistral"):
        self.model = os.getenv("OLLAMA_MODEL", "mistral")
        base_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.url = f"{base_url}/api/generate"

    def generate_json(self, prompt):

        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )

        text = response.json()["response"]

        match = re.search(r"\{[\s\S]*\}", text)

        if not match:
            raise Exception(f"Model did not return JSON:\n{text}")

        json_text = match.group()

        try:
            return json.loads(json_text)
        except Exception:
            print("INVALID JSON FROM MODEL:")
            print(json_text)
            raise
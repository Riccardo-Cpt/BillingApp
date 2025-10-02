import ollama
import requests

class ollama_utils:
    def __init__(self, url, model):
        self.url = url
        self.model = model

    def query_ollama(self, prompt):

        headers = {"Content-Type": "application/json"}
            
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0},
        }

        response = requests.post(self.url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["response"]
import ollama
import requests

class ollama_utils:
    def query_ollama(prompt, url, model="llama3.2:1b"):

        headers = {"Content-Type": "application/json"}
            
        data = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0},
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["response"]
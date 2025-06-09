import requests
import json

def generate_prompt(prompt, model_name="deepseek-r1:7b"):
    url = "http://localhost:11434/api/generate"
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = response.json()
        actual_response = response_json["response"]
        print(actual_response)
        return actual_response
    else:
        print("Error:", response.status_code, response.text)
        return None

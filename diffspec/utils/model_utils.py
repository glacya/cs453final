import ollama

def prompt_model(prompt, model="qwen3:8b"):
    response = ollama.generate(
        model=model,
        prompt=prompt
    )
    return response.get('response', '').strip()

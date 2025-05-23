import ollama
import time
import httpx

class ModelTimeoutError(Exception):
    pass

def prompt_model(
    prompt: str,
    model: str = "qwen3:8b",
    max_tokens: int = 2000,
    timeout: float = 240.0,
    max_retries: int = 3,
    temperature: float = 0.25,
):
    client = ollama.Client(timeout=httpx.Timeout(timeout, connect=5.0, read=timeout))
    for attempt in range(1, max_retries + 1):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"[{now}] Attempt {attempt} start")
        try:
            resp = client.generate(
                model=model,
                prompt=prompt,
                options={"temperature": temperature, "max_tokens": max_tokens},
            )
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Success")
            return resp["response"].strip()
        except httpx.TimeoutException as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Timeout (attempt {attempt}): {e}")
            if attempt == max_retries:
                raise ModelTimeoutError(f"Timed out after {max_retries} attempts")
            print(f"[!] Retrying ({attempt}/{max_retries})")
        except Exception:
            raise
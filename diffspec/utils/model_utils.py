import ollama
import time
import concurrent.futures
import httpx

class ModelTimeoutError(Exception):
    """Raised when the model call times out after all retries."""
    pass

def prompt_model(
    prompt: str,
    model: str = "qwen3:8b",
    max_tokens: int = 2000,
    timeout: float = 240.0,        # per‐call timeout in seconds
    max_retries: int = 3,
    temperature: float = 0.25,
):
    """
    Try up to `max_retries` times to generate within `timeout` seconds.
    If all attempts time out, raise ModelTimeoutError.
    """
    for attempt in range(1, max_retries + 1):
        start = time.monotonic()
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"[{now}] Attempt {attempt} start")

        # run generate() in a separate thread so we can bound its runtime
        def run_generate():
            # you can also pass a HTTPX timeout on the client if you like:
            # client = ollama.Client(timeout=timeout)
            # return client.generate(...)
            return ollama.generate(
                model=model,
                prompt=prompt,
                options={
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                }
            )

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(run_generate)

            try:
                resp = future.result(timeout=timeout)
            except concurrent.futures.TimeoutError:
                elapsed = time.monotonic() - start
                now_end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(f"[{now_end}] Attempt {attempt} timed out after {elapsed:.2f}s")
                if attempt < max_retries:
                    print(f"[!] Timeout – retrying ({attempt}/{max_retries})")
                    continue
                else:
                    raise ModelTimeoutError(
                        f"Failed after {max_retries} attempts due to timeouts."
                    )
            except httpx.TimeoutException as e:
                # if you configured a client with HTTPX-level timeouts
                elapsed = time.monotonic() - start
                now_end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(f"[{now_end}] HTTPX timeout on attempt {attempt} after {elapsed:.2f}s: {e}")
                if attempt < max_retries:
                    print(f"[!] HTTPX timeout – retrying ({attempt}/{max_retries})")
                    continue
                else:
                    raise ModelTimeoutError(
                        f"Failed after {max_retries} attempts due to HTTPX timeouts: {e}"
                    )
            except Exception as e:
                # some other error – re‐raise immediately
                elapsed = time.monotonic() - start
                now_end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(f"[{now_end}] Attempt {attempt} failed after {elapsed:.2f}s: {e!s}")
                raise

        # if we get here, we have a valid response
        end = time.monotonic()
        now_end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"[{now_end}] Attempt {attempt} success, elapsed: {end - start:.2f}s")
        return resp.get("response", "").strip()

    # Should never reach here
    raise ModelTimeoutError("Unreachable: retries exhausted without raising")
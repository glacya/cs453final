import re

def clean_diff_output(text: str) -> str:
    """Remove <think>...</think> blocks and strip surrounding whitespace."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

# load file given path
def load_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read()
    return data


# save output to file
def save_file(content, path):
    with open(path, 'w', encoding='utf-8')  as output:
        output.write(content)

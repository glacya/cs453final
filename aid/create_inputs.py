#!/usr/bin/env python3
"""
Auto-generate and execute Cyaron-based input generators for specified problems.
Supports optional filtering by a PID list file and separate parsing/execution mode.
TODO : revise this
"""
import sys
import subprocess
import re
from pathlib import Path
import ollama
import argparse
from typing import Set, Optional
import traceback
import shutil


# Base directory holding all projects
BASE_DIR = Path("datasets/TrickyBugs")

# Subfolders within each project
INPUT_GENS_DIR = Path("input_generator")
CHAT_INPUTS_DIR = Path("chat_generated_inputs")

# Log files
FAILED_PIDS_FILE = Path("failed_pids.txt")
FAILED_LOGS_FILE = Path("failed_logs.txt")

# Collect failures
failed_pids = []
failed_logs = []


def generate_prompt_template(pro_des: str) -> str:
    return f""" 
SYSTEM: ALWAYS wrap your entire Python script in a single ```python ``` block and emit no other text.

INSTRUCTION:

The following is a description of a coding problem, please write an input generator for this problem matching the following patterns.
DO NOT SOLVE THE PROBLEM BUT CREATE AN INPUT-GENERATOR TO TEST THE SOLUTIONS OF PROBLEM.
It must produce 100 independent test files saved as '../chat_generated_inputs/chatGenInput_i.in' (i = 0..99)
The inputs should meet the given constraints of the problem description.
Ensure you create directories with os.makedirs, and only wrap the final code in a ```python ``` fence.

Your generator should import and use only this **sufficient toolkit** for random‐test patternes in the below code.
ONLY IMPORT THE PACKAGED LISTED BELOW. DO NOT USE ANYTHING ELSE. 

sufficient toolkit
```python
import os
import random
import string
import math
from cyaron import IO, Vector, String, Graph
```

Then, for each test file, choose random lengths within problem-specific bounds (if fixed, use fixed length) and generate accordingly.
Your generator must choose every random length from the actual problem constraints.  
For example, if the problem says “1 ≤ |A| ≤ 2×10⁵”, use:

    min_len, max_len = 1, 2 * 10**5
    L = random.randint(min_len, max_len)

Do **not** copy the example values (like 1 or 2 * 10**5) directly.  
Instead, extract the upper and lower bounds from the **PROBLEM DESCRIPTION** section and bind them to variables (`min_len`, `max_len`, etc.) before calling `random.randint`.
Strictly follow the code style and its exaplnation when generating the input-generator script.  

```python

# Basic integer and pair lists:
min_num, max_num = 3, 100
N = random.randint(min_num, max_num)
pairs = Vector.random(num=N, position_range=[(1,6),(1,6)], mode=1)

# Random string with variable length from constraints
min_len, max_len = 1, 2 * 10**5
L = random.randint(min_len, max_len)
s = String.random(L, charset=string.ascii_lowercase)  
io.input_writeln(s)  

# Random list of integers within constraints: 
min_len, max_len = 1, 2 * 10**5
N = random.randint(min_len, max_len)
arr = Vector.random(num=N, position_range=[(1, 10**9)], mode=0)  
io.input_writeln(*arr)  

# strictly increasing sequence  
min_len, max_len = 1, 2 * 10**5
def generate_increasing_sequence(n, low=1, high=10**9):
    return sorted(random.sample(range(low, high), n))
seq = generate_increasing_sequence(N)
io.input_writeln(*seq)

# Random tree as edge list:
min_n, max_n = 2, 200000
weight_min, weight_max = 1, 1000
n = random.randint(min_n, max_n)
tree = Graph.tree(n, weight_limit=(weight_min, weight_max))
io.input_writeln(n)
for u, v, w in tree.edges:
    io.input_writeln(u, v, w)

# Random graph:
min_n, max_n = 2, 2 * 10**5
min_m, max_m = 0, 5000
n = random.randint(min_n, max_n)
ceiling_m = min(n*(n-1)//2, max_m)
m = random.randint(min_m, ceiling_m)
g = Graph.graph(n, m, self_loop=False, repeated_edges=False)
io.input_writeln(n, m)
for u, v, _ in g.edges:
    io.input_writeln(u, v)

# Connected Undirected, Weighted Graph:
min_n, max_n = 2, 10000
weight_min, weight_max = 1, 1000
n = random.randint(min_n, max_n)
max_m = 5000
max_edges = min(n*(n-1)//2, max_m)
m = random.randint(n-1, max_edges)
udag = Graph.UDAG(n, m, weight_limit=(weight_min, weight_max))
io.input_writeln(n, m)
for u, v, w in udag.edges:
    io.input_writeln(u, v, w)

# Directed Acyclic Graph (DAG):
min_n, max_n = 1, 5000
n = random.randint(min_n, max_n)
max_m = n*(n-1)//2
m = random.randint(0, max_m)
dag = Graph.DAG(n, m)
io.input_writeln(n, m)
for u, v in dag.edges:
    io.input_writeln(u, v)

    
```

Especially when Write each file with IO, DO NOT USE OTHER FUNCTIONS UNDER IO. ONLY USE io.input_writeln and io.input_write.
YOU MUST FOLLOW THE STYLE BELOW. 
Produce 100 independent test files SAVED AS **'../chat_generated_inputs/chatGenInput_i.in'** (i = 0..99)

```python
# Write each file with IO:
for i in range(100):
    os.makedirs(f'../chat_generated_inputs/', exist_ok=True)
    path = f"../chat_generated_inputs/chatGenInput_{{i}}"
    io = IO(file_prefix=path, disable_output=True)

    # write N on its own line
    io.input_writeln(N)

    # write each pair on its own line
    for x, y in pairs:
        io.input_writeln(x, y)

    # OR build a single line of space-separated values manually:
    io.input_write(*[random.randint(1,100) for _ in range(5)])
    io.input_writeln()  # finish the line
```

PROBLEM DESCRIPTION:
{pro_des}
"""


def generate_code(pid: str, description: str, model: str):
    prompt = generate_prompt_template(description)
    print(f"[{pid}] Generating input_gen.py...")
    resp = ollama.generate(model=model, prompt=prompt)
    code = resp.get('response', '').strip()
    if not code:
        print(f"[{pid}] No code generated.")
        return False

    # Ensure directories
    gen_dir = BASE_DIR / pid / INPUT_GENS_DIR
    gen_dir.mkdir(parents=True, exist_ok=True)
    chat_gen_dir = BASE_DIR / pid / CHAT_INPUTS_DIR
    chat_gen_dir.mkdir(parents=True, exist_ok=True)

    # Save raw generator
    raw_path = gen_dir / 'input_gen_raw.py'
    raw_path.write_text(code + '\n', encoding='utf-8')

    # Extract code blocks
    blocks = re.findall(r"```python\n([\s\S]*?)```", code)
    final_code = blocks[-1] if blocks else code

    # Save parsed generator
    parsed_path = gen_dir / 'input_gen.py'
    parsed_path.write_text(final_code + '\n', encoding='utf-8')

    return True

def execute_code(pid: str):
    try:
        gen_dir = BASE_DIR / pid / INPUT_GENS_DIR
        parsed = gen_dir / 'input_gen.py'
        if not parsed.exists():
            print(f"Skipping {pid}: no generator script found.")
            return False
        # Ensure output dir exists
        chat_gen_dir = BASE_DIR / pid / CHAT_INPUTS_DIR
        chat_gen_dir.mkdir(parents=True, exist_ok=True)

        print(f"[{pid}] Executing input_gen.py...")
        result = subprocess.run([sys.executable, parsed.name], cwd=gen_dir, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Exit {result.returncode}: {result.stderr}")
        return True
    except Exception as e:
        failed_pids.append(pid)
        failed_logs.append(f"[execute] {pid}: {str(e)}\nStdout:\n{result.stdout if 'result' in locals() else ''}\nStderr:\n{result.stderr if 'result' in locals() else ''}\n" + traceback.format_exc())
        return False

def main_generate(model: str, pid_list: Optional[Set[str]] = None):
    for d in BASE_DIR.iterdir():
        if not d.is_dir():
            continue
        pid = d.name
        if pid_list and pid not in pid_list:
            continue
        desc_file = d / 'spec.txt'
        if not desc_file.exists():
            print(f"Skipping {pid}: no description.")
            continue
        clear_directories(pid)
        generate_code(pid, desc_file.read_text(encoding='utf-8'), model)


def main_execute(pid_list: Optional[Set[str]] = None):
    for problem_dir in BASE_DIR.iterdir():
        if not problem_dir.is_dir():
            continue
        pid = problem_dir.name
        if pid_list and pid not in pid_list:
            continue
        execute_code(pid)

def clear_directories(pid: str):
    """Clear chat_generated_inputs and input_generator directories for a given problem."""
    for subdir in [INPUT_GENS_DIR, CHAT_INPUTS_DIR]:
        path = BASE_DIR / pid / subdir
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)

def write_logs():
    if failed_pids:
        FAILED_PIDS_FILE.write_text("\n".join(failed_pids), encoding='utf-8')
        FAILED_LOGS_FILE.write_text("\n".join(failed_logs), encoding='utf-8')
        print(f"Logged failures: {len(failed_pids)} items.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Auto Input Generator')
    parser.add_argument('--model', type=str, default='qwen3:8b')
    parser.add_argument('--file', type=str, default='pids.txt')
    parser.add_argument('--mode', choices=['generate', 'execute', 'both'], default='both',
                        help='Operation mode')
    args = parser.parse_args()

    pids = None
    if args.file:
        pids = set(Path(args.file).read_text().split())

    if args.mode in ('generate', 'both'):
        main_generate(args.model, pids)
    if args.mode in ('execute', 'both'):
        main_execute(pids)

    write_logs()

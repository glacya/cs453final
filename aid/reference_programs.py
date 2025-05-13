# Retrieves canonical programs from TrickyBugs & EvalPlus datasets.

import json
import os
import subprocess
from dotenv import load_dotenv
from pathlib import Path
from evalplus.data import get_human_eval_plus

base_dir = Path(__file__).resolve().parent

# Collect EvalPlus reference programs.
# EvalPlus reference programs are in Python language, consisting of function definitions and possible imports.
# Find aid/reference_programs/EvalPlus/HumanEval_*/ref.py file.
def get_evalplus_reference_programs():
    problems = get_human_eval_plus(mini=False)
    # TODO: Add input validator.
    # TODO: What if the solution code consists of multiple function definitions?

    for problem_key, problem_info in problems.items():
        problem_index = problem_key.split("/")[-1]

        problem_path = base_dir / f"datasets/EvalPlus/HumanEval_{problem_index}/ref.py"
        problem_path.parent.mkdir(parents=True, exist_ok=True)

        def_line = ""

        for line in problem_info["prompt"].split("\n"):
            def_line += line + "\n"

            if line.startswith("def"):
                break

        with open(problem_path, "w") as f:
            f.write(def_line)
            f.write(problem_info["canonical_solution"])


# IMPORTANT: You may not want to run this function.
# Collect TrickyBugs reference programs.
# TrickyBugs reference programs are in C++ language. They are in full program, and accept input file as an input.
# Thus, we save both program source code and compiled binary.
# Since the dataset for TrickyBugs are large, I decided to collect the programs and add them directly in git.
def get_trickybugs_reference_programs():
    load_dotenv()
    trickybugs_path = Path(os.getenv("TRICKYBUGS_PATH"))

    for problem_dir in trickybugs_path.iterdir():
        ref_path = problem_dir / "reference_programs/sol_0.cpp"

        output_path = base_dir / f"datasets/TrickyBugs/{problem_dir.name}"
        output_path.mkdir(parents=True, exist_ok=True)

        # g++ version: 13.3.0 on WSL Ubuntu 24.04
        try:
            subprocess.run(f"cp {str(ref_path)} {output_path}/ref.cpp && g++ -c {output_path}/ref.cpp -o {output_path}/ref", shell=True, capture_output=True, text=True)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    get_evalplus_reference_programs()
    # -- Do not execute the following line.
    get_trickybugs_reference_programs()
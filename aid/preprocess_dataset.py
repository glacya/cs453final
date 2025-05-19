import os
import subprocess
import shutil
from dotenv import load_dotenv
from pathlib import Path

base_dir = Path(__file__).resolve().parent
necessary_entries = [
    "variants",
    "metainfo.json",
    "put.py",
    "ref",
    "ref.cpp",
    "spec.txt"
]

# Load program variants and PUT from TrickyBugs directory of AID dataset.
def load_trickybugs_data_from_aid_dataset():
    # Use only Python programs.
    aid_variant_path = Path(os.getenv("AID_PATH")) / "TrickyBugs/GenProgs/aid_generated_progs_python"
    aid_put_path = Path(os.getenv("AID_PATH")) / "TrickyBugs/PUT_python"

    # Copy PUT
    for file_path in aid_put_path.glob("*/*.py"):
        dest_put_path = base_dir / f"datasets/TrickyBugs/{file_path.parent.name}/put.py"
        dest_put_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(file_path, dest_put_path)


    # Copy program variants
    for problem_dir in aid_variant_path.iterdir():
        for file_path in problem_dir.iterdir():
            if file_path.suffix == ".py":
                file_index = str(file_path.stem).split("_")[1][3:]
                file_name = f"variant{file_index}.py"

                dest_variant_path = base_dir / f"datasets/TrickyBugs/{problem_dir.name}/variants"
                dest_variant_path.mkdir(parents=True, exist_ok=True)

                shutil.copy2(file_path, dest_variant_path / file_name)

# Collect data from original TrickyBugs dataset.
# It loads problem specifications and reference programs.
def load_trickybugs_data_from_original_dataset():
    trickybugs_path = Path(os.getenv("TRICKYBUGS_PATH"))

    for problem_dir in trickybugs_path.iterdir():
        ref_path = problem_dir / "reference_programs/sol_0.cpp"
        spec_path = problem_dir / "problem_description.txt"
        metadata_path = problem_dir / "metainfo.json"

        output_path = base_dir / f"datasets/TrickyBugs/{problem_dir.name}"
        output_path.mkdir(parents=True, exist_ok=True)

        # Reference solutions are in C++, we need to compile them.
        # g++ version: 13.3.0 on WSL Ubuntu 24.04
        command = f"cp {spec_path} {output_path}/spec.txt; cp {metadata_path} {output_path}/metainfo.json;"
        command += f"cp {ref_path} {output_path}/ref.cpp && g++ -c {output_path}/ref.cpp -o {output_path}/ref"

        try:
            subprocess.run(command, shell=True, capture_output=True, text=True)
        except Exception as e:
            print(e)

# Copy original test cases for each problem directory
# from trickybugs/problem/original_test_cases to our dataset folder.
def load_original_test_cases():
    trickybugs_path = Path(os.getenv("TRICKYBUGS_PATH"))
    dataset_path = base_dir / "datasets/TrickyBugs"

    for problem_dir in trickybugs_path.iterdir():
        src_tests = problem_dir / "original_test_cases"
        if not src_tests.is_dir():
            continue

        dest_dir = dataset_path / problem_dir.name / "original_test_cases"
        dest_dir.mkdir(parents=True, exist_ok=True)

        for test_file in src_tests.iterdir():
            if test_file.is_file():
                shutil.copy2(test_file, dest_dir / test_file.name)


# AID filtered out some problems from original TrickyBugs/EvalPlus datasets.
# This file does removing incomplete problem directories.
# 
# The problem directory must contain following objects after preprocessing:
# - ref.cpp
# - ref
# - variants
#   - variantN.py
# - put.py
# - spec.txt
# - metainfo.json

def polish_trickybugs_problem_directory():
    dataset_path = base_dir / "datasets/TrickyBugs"

    polish_targets = []

    # For each problem path, check if it contains 6 full elements.
    # It skips checking children of /variants directory.
    for problem_path in dataset_path.iterdir():
        hit = 0
        has_og_test_cases = False
        for file_path in problem_path.iterdir():
            if file_path.name in necessary_entries:
                hit += 1

            if file_path.name == "original_test_cases":
                has_og_test_cases = True
        
        if not has_og_test_cases:
            print(problem_path.name)

        # Some of the element is missing. Destroy the directory.
        if hit < len(necessary_entries):
            polish_targets.append(problem_path)

    for p in polish_targets:
        shutil.rmtree(p)
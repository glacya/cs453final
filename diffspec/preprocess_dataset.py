import os
import subprocess
import shutil
from dotenv import load_dotenv
from pathlib import Path

base_dir = Path(__file__).resolve().parent
necessary_entries = [
    "variants",
    "put.py",
    "inputs",
    "ref",
    "ref.cpp",
]

# Load data from AID directory, and create separate dataset directory.
def load_trickybugs_data_from_aid_directory():
    aid_dataset_path = base_dir / "../aid/datasets/TrickyBugs"
    dest_path = base_dir / "datasets/TrickyBugs"

    for problem_path in aid_dataset_path.iterdir():
        variant_src_path = problem_path / "variants"
        put_src_path = problem_path / "put.py"
        ref_src_path = problem_path / "ref.cpp"

        problem_dest_path = dest_path / problem_path.stem
        variant_dest_path = problem_dest_path / "variants"
        put_dest_path = problem_dest_path / "put.py"
        ref_dest_path = problem_dest_path / "ref.cpp"

        shutil.copytree(variant_src_path, variant_dest_path, dirs_exist_ok=True)
        shutil.copy2(put_src_path, put_dest_path)
        shutil.copy2(ref_src_path, ref_dest_path)

# Load external test inputs generated with diffspec.
def load_trickybugs_data_from_diffspec_inputs_directory():
    diffspec_src_path = Path(os.getenv("DIFFSPEC_PATH"))
    diffspec_src_inner_path = diffspec_src_path / "generated_tests/parsed"
    diffspec_dest_path = base_dir / "datasets/TrickyBugs"

    # Copy inputs.
    for problem_dir in diffspec_src_inner_path.iterdir():
        dest_dir = diffspec_dest_path / problem_dir.stem / "inputs"

        dest_dir.mkdir(exist_ok=True, parents=True)

        for input_json_path in problem_dir.iterdir():
            shutil.copy2(input_json_path, dest_dir / input_json_path.name)




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
        for file_path in problem_path.iterdir():
            if file_path.name in necessary_entries:
                hit += 1

        # Some of the element is missing. Destroy the directory.
        if hit < len(necessary_entries):
            polish_targets.append(problem_path)

    for p in polish_targets:
        shutil.rmtree(p)

if __name__ == "__main__":
    load_dotenv()
    # load_trickybugs_data_from_aid_directory()
    load_trickybugs_data_from_diffspec_inputs_directory()
    polish_trickybugs_problem_directory()
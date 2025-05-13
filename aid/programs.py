# Collect PUTs and program variants from external dataset to repository folder.
# Note that this file can be removed from repository in the future.

from dotenv import load_dotenv
from pathlib import Path
import shutil
import os

base_dir = Path(__file__).resolve().parent

# Load program variants and PUT from EvalPlus directory of AID dataset.
def load_evalplus_programs():
    evalplus_variant_path = Path(os.getenv("AID_PATH")) / "EvalPlus/GenProgs/aid_generated_progs"
    evalplus_put_path = Path(os.getenv("AID_PATH")) / "EvalPlus/PUTs"

    # Copy PUT
    for file_path in evalplus_put_path.glob("*/*.py"):
        dest_put_path = base_dir / f"datasets/EvalPlus/{file_path.parent.name}/put.py"
        shutil.copy2(file_path, dest_put_path)

    # Copy program variants
    for problem_dir in evalplus_variant_path.iterdir():
        for file_path in problem_dir.iterdir():
            if file_path.suffix == ".py":
                file_name = f"variant{file_path.name}"

                dest_variant_path = base_dir / f"datasets/EvalPlus/{problem_dir.name}/variants"
                dest_variant_path.mkdir(parents=True, exist_ok=True)

                shutil.copy2(file_path, dest_variant_path / file_name)

# Load program variants and PUT from TrickyBugs directory of AID dataset.
def load_trickybugs_programs():
    # TODO: It excluded C++ programs.
    trickybugs_variant_path = Path(os.getenv("AID_PATH")) / "TrickyBugs/GenProgs/aid_generated_progs_python"
    trickybugs_put_path = Path(os.getenv("AID_PATH")) / "TrickyBugs/PUT_python"

    # Copy PUT
    for file_path in trickybugs_put_path.glob("*/*.py"):
        dest_put_path = base_dir / f"datasets/TrickyBugs/{file_path.parent.name}/put.py"
        shutil.copy2(file_path, dest_put_path)

    # Copy program variants
    for problem_dir in trickybugs_variant_path.iterdir():
        for file_path in problem_dir.iterdir():
            if file_path.suffix == ".py":
                file_index = str(file_path.stem).split("_")[1][3:]
                file_name = f"variant{file_index}.py"

                dest_variant_path = base_dir / f"datasets/TrickyBugs/{problem_dir.name}/variants"
                dest_variant_path.mkdir(parents=True, exist_ok=True)

                shutil.copy2(file_path, dest_variant_path / file_name)


if __name__ == "__main__":
    load_dotenv()

    load_evalplus_programs()
    load_trickybugs_programs()
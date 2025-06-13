# Here are the terms we use:
# - PUT: Program under test.
# - REF: Reference solution program. It is considered as ground truth.

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from collections import Counter
import subprocess
import time
import json

POOL_WORKERS = 6

# Executes program and collects the result.
# It assumes that input path is "/datasets/TrickyBugs/{pid}/inputs/{input_index}.json".

# DiffSpec version.
def execute_problem(problem_dir: Path) -> tuple:
    prob_start_time = time.time()
    print("Executing problem", problem_dir.name)

    invalid_input_format_files = 0
    total_input_files = 0
    
    put_failed = 0
    ref_failed = 0
    variant_failed = 0
    execution_failure_inputs = 0
    total_executed_inputs = 0
    
    put_variant0_diverse = 0
    put_variant0_fail = 0
    put_variant0_no_effect = 0

    has_diff_and_correct = 0
    has_diff_and_incorrect = 0
    no_diff_and_correct = 0
    no_diff_and_incorrect = 0

    # Define paths.
    input_dir = problem_dir / "inputs"
    put_path = problem_dir / "put.py"
    ref_src_path = problem_dir / "ref.cpp"
    ref_path = problem_dir / "ref"
    variant_dir = problem_dir / "variants"
    variant0_path = problem_dir / "variants/variant0.py"

    # Check if input directory is empty. If empty, skip and report.
    if input_dir.is_dir() and not any(input_dir.iterdir()):
        print(f"- Skipping {problem_dir.name}, input directory empty")

        return {
            # How many inputs are generated, compared to ideal numbers?
            "invalid_input_format_files": 0,
            "total_input_files": 0,
            
            # How many generated inputs get classified i.e. no error?
            "put_failed": 0,
            "ref_failed": 0,
            "variant_failed": 0,
            "execution_failure_inputs": 0,
            "total_executed_inputs": 0,
            # PUT vs variant0
            "put_variant0_diverse": 0,
            "put_variant0_fail": 0,
            "put_variant0_no_effect": 0,
            # Diversity-first classification
            "has_diff_and_correct": 0,
            "has_diff_and_incorrect": 0,
            "no_diff_and_correct": 0,
            "no_diff_and_incorrect": 0,
        }

    # Make directory for outputs.
    output_dir = problem_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Compile REF.
    subprocess.run(f"g++ {ref_src_path} -o {ref_path}; chmod +x {ref_path}", shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

    # Do not produce output files, just take them in memory. File operations are costly.
    input_set = set()

    for input_json in input_dir.glob("*.json"):
        content = None
        total_input_files += 1

        try:
            with open(input_json, "r") as f:
                content = json.load(f)
        except json.JSONDecodeError as e:
            invalid_input_format_files += 1
            continue


        for input_data in content:
            
            input_set.add(str(input_data).strip())

    
    for input_data in input_set:
        put_output = None
        ref_output = None
        variant0_output = None

        total_executed_inputs += 1

        put_failure = False
        variant0_failure = False

        # Run REF first. REF failure stops computing input immediately.
        try:
            ref_run = subprocess.run([str(ref_path)], capture_output=True, text=True, input=input_data, timeout=5, check=True)
            ref_output = ref_run.stdout.strip()

        except:
            ref_failed += 1
            continue

        # Run PUT and variant0.
        try:
            put_run = subprocess.run(["python", str(put_path)], capture_output=True, text=True, input=input_data, timeout=5, check=True)
            put_output = put_run.stdout.strip()

        except:
            put_failed += 1
            put_failure = True

        try:
            variant0_run = subprocess.run(["python", str(variant0_path)], capture_output=True, text=True, input=input_data, timeout=5, check=True)
            variant0_output = variant0_run.stdout.strip()
        except:
            variant0_failure = True
        
        # If both PUT and variant0 failed, mark input as reporting severe failure.
        # If one of PUT and variant0 failed, mark input as finding diversity.
        # If outputs of PUT and variant0 are different, mark input as finding diversity.
        if put_failure and variant0_failure:
            put_variant0_fail += 1
        elif put_failure or variant0_failure:
            put_variant0_diverse += 1
        elif put_output != variant0_output:
            put_variant0_diverse += 1
        else:
            put_variant0_no_effect += 1
        
        # Skip further operation if PUT failed.
        if put_failure:
            continue

        
        variant_outputs = []

        for variant_path in variant_dir.iterdir():
            try:
                variant_result = subprocess.run(["python", str(variant_path)], capture_output=True, text=True, input=input_data, timeout=5, check=True)

                variant_output = variant_result.stdout.strip()

                if variant_output != put_output:
                    variant_outputs.append(variant_output)
            except:
                variant_failed += 1
        

        variant_final_output = None
        variant_outputs = list(filter(lambda x: x is not None, variant_outputs))
        counter = Counter(variant_outputs)
        most_frequent = counter.most_common(1)

        if most_frequent:
            variant_final_output = most_frequent[0][0]
        else:
            # If no outputs disagreed with the output of PUT, then just use PUT's output.
            variant_final_output = put_output

        # Determine the type of test case.
        # Truth table here:
        ####################
        #   put == var      var == ref      Classification
        #   T               T               No diversity, no bug, no_diff_correct
        #   T               F               No diversity, had bug, no_diff_incorrect
        #   F               T               Found diversity, no bug, has_diff_correct
        #   F               F               Found diversity, had bug, has_diff_incorrect

        if put_output == variant_final_output:
            if variant_final_output == ref_output:
                no_diff_and_correct += 1
            else:
                no_diff_and_incorrect += 1
        else:
            if variant_final_output == ref_output:
                has_diff_and_correct += 1
            else:
                has_diff_and_incorrect += 1

    execution_failure_inputs = ref_failed + put_failed

    print(f"- Problem {problem_dir.name} took {time.time() - prob_start_time} seconds")

    return {
        # How many inputs are generated, compared to ideal numbers?
        "invalid_input_format_files": invalid_input_format_files,
        "total_input_files": total_input_files,
        # How many generated inputs get classified i.e. no error?
        "put_failed": put_failed,
        "ref_failed": ref_failed,
        "variant_failed": variant_failed,
        "execution_failure_inputs": execution_failure_inputs,
        "total_executed_inputs": total_executed_inputs,
        # PUT vs variant0
        "put_variant0_diverse": put_variant0_diverse,
        "put_variant0_fail": put_variant0_fail,
        "put_variant0_no_effect": put_variant0_no_effect,
        # Diversity-first classification
        "has_diff_and_correct": has_diff_and_correct,
        "has_diff_and_incorrect": has_diff_and_incorrect,
        "no_diff_and_correct": no_diff_and_correct,
        "no_diff_and_incorrect": no_diff_and_incorrect,
    }

def execute_programs_and_produce_statistics() -> dict:
    base_dir = Path(__file__).resolve().parent
    dataset_dir = base_dir / "datasets/TrickyBugs"
    begin_time = time.time()

    result_dict = None

    problem_paths = list(dataset_dir.iterdir())

    with ThreadPoolExecutor(max_workers=POOL_WORKERS) as executor:
        futures = {executor.submit(execute_problem, path): path for path in problem_paths}

        for future in as_completed(futures):
            path = futures[future]
            try:
                result = future.result()
                
                if result_dict is None:
                    result_dict = result
                else:
                    for key in result_dict:
                        result_dict[key] += result[key]

            except Exception as e:
                print(f"Error processing {path}: {e}")
    
    ratio_input_no_error = 1 - result_dict["execution_failure_inputs"] / result_dict["total_executed_inputs"]
    ratio_put_variant0_diversity = result_dict["put_variant0_diverse"] / (result_dict["total_executed_inputs"] - result_dict["ref_failed"])
    ratio_put_variant0_fail = result_dict["put_variant0_fail"] / (result_dict["total_executed_inputs"] - result_dict["ref_failed"])

    result_dict["ratio_input_no_error"] = ratio_input_no_error
    result_dict["ratio_put_variant0_diversity"] = ratio_put_variant0_diversity
    result_dict["ratio_put_variant0_fail"] = ratio_put_variant0_fail


    print(f"DiffSpec evaluation took {time.time() - begin_time} seconds in total")

    return result_dict


if __name__ == "__main__":

    result = execute_programs_and_produce_statistics()

    with open("diffspec_evaluation.txt", "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("Done. Evaluation result is written in diffspec_evaluation.txt.")
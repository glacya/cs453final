# Here are the terms we use:
# - PUT: Program under test.
# - REF: Reference solution program. It is considered as ground truth.

# Let newly produced test be T.
# True positive: PUT(T.in) != T.out && REF(T.in) == T.out
# False positive: T.in is invalid || PUT(T.in) != T.out && PUT(T.in) == REF(T.in)
# False negative: PUT(T.in) == T.out && PUT(T.in) != REF(T.in)

# Precision: Among the test cases that reported bugs, how many of them actually catched bugs?
# Recall: Among the test cases that touched the bug of PUT, how many of them identified the bugs?

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from collections import Counter
import subprocess
import time
import json

POOL_WORKERS = 10

# Executes program and collects the result.
# It assumes that input path is "/datasets/TrickyBugs/{pid}/inputs/{input_index}.in".

# AID version
def execute_problem(problem_dir: Path) -> tuple:
    prob_start_time = time.time()
    print("Executing problem", problem_dir.name)

    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    undetermined = 0
    variant_failed = 0
    put_failed = 0
    ref_failed = 0
    put_variant_different = 0
    total_inputs = 0

    # Define paths.
    input_dir = problem_dir / "chat_generated_inputs"
    put_path = problem_dir / "put.py"
    ref_src_path = problem_dir / "ref.cpp"
    ref_path = problem_dir / "ref"
    variant_dir = problem_dir / "variants"

    # Check if input directory is empty. If empty, skip and report.
    if input_dir.is_dir() and not any(input_dir.iterdir()):
        print(f"- Skipping {problem_dir.name}, input directory empty")
        return (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    # Make directory for outputs.
    output_dir = problem_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Compile REF.
    subprocess.run(["g++", str(ref_src_path), "-o", str(ref_path)])
    subprocess.run(["chmod", "+x", str(ref_path)])

    # For each input file, run PUT, variants, and reference program.
    # Then, inspect outputs to get statistical information.
    for input_path in input_dir.glob("*.in"):
        total_inputs += 1
        input_string = None

        with open(input_path, "r") as f:
            input_string = f.read()

        try:
            put_output = None
            ref_output = None

            # Run PUT.
            try:
                put_run = subprocess.run(["python", str(put_path)], input=input_string, capture_output=True, text=True, timeout=3, check=True)
                put_output = put_run.stdout.strip()
            except:
                put_failed += 1
                continue

            # Run reference program.
            try:
                ref_run = subprocess.run([str(ref_path)], input=input_string, capture_output=True, text=True, timeout=3, check=True)
                ref_output = ref_run.stdout.strip()
            except:
                ref_failed += 1
                continue

            # Run variants.
            variant_outputs = []

            for variant_path in variant_dir.iterdir():
                try:
                    variant_result = subprocess.run(["python", str(variant_path)], input=input_string, capture_output=True, text=True, timeout=3, check=True)
                    variant_outputs.append(variant_result.stdout.strip())
                except:
                    variant_failed += 1


            # T.out
            variant_final_output = None

            # Pick the most frequent one.
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
            #   put  var    ref     result
            #   A    A      A       TN (No bug, no detection)
            #   A    A      B       FN (Bug, no detection)
            #   A    B      A       FP (No bug, false detection)
            #   A    B      B       TP (Bug, correctly detected)
            #   A    B      C       ?? (Bug, detected, but the suggested output is wrong. Therefore, false detection)          

            if put_output == variant_final_output:
                if variant_final_output == ref_output:
                    true_negative += 1
                else:
                    false_negative += 1
            else:
                put_variant_different += 1

                if put_output == ref_output:
                    false_positive += 1
                elif variant_final_output == ref_output:
                    true_positive += 1
                else:
                    undetermined += 1

        except Exception as e:
            print(f"While running problem {problem_dir.name}, an exception occurred:")
            print(e)

    print(f"- Problem {problem_dir.name} took {time.time() - prob_start_time} seconds")

    return (true_positive, true_negative, false_positive, false_negative, undetermined, put_failed, ref_failed, variant_failed, put_variant_different, total_inputs)

def execute_programs_and_produce_statistics() -> dict:
    base_dir = Path(__file__).resolve().parent
    dataset_dir = base_dir / "datasets/TrickyBugs"
    begin_time = time.time()

    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    undetermined = 0
    put_failed = 0
    ref_failed = 0
    variant_failed = 0
    put_variant_different = 0
    total_inputs = 0

    no_chat_inputs_pid = base_dir / "no_chat_inputs_pid.txt"
    no_chat_inputs_list = ""

    problem_paths = list(dataset_dir.iterdir())

    with ThreadPoolExecutor(max_workers=POOL_WORKERS) as executor:
        futures = {executor.submit(execute_problem, path): path for path in problem_paths}

        for future in as_completed(futures):
            path = futures[future]
            try:
                result = future.result()
                
                true_positive += result[0]
                true_negative += result[1]
                false_positive += result[2]
                false_negative += result[3]
                undetermined += result[4]
                put_failed += result[5]
                ref_failed += result[6]
                variant_failed += result[7]
                put_variant_different += result[8]
                total_inputs += result[9]

            except Exception as e:
                print(f"Error processing {path}: {e}")


    for problem_dir in dataset_dir.iterdir():
        input_dir = problem_dir / "chat_generated_inputs"
        if input_dir.is_dir() and not any(input_dir.iterdir()):
            no_chat_inputs_list += f"{problem_dir.name}\n"

    if no_chat_inputs_list != "":
        with open(no_chat_inputs_pid, "w") as f:
            f.write(no_chat_inputs_list)

    # Precision = (TP) / (TP + FP)
    # Recall = (TP) / (TP + FN)
    # F1 = 2 / ((1 / Precision) + (1 / Recall))
    precision = 0
    recall = 0
    f1_score = 0

    if true_positive + false_positive > 0:
        precision = true_positive / (true_positive + false_positive)
    
    if true_positive + false_negative > 0:
        recall = true_positive / (true_positive + false_negative)

    if precision > 0 and recall > 0:
        f1_score = 2 / ((1 / precision) + (1 / recall))

    ratio_put_var_disagree = put_variant_different / (total_inputs - put_failed - ref_failed)
    ratio_input_no_error = 1 - (put_failed + ref_failed) / total_inputs

    print(f"AID evaluation took {time.time() - begin_time} seconds in total")

    return {
        "true_positive": true_positive,
        "true_negative": true_negative,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "undetermined": undetermined,
        "put_failed": put_failed,
        "ref_failed": ref_failed,
        "variant_failed": variant_failed,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "total_inputs": total_inputs,
        "ratio_put_var_disagree": ratio_put_var_disagree,
        "ratio_input_no_error": ratio_input_no_error,
    }

if __name__ == "__main__":
    aid_statistics = execute_programs_and_produce_statistics()

    with open("aid_evaluation.txt", "w") as f:
        json.dump(aid_statistics, f, indent=2, ensure_ascii=False)

    print("Done. Evaluation result is written in aid_evaluation.txt.")
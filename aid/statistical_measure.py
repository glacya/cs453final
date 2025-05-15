# Here are the terms we use:
# - PUT: Program under test.
# - REF: Reference solution program. It is considered as ground truth.

# Let newly produced test be T.
# True positive: PUT(T.in) != T.out && REF(T.in) == T.out
# False positive: T.in is invalid || PUT(T.in) != T.out && PUT(T.in) == REF(T.in)
# False negative: PUT(T.in) == T.out && PUT(T.in) != REF(T.in)

# Precision: Among the test cases that reported bugs, how many of them actually catched bugs?
# Recall: Among the test cases that touched the bug of PUT, how many of them identified the bugs?

from pathlib import Path
from collections import Counter
import subprocess

# Executes program and collects the result.
# It assumes that input path is "/datasets/TrickyBugs/{pid}/inputs/{input_index}.in".

# TODO: Expand the function so that it can support inputs from both AID and DiffSpec.
# TODO: Add input validation process
def execute_programs_and_produce_statistics() -> dict:
    base_dir = Path(__file__).resolve().parent
    dataset_dir = base_dir / "datasets/TrickyBugs"

    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0

    for problem_dir in dataset_dir.iterdir():
        # Define paths.
        input_dir = problem_dir / "inputs"
        put_path = problem_dir / "put.py"
        ref_path = problem_dir / "ref"
        variant_dir = problem_dir / "variants"

        # Make directory for outputs.
        output_dir = problem_dir / "outputs"
        output_dir.mkdir(parents=True, exist_ok=True)

        # For each input file, run PUT, variants, and reference program.
        # Then, inspect outputs to get statistical information.
        for input_path in input_dir.glob("*.in"):
            input_name = input_path.stem
            try:
                # Define output paths.
                put_output_path = output_dir / f"{input_name}.put.out"
                ref_output_path = output_dir / f"{input_name}.ref.out"

                # Run PUT.
                subprocess.run(f"python {put_path} < {input_path} > {put_output_path}")

                # Run reference program.
                subprocess.run(f"python {ref_path} < {input_path} > {ref_output_path}")

                # Run variants.
                variant_output_paths = []

                for variant_path in variant_dir.iterdir():
                    var_name = variant_path.stem

                    variant_output_path = output_dir / f"{input_name}.{var_name}.out"
                    subprocess.run(f"python {ref_path} < {input_path} < {variant_output_path}")

                    variant_output_paths.append(variant_output_path)

                # Now, check the outputs.
                
                # PUT(T.in)
                put_output = None

                # REF(T.in)
                ref_output = None

                # T.out
                variant_final_output = None

                with open(put_output_path, "r") as f:
                    put_output = f.read().rstrip()
                
                with open(ref_output_path, "r") as f:
                    ref_output = f.read().rstrip()

                # Pick the final output of test case, based on the outputs of variants.
                variant_outputs = []
                for p in variant_output_paths:
                    with open(p, "r") as f:
                        output = f.read().rstrip()

                        # Ignore if the output of variant is equal to the output of PUT.
                        if output == put_output:
                            continue

                        variant_outputs.append(output)

                # Pick the most frequent one.
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
                #   A    B      C       FP (Bug, detected, but the suggested output is wrong. Therefore, false detection)          

                if put_output == variant_final_output:
                    if variant_final_output == ref_output:
                        true_negative += 1
                    else:
                        false_negative += 1
                else:
                    if put_output == ref_output:
                        false_positive += 1
                    elif variant_final_output == ref_output:
                        true_positive += 1
                    else:
                        false_positive += 1

            except Exception as e:
                print(f"While running problem {problem_dir.name}, an exception occurred:")
                print(e)

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

    return {
        "true_positive": true_positive,
        "true_negative": true_negative,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score
    }
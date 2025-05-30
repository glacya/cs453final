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

POOL_WORKERS = 10

# Executes program and collects the result.
# It assumes that input path is "/datasets/TrickyBugs/{pid}/inputs/{input_index}.in".

# TODO: Expand the function so that it can support inputs from both AID and DiffSpec.
# TODO: Add input validation process
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

    # Define paths.
    input_dir = problem_dir / "chat_generated_inputs"
    put_path = problem_dir / "put.py"
    ref_src_path = problem_dir / "ref.cpp"
    ref_path = problem_dir / "ref"
    variant_dir = problem_dir / "variants"

    # Check if input directory is empty. If empty, skip and report.
    if input_dir.is_dir() and not any(input_dir.iterdir()):
        print(f"- Skipping {problem_dir.name}, input directory empty")
        return (0, 0, 0, 0, 0, 0, 0, 0)

    # Make directory for outputs.
    output_dir = problem_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Compile REF.
    subprocess.run(f"g++ {ref_src_path} -o {ref_path}; chmod +x {ref_path}", shell=True)

    # For each input file, run PUT, variants, and reference program.
    # Then, inspect outputs to get statistical information.
    for input_path in input_dir.glob("*.in"):
        input_name = input_path.stem
        try:
            # Define output paths.
            put_output_path = output_dir / f"{input_name}.put.out"
            ref_output_path = output_dir / f"{input_name}.ref.out"

            # Run PUT.
            try:
                subprocess.run(f"python {put_path} < {input_path} > {put_output_path}", shell=True, stderr=subprocess.DEVNULL, timeout=10)
            except:
                # log_file.write(f"- PUT failed to run input {input_name}")
                put_failed += 1
                continue

            # Run reference program.
            try:
                subprocess.run(f"{ref_path} < {input_path} > {ref_output_path}", shell=True, stderr=subprocess.DEVNULL, timeout=10)
            except:
                # log_file.write(f"- REF failed to run input {input_name}")
                ref_failed += 1
                continue

            # Run variants.
            # variant_num = len(list(variant_dir.iterdir()))

            variant_output_paths = []
            # variant_output_paths = [None for _ in range(variant_num)]
            # thread_handles = []

            # thread_values = {
            #     "output_dir": output_dir,
            #     "input_path": input_path,
            # }

            for i, variant_path in enumerate(variant_dir.iterdir()):
                # t = threading.Thread(target=variant_input_runner, args=[thread_values, variant_path, variant_output_paths, log_file, i])
                # t.start()
                # thread_handles.append(t)

                var_name = variant_path.stem

                variant_output_path = output_dir / f"{input_name}.{var_name}.out"
                try:
                    result = subprocess.run(f"python {variant_path} < {input_path} > {variant_output_path}", shell=True, stderr=subprocess.DEVNULL, timeout=10)

                    # Take output only if succeeded. Some variants are malformed, and we filter it out.
                    if result.returncode == 0:
                        variant_output_paths.append(variant_output_path)
                except:
                    variant_failed += 1
                    # log_file.write(f"- Variant {var_name} failed to run input {input_name}")

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
            # variant_outputs = [None for _ in range(variant_num)]
            variant_outputs = []
            # thread_handles = []

            for i, p in enumerate(variant_output_paths):
                if p is None:
                    continue

                # t = threading.Thread(target=variant_output_collector, args=[p, put_output, variant_outputs, i])
                # t.start()
                # thread_handles.append(t)

                # if p is None:
                #     continue

                with open(p, "r") as f:
                    output = f.read().rstrip()

                    # Ignore if the output of variant is equal to the output of PUT.
                    if output == put_output:
                        continue

                    variant_outputs.append(output)

            # for t in thread_handles:
            #     t.join()

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
                    undetermined += 1

        except Exception as e:
            print(f"While running problem {problem_dir.name}, an exception occurred:")
            print(e)

    print(f"- Problem {problem_dir.name} took {time.time() - prob_start_time} seconds")

    return (true_positive, true_negative, false_positive, false_negative, undetermined, put_failed, ref_failed, variant_failed)

def execute_programs_and_produce_statistics() -> dict:
    base_dir = Path(__file__).resolve().parent
    dataset_dir = base_dir / "datasets/TrickyBugs"

    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    undetermined = 0
    put_failed = 0
    ref_failed = 0
    variant_failed = 0

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
        "f1_score": f1_score
    }
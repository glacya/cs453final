import os
import argparse
import pandas as pd
from utils.data_utils import load_file, save_file, clean_diff_output
from utils.prompt_utils import (
    generate_differences_from_code_snippets,
    generate_test_descriptions_from_bug_code_diff,
    generate_test_body
)

failed_pids_diff = []
failed_pids_desc = []
failed_pids_body = []


def try_cached_or_generate(path, generator_fn):
    if os.path.exists(path):
        return load_file(path)
    else:
        result = generator_fn()
        save_file(result, path)
        return result


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run diff-based test generation in configurable stages"
    )
    parser.add_argument(
        "-m", "--mode",
        choices=["diffs", "descriptions", "bodies", "all"],
        default="all",
        help="Which stage to run: diffs, descriptions, bodies, or all"
    )
    parser.add_argument(
        "-f", "--file",
        default="pids.txt",
        help="Path to file listing project IDs (one per line)"
    )
    parser.add_argument(
        "--base-path",
        default="../aid/datasets/TrickyBugs",
        help="Base directory containing project folders"
    )
    parser.add_argument(
        "--output-path",
        default="generated_tests",
        help="Directory to store caches and outputs"
    )
    return parser.parse_args()


def read_pids(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PID file not found: {file_path}")
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def ensure_dirs(output_path):
    os.makedirs(os.path.join(output_path, "processed"), exist_ok=True)
    os.makedirs(os.path.join(output_path, "cache/diffs"), exist_ok=True)
    os.makedirs(os.path.join(output_path, "cache/descriptions"), exist_ok=True)


def run_diffs(pids, args):
    for i, subdir in enumerate(pids):
        print(f"\n[Problem {i}] {subdir}")
        problem_dir = os.path.join(args.base_path, subdir)
        spec_path = os.path.join(problem_dir, "spec.txt")
        buggy_path = os.path.join(problem_dir, "put.py")
        variant_path = os.path.join(problem_dir, "variants/variant0.py")
        example_path = os.path.join(problem_dir, "original_test_cases/sys_test0.in")
        if not all(os.path.exists(p) for p in [spec_path, buggy_path, variant_path, example_path]):
            print(f"[!] Skipping incomplete problem at {subdir}")
            continue

        spec = load_file(spec_path).strip()
        buggy_code = load_file(buggy_path)
        variant_code = load_file(variant_path)

        diff_cache = os.path.join(args.output_path, "cache/diffs", f"{subdir}.txt")
        try:
            raw_code_diffs = try_cached_or_generate(
                diff_cache,
                lambda: generate_differences_from_code_snippets(
                    "qwen3:8b", subdir, spec, buggy_code, variant_code, "buggy", "variant"
                )
            )
            code_diffs = clean_diff_output(raw_code_diffs)
        except Exception as e:
                print(f"[!] Exception during generation for {subdir} / error: {e}")
                failed_pids_diff.append(subdir)
                continue
        # saved to cache; further processing in descriptions/bodies stages


def run_descriptions(pids, args, bugs_df):
    for subdir in pids:
        print(f"\n[Descriptions] Processing {subdir}")
        problem_dir = os.path.join(args.base_path, subdir)
        spec_path = os.path.join(problem_dir, "spec.txt")
        diffs_path = os.path.join(args.output_path, "cache/diffs", f"{subdir}.txt")
        buggy_path = os.path.join(problem_dir, "put.py")
        variant_path = os.path.join(problem_dir, "variants/variant0.py")
        if not os.path.exists(spec_path) or not os.path.exists(diffs_path):
            print(f"[!] Missing spec or diffs for {subdir}, skipping descriptions.")
            continue
        spec = load_file(spec_path).strip()
        raw_code_diffs = load_file(diffs_path)
        code_diffs = clean_diff_output(raw_code_diffs)

        buggy_code = load_file(buggy_path)
        variant_code = load_file(variant_path)

        for k, bug in bugs_df.iterrows():
            bug_class = bug["bug_class"]
            bug_description = bug["description"]
            print(f"  [Bug {k}] {bug_class} - {bug_description}")
            desc_cache = os.path.join(
                args.output_path, "cache/descriptions",
                f"{subdir}_{k}.txt"
            )
            try:
                raw_nl = try_cached_or_generate(
                    desc_cache,
                    lambda diff=code_diffs, bug_class=bug_class, bug_description=bug_description: generate_test_descriptions_from_bug_code_diff(
                        "qwen3:8b", subdir, spec,
                        diff, bug_class, bug_description, "buggy", "variant", buggy_code, variant_code
                    )
                )
                #cleaned = clean_diff_output(raw_nl)
                # descriptions cached raw; bodies stage will split and prefix
            except Exception as e:
                print(f"[!] Exception during generation for {subdir} / bug {k}: {e}")
                failed_pids_desc.append(subdir)
                continue

def run_bodies(pids, args, bugs_df):
    for subdir in pids:
        print(f"\n[Bodies] Processing {subdir}")
        problem_dir = os.path.join(args.base_path, subdir)
        spec_path = os.path.join(problem_dir, "spec.txt")
        example_path = os.path.join(problem_dir, "original_test_cases/sys_test0.in")
        diffs_path = os.path.join(args.output_path, "cache/diffs", f"{subdir}.txt")
        if not all(os.path.exists(p) for p in [spec_path, example_path, diffs_path]):
            print(f"[!] Skipping incomplete problem at {subdir}")
            continue
        spec = load_file(spec_path).strip()
        example_tests = load_file(example_path)
        raw_code_diffs = load_file(diffs_path)
        code_diffs = clean_diff_output(raw_code_diffs)

        for k, bug in bugs_df.iterrows():
            bug_class = bug["bug_class"]
            bug_description = bug["description"]
            print(f"  [Bug {k}] {bug_class} - {bug_description}")
            desc_cache = os.path.join(
                args.output_path, "cache/descriptions",
                f"{subdir}_{k}.txt"
            )
            if not os.path.exists(desc_cache):
                continue
            raw_nl = load_file(desc_cache)
            nl_clean = clean_diff_output(raw_nl)
            nl_test_description = nl_clean #           nl_test_description = f"# Code diff: {code_diffs}\n{nl_clean}"
            try:
                generated = generate_test_body(
                    "qwen3:8b", subdir, spec, example_tests, nl_test_description
                )
            except Exception as e:
                print(f"[!] Exception during generation for {subdir} / bug {k}: {e}")
                failed_pids_body.append(subdir)
                continue
            out = generated.replace("#", "\n#")
            test_code = f"# {nl_test_description}\n{out}"
            out_file = f"{subdir}_{k}.py"
            save_file(test_code, os.path.join(args.output_path, "processed", out_file))

def write_logs():
    if failed_pids_diff:
        with open("failed_pids_diff.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(failed_pids_diff))
    if failed_pids_desc:
        with open("failed_pids_desc.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(failed_pids_desc))
    if failed_pids_body:
        with open("failed_pids_body.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(failed_pids_body))


def main():
    args = parse_args()
    ensure_dirs(args.output_path)
    pids = read_pids(args.file)
    bugs_df = pd.read_json('bug_categorization/AlgorithmicBugCategories.json')

    if args.mode in ("diffs", "all"):
        run_diffs(pids, args)
    if args.mode in ("descriptions", "all"):
        run_descriptions(pids, args, bugs_df)
    if args.mode in ("bodies", "all"):
        run_bodies(pids, args, bugs_df)

    if args.mode == "all":
        print("[O] Test generation completed.")
    
    write_logs()

if __name__ == "__main__":
    main()

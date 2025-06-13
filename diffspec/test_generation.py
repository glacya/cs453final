import os
import argparse
import pandas as pd
from utils.data_utils import load_file, save_file, clean_diff_output, strip_json_block
from utils.prompt_utils import (
    generate_differences_from_code_snippets,
    generate_test_descriptions_from_bug_code_diff,
    generate_test_body,
    generate_parsed_from_body
)

GEN_COUNT = 5

failed_pids_diff = []
failed_pids_desc = []
failed_pids_body = []
failed_pids_parse = []

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
        choices=["diffs", "descriptions", "bodies", "parse", "all"],
        default="all",
        help="Which stage to run: diffs, descriptions, bodies, parse, or all"
    )
    parser.add_argument(
        "-f", "--file",
        default="pids.txt",
        help="Path to file listing program IDs (one per line)"
    )
    parser.add_argument(
        "--base-path",
        default="datasets/TrickyBugs",
        help="Base directory containing program folders"
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
    os.makedirs(os.path.join(output_path, "parsed"), exist_ok=True)

def run_diffs(pids, args):
    for i, subdir in enumerate(pids):
        print(f"\n[Problem {i}] {subdir}")
        problem_dir = os.path.join(args.base_path, subdir)
        spec_path = os.path.join(problem_dir, "spec.txt")
        buggy_path = os.path.join(problem_dir, "put.py")
        variant_path = os.path.join(problem_dir, "variants/variant0.py")

        if not all(os.path.exists(p) for p in [spec_path, buggy_path, variant_path]):
            print(f"[!] Skipping incomplete problem at {subdir}")
            continue

        spec = load_file(spec_path).strip()
        buggy_code = load_file(buggy_path)
        variant_code = load_file(varasdfiant_path)

        diff_cache = os.path.join(args.output_path, "cache/diffs", f"{subdir}.txt")
        try:
            raw_code_diffs = try_cached_or_generate(
                diff_cache,
                lambda: generate_differences_from_code_snippets(
                    "qwen3:8b", spec, buggy_code, variant_code
                )
            )

        except Exception as e:
            print(f"[!] Exception during generation for {subdir} / error: {e}")
            failed_pids_diff.append(subdir)
            continue

def run_descriptions(pids, args):
    for subdir in pids:
        print(f"\n[Descriptions] Processing {subdir}")
        problem_dir = os.path.join(args.base_path, subdir)
        spec_path = os.path.join(problem_dir, "spec.txt")
        diffs_path = os.path.join(args.output_path, "cache/diffs", f"{subdir}.txt")
        if not os.path.exists(spec_path) or not os.path.exists(diffs_path):
            print(f"[!] Missing spec or diffs for {subdir}, skipping descriptions.")
            continue
        spec = load_file(spec_path).strip()
        code_diffs = clean_diff_output(load_file(diffs_path))

        for k in range(GEN_COUNT):
            print(f"  [Generation {k+1}/{GEN_COUNT}] Generating description")
            desc_cache = os.path.join(
                args.output_path, "cache/descriptions",
                f"{subdir}_{k}.txt"
            )
            try:
                raw_nl = try_cached_or_generate(
                    desc_cache,
                    lambda: generate_test_descriptions_from_bug_code_diff(
                        "qwen3:8b", spec, code_diffs,
                        load_file(os.path.join(problem_dir, "put.py")),
                        load_file(os.path.join(problem_dir, "variants/variant0.py"))
                    )
                )
            except Exception as e:
                print(f"[!] Exception during generation for {subdir} / generation {k}: {e}")
                failed_pids_desc.append(subdir)
                continue

def run_bodies(pids, args):
    for subdir in pids:
        print(f"\n[Bodies] Processing {subdir}")
        problem_dir = os.path.join(args.base_path, subdir)
        spec_path = os.path.join(problem_dir, "spec.txt")
        diffs_path = os.path.join(args.output_path, "cache/diffs", f"{subdir}.txt")
        if not all(os.path.exists(p) for p in [spec_path, diffs_path]):
            print(f"[!] Skipping incomplete problem at {subdir}")
            continue
        spec = load_file(spec_path).strip()

        for k in range(GEN_COUNT):
            print(f"  [Generation {k+1}/{GEN_COUNT}] Generating body")
            desc_cache = os.path.join(
                args.output_path, "cache/descriptions",
                f"{subdir}_{k}.txt"
            )
            if not os.path.exists(desc_cache):
                continue
            nl_clean = clean_diff_output(load_file(desc_cache))

            out_file = f"{subdir}_{k}.txt"
            proc_path = os.path.join(args.output_path, "processed", out_file)
            if os.path.exists(proc_path):
                continue

            try:
                generated = generate_test_body(
                    "qwen3:8b", spec, nl_clean
                )
            except Exception as e:
                print(f"[!] Exception during body gen for {subdir} / generation {k}: {e}")
                failed_pids_body.append(subdir)
                continue
            out = generated.replace("#", "\n#")
            test_code = f"# {nl_clean}\n{out}"
            save_file(test_code, proc_path)

def run_parse(pids, args):
    for subdir in pids:
        print(f"\n[Parse] Processing {subdir}")
        problem_dir = os.path.join(args.base_path, subdir)
        spec_path = os.path.join(problem_dir, "spec.txt")
        processed_dir = os.path.join(args.output_path, "processed")
        parsed_root = os.path.join(args.output_path, "parsed")
        parsed_subdir = os.path.join(parsed_root, subdir)
        os.makedirs(parsed_subdir, exist_ok=True)

        if not os.path.exists(spec_path):
            print(f"[!] Missing spec for {subdir}, skipping parse.")
            continue
        spec = load_file(spec_path).strip()

        for k in range(GEN_COUNT):
            processed_file = os.path.join(processed_dir, f"{subdir}_{k}.txt")
            if not os.path.exists(processed_file):
                continue
            out_file = f"chatGenInput_{k}.json"
            out_path = os.path.join(parsed_subdir, out_file)
            if os.path.exists(out_path):
                continue
            test_body = load_file(processed_file)
            body_clean = clean_diff_output(test_body)
            try:
                parsed = generate_parsed_from_body(
                    "qwen3:8b", spec, body_clean
                )
            except Exception as e:
                print(f"[!] Exception during parse for {subdir} / generation {k}: {e}")
                failed_pids_parse.append(subdir)
                continue
            cleaned_parsed = strip_json_block(clean_diff_output(parsed))
            save_file(cleaned_parsed, out_path)

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
    if failed_pids_parse:
        with open("failed_pids_parse.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(failed_pids_parse))

def main():
    args = parse_args()
    ensure_dirs(args.output_path)
    pids = read_pids(args.file)

    if args.mode in ("diffs", "all"):
        run_diffs(pids, args)
    if args.mode in ("descriptions", "all"):
        run_descriptions(pids, args)
    if args.mode in ("bodies", "all"):
        run_bodies(pids, args)
    if args.mode in ("parse", "all"):
        run_parse(pids, args)

    if args.mode == "all":
        print("[O] Test generation completed.")
    write_logs()

if __name__ == "__main__":
    main()

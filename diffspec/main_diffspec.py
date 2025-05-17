import os
import time
import pandas as pd
from utils.data_utils import load_file, save_file, clean_diff_output
from utils.prompt_utils import (
    generate_differences_from_code_snippets,
    generate_test_descriptions_from_bug_code_diff,
    generate_test_body
)

def try_cached_or_generate(path, generator_fn):
    if os.path.exists(path):
        return load_file(path)
    else:
        result = generator_fn()
        save_file(result, path)
        return result

def main():
    model = "qwen3:8b"
    base_path = "../aid/datasets/TrickyBugs"
    output_path = "generated_tests"
    os.makedirs(os.path.join(output_path, "processed"), exist_ok=True)
    os.makedirs(os.path.join(output_path, "cache/diffs"), exist_ok=True)
    os.makedirs(os.path.join(output_path, "cache/descriptions"), exist_ok=True)

    bugs_df = pd.read_json('bug_categorization/AlgorithmicBugCategories.json')

    subdirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    for i, subdir in enumerate(subdirs):
        problem_dir = os.path.join(base_path, subdir)
        spec_path = os.path.join(problem_dir, "spec.txt")
        buggy_path = os.path.join(problem_dir, "put.py")
        variant_path = os.path.join(problem_dir, "variants/variant0.py")
        example_path = os.path.join(problem_dir, 'original_test_cases/sys_test0.in')

        if not all(os.path.exists(p) for p in [spec_path, buggy_path, variant_path, example_path]):
            print(f"[!] Skipping incomplete problem at {subdir}")
            continue

        spec = load_file(spec_path).strip()
        buggy_code = load_file(buggy_path)
        variant_code = load_file(variant_path)
        example_tests = load_file(example_path)

        print(f"\n[Problem {i}] {subdir}")

        # Cache key for code diff
        diff_cache_path = os.path.join(output_path, "cache/diffs", f"{subdir}.txt")
        raw_code_diffs = try_cached_or_generate(
            diff_cache_path,
            lambda: generate_differences_from_code_snippets(
                model, subdir, spec, buggy_code, variant_code, "buggy", "variant"
            )
        )
        code_diffs = clean_diff_output(raw_code_diffs)

        for k, bug in bugs_df.iterrows():
            bug_class = bug["bug_class"]
            bug_description = bug["description"]
            print(f"  [Bug {k}] {bug_class} - {bug_description}")
            nl_test_descriptions_list = []

            for d, diff in enumerate(code_diffs.split("\n\n")):
                desc_cache_path = os.path.join(output_path, "cache/descriptions", f"{subdir}_{bug_class.replace(' ', '')}_{d}.txt")
                raw_nl_test_descriptions = try_cached_or_generate(
                    desc_cache_path,
                    lambda: generate_test_descriptions_from_bug_code_diff(
                        model, subdir, spec, diff, bug_class, bug_description, "buggy", "variant"
                    )
                )
                nl_test_descriptions = clean_diff_output(raw_nl_test_descriptions)
                nl_test_descriptions = [
                    f"# Code diff: {diff}\n{desc}" for desc in nl_test_descriptions.split("\n\n")
                ]
                nl_test_descriptions_list.extend(nl_test_descriptions)

            for j, nl_test_description in enumerate(nl_test_descriptions_list):
                nl_test_description = " ".join(nl_test_description.splitlines()).strip()
                generated_test = generate_test_body(
                    model, subdir, spec, example_tests, nl_test_description
                )
                generated_test = generated_test.replace("#", "\n#")
                print(generated_test)

                test_code = f"# {nl_test_description}\n{generated_test}"
                out_file = f"{subdir}_{bug_class.replace(' ', '')}_{j}.py"
                save_file(test_code, os.path.join(output_path, "processed", out_file))

    print("[✓] Test generation completed.")

if __name__ == "__main__":
    main()

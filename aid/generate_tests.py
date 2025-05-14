from pathlib import Path

input_loop = 10
base_dir = Path(__file__).resolve().parent

# Run input generator to create .json file.
# .json file is created by one per problem, regardless of 
def run_evalplus_input_generator(problem_name: str) -> dict:
    generator_path = base_dir / "datasets/EvalPlus" / problem_name / "generator.py"

    for i in range(input_loop):
        pass

# Input of TrickyBugs should be .in file.
# Run input generator to create .in files.
def run_trickybugs_input_generator(problem_name: str):
    pass

# Create and collect tests for EvalPlus problems.
def generate_evalplus_tests():
    dataset_path = base_dir / "datasets/EvalPlus"

    for problem_path in dataset_path.iterdir():
        generated_inputs = run_evalplus_input_generator(problem_path.name)

        # run_evalplus_


    pass

# Create and collect tests for TrickyBugs problems.
def generate_trickybugs_tests():
    pass


if __name__ == "__main__":
    generate_evalplus_tests()
    generate_trickybugs_tests()
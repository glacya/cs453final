# Import here.

from preprocess_dataset import *
from statistical_measure import *
import argparse
import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AID pipeline.')
    parser.add_argument('-p', '--preprocess', action="store_true", help="the target file to symbolically execute")
    args = parser.parse_args()

    if args.preprocess:
        print("Preprocessing dataset...")

        load_dotenv()

        print("Loading data from AID dataset...")
        load_trickybugs_data_from_aid_dataset()

        print("Loading data from TrickyBugs dataset...")
        load_trickybugs_data_from_original_dataset()

        print("Removing incomplete data...")
        polish_trickybugs_problem_directory()

        print("Preprocessing is finished.")
    else:
        print("Evaluating dataset...")

        # TODO: Implement the followings and add them in pipeline:
        # - Generate input generators
        # - Generate inputs

        aid_statistics = execute_programs_and_produce_statistics()

        with open("aid_evaluation.txt", "w") as f:
            json.dump(aid_statistics, f, indent=2, ensure_ascii=False)

        print("Done. Evaluation result is written in aid_evaluation.txt.")
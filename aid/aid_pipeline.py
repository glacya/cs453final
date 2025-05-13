from evalplus.data import get_human_eval_plus, get_human_eval_plus_hash
from evalplus.evaluate import get_groundtruth
import json



problems = get_human_eval_plus(mini=False)
dataset_hash = get_human_eval_plus_hash()
expected_output = get_groundtruth(problems, dataset_hash, []) 

problem_num = 150
problem_key = f"HumanEval/{problem_num}"

with open('output.json', 'w', encoding="utf-8") as f:
    json.dump(problems[problem_key], f, indent=2, ensure_ascii=False)

print(problems[problem_key]["canonical_solution"])

# with open('output.json', 'w', encoding='utf-8') as f:
    # json.dump(expected_output["HumanEval/1"], f, indent=2, ensure_ascii=False)

# print(expected_output["HumanEval/0"])
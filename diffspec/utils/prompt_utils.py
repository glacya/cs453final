from utils.model_utils import prompt_model

def generate_differences_from_code_snippets(model, problem_name, spec, src_buggy, src_correct, label_buggy, label_correct):
    prompt = f"""
You are an expert software testing engineer in python.

You are provided with the relevant code implementing the specification: 
{spec}

You have two implementations of that spec:

- Potentially buggy:
{src_buggy}

- Potentially correct:
{src_correct}

Identify **only** those code-level differences that would lead to different behaviors.  
Return **exactly** a Markdown list in this form (no extra text, no quotes):

FORMAT:
```
- The buggy version {{…}}, while the variant {{…}}
- The buggy version {{…}}, while the variant {{…}}
- …
- The buggy version {{…}}, while the variant {{…}}
```

"""
    return prompt_model(prompt.strip(), model, temperature=0.1)

def generate_test_descriptions_from_bug_code_diff(model, problem_name, spec, code_diff, bug_class, bug_description, label_buggy, label_correct, src_buggy, src_correct):
    prompt = f"""
You are an expert software testing engineer in python.

Here is the specification of the problem:
{spec}

You are provided with a list of differences in the code implementations for the specification in two different implementations:

- Potentially buggy:
{src_buggy}

- Potentially correct:
{src_correct}

- Key differences:
{code_diff}

And the actual implementation under test:
{src_buggy}

Your task is to generate natural language test descriptions that would expose the difference in behavior, especially that can be buggy.
Make it clear and simple.
Return **exactly** a Markdown list in this form (no extra text, no quotes):

FORMAT:
```
- A test case with {{...}}
- A test case with {{...}}
...
- A test case with {{...}}
```

"""
    return prompt_model(prompt.strip(), model, temperature=0.2, timeout=480.0)

def split_spec_by_constraints(spec: str):
    keyword = "CONSTRAINTS:"
    index = spec.find(keyword)

    if index == -1:
        raise ValueError("The keyword 'CONSTRAINTS:' was not found in the spec.")

    explanations = spec[:index].rstrip()
    constraints_and_examples = spec[index:].lstrip()

    return explanations, constraints_and_examples

def generate_test_body(model, problem_name, spec, example_tests, nl_test_description):
    explanations, constraints_and_examples = split_spec_by_constraints(spec)
    prompt = f"""
    You are an expert test engineer in python. You usualy generate inputs that match the given constraint and examples as your job.

    The goal is to find test inputs for differential tests that returns different outputs in different implementations for an problem so we can test for nuances in the two implementations based on the natural language specifications. 

    Here is a problem specification:

    {explanations}

    Here are the constraints and an examples explaining **THE EXACT FORMAT YOU SHOULD STRICTLY FOLLOW** when generating the test input:
    {constraints_and_examples}

    Here is a  **natural-language description** of the specific differential test we need:

    {nl_test_description}

    Your test input should follow the below format as a result inside the plaintext. 
    Only show the input in the ``` ```block after the 'input :' line. STRICTLY FOLLOW THE FORMAT

    FORMAT:

    # Test Case 1: {{brief one-line instruction from the description}}
    input :     
    ```
    {{the raw test input—just lines of values, no variable names or extra text}}
    ```

    """ 
    return prompt_model(prompt.strip(), model, temperature=0.05)

# 중간 버전
# prompt = f"""
# SYSTEM: ALWAYS wrap your entire test input in a single ```plaintext  ``` block and emit no other text.

# You are an expert test engineer in python.
# The goal is to find differential tests that returns different outputs in different implementations for this problem.

# Here is a problem specification:

# {explanations}

# Your goal is to generate differential tests so we can test for nuances in the two implementations based on the natural language specifications. 

# Here is the CONSTRAINT AND EXAMPLES that shows THE FORMAT YOU SHOULD STRICTLY FOLLOW when generating the test.
# CONSTRAINT AND EXAMPLES: 
# {constraints_and_examples}

# Here is a description of a test that can result in differential behaviour in the two implementations for the problem:

# {nl_test_description}

# Generate one input for the test in the same format as the CONSTRAINT AND EXAMPLES shows. 
# """ 
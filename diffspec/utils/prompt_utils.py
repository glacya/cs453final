from utils.model_utils import prompt_model

def generate_differences_from_code_snippets(model, problem_name, spec, src_buggy, src_correct, label_buggy, label_correct):
    prompt = f"""
You are an expert Python testing engineer.
The goal is to find differential tests that returns different outputs in different implementations of python.

You are provided with the relevant code implementing the instruction: 
{spec}

in two different implementations:

- Potentially buggy:
{src_buggy}

- Potentially correct:
{src_correct}

Identify and list the differences between the two code implementations that could indicate potential bugs or logic changes.
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

def generate_test_descriptions_from_bug_code_diff(model, problem_name, spec, code_diff, bug_class, bug_description, label_buggy, label_correct):
    prompt = f"""
You are an expert in software testing in python.
The goal is to find differential tests that returns different outputs in different implementations of python.

Here is the specification of the problem:
{spec}

And the difference of two implementaions:
{code_diff}

Your task is to generate natural language test descriptions that would expose the difference in behavior.
Focus on potential bugs when generating the test. Make it clear and simple.
Return **exactly** a Markdown list in this form (no extra text, no quotes):

FORMAT:
```
- A test case with {{explanation about the test case}}
- A test case with {{explanation about the test case}}
- A test case with {{explanation about the test case}}
...
- A test case with {{explanation about the test case}}
```

"""
    return prompt_model(prompt.strip(), model, temperature=0.35)

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

    Here is the CONSTRAINT AND EXAMPLES that shows THE FORMAT YOU SHOULD STRICTLY FOLLOW when generating the test input as an expert test engineer.
    # CONSTRAINT AND EXAMPLES: 
    {constraints_and_examples}

    Here is a description of a test that can result in differential behaviour in the two implementations for the problem:

    {nl_test_description}

    Your output should follow the below format as a result inside the plaintext, but the content should be from the differential test description.
    Only show the input in the ``` ```block after the 'input :' line. STRICTLY FOLLOW THE FORMAT

    FORMAT:

    # Test Case 1: {{the instruction written in the description}}
    ```
    input : 
    {{test input you generated. just the numbers of line and values of variables not the name of variables }}
    ```

    """ 
    return prompt_model(prompt.strip(), model, temperature=0.2)

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
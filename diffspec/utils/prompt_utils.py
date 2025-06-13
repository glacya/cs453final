from utils.model_utils import prompt_model

def generate_differences_from_code_snippets(model, spec, src_buggy, src_correct):
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

def generate_test_descriptions_from_bug_code_diff(model, spec, code_diff, src_buggy, src_correct):
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

def generate_test_body(model, spec, nl_test_description):
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
    return prompt_model(prompt.strip(), model, temperature=0.05, timeout=600.0)

def generate_parsed_from_body(model, spec, test_body):
    explanations, constraints_and_examples = split_spec_by_constraints(spec)

    prompt = f"""
    SYSTEM : You are a precise parser. 
    Your job is to take an arbitrary blob of text and return only the pieces that represent “input examples.” 
    You will output a JSON array of strings—each string is one input block. You must filter out anything that isn’t an input.

    Here’s a text dump.  Extract *all* of the input examples into a JSON list.  
    1. Recognize triple-backtick code fences, whether or not they contain the word “Input:” but it looks like a input.
    2. If there is no triple-backtick code fences, recognize lines or paragraphs prefixed by “Input:” even outside fences.  
    3. Discard any code/output/explanation that isn’t clearly part of an input example.  

    Return:
    [
    "first input example here…",
    "second input example here…",
    …
    ]

    You can check the constraint and examples how a input should look like from the examples.
    Constraints and Examples:
    {constraints_and_examples}

    Text dump:
    {test_body}

    """
    return prompt_model(prompt.strip(), model, temperature=0.05)
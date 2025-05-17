from utils.model_utils import prompt_model

def generate_differences_from_code_snippets(model, problem_name, spec, src_buggy, src_correct, label_buggy, label_correct):
    prompt = f"""
You are an expert software testing engineer in python.
Here is a problem specification written in natural language:

{spec}

You are provided with two implementations of the same problem.
One of them is potentially buggy ({label_buggy}) and the other is potentially correct ({label_correct}).

Implementation ({label_buggy}):
{src_buggy}

Implementation ({label_correct}):
{src_correct}

Identify and list the differences between the two code snippets that could indicate potential bugs or logic changes.
Return only the list of code-level differences that would lead to different behaviors.
"""
    return prompt_model(prompt.strip(), model)

def generate_test_descriptions_from_bug_code_diff(model, problem_name, spec, code_diff, bug_class, bug_description, label_buggy, label_correct):
    prompt = f"""
You are an expert in software testing in python.
You are working on the problem '{problem_name}'. Here is its specification:

{spec}

You found the following difference in two implementations:

{code_diff}

This difference may be related to the bug type: '{bug_class}'.
Bug description: {bug_description}

Your task is to generate natural language test descriptions that would expose the difference in behavior caused by this bug.
Focus on how the bug violates the specification. Provide only a list of test descriptions.
"""
    return prompt_model(prompt.strip(), model)

def generate_test_body(model, problem_name, spec, example_tests, nl_test_description):
    prompt = f"""
You are an expert test engineer in python.
The goal is to find differential tests that returns different outputs in different implementations for this problem.
Here is a problem specification:

{spec}

Your goal is to generate differential tests so we can test for nuances in the two implementations based on the natural language specifications. 

Here are some examples of existing tests for this problem.

{example_tests}

Here is a description of a test that can result in differential behaviour in the two implementations for the problem.
{nl_test_description}

Generate the code for the test in the same format as the example. 
You are required to strictly follow these instructions when generating the test.
1. Make sure you only generate one test.
2. Do not include comments in the same line as code.
Only generate the test case so it can be directly executed, and comment out any natural language descriptions describing what the test does."

"""
    return prompt_model(prompt.strip(), model)

# AID

### Things we can use in AID dataset folder:
 - Programs under test - PUT.
   - Datasets/TrickyBugs/PUT_python/p*/*.py
   - Datasets/TrickyBugs/PUT_cpp/p*/sol_*.cpp      <- Ignore if we only cover Python programs
   - Datasets/EvalPlus/PUTs/HumanEval_*/put*.py

 - Prompt template that generates input generator
   - Datasets/TrickyBugs/PromptTemplates/geninput_generator
   - Datasets/EvalPlus/PromptTemplates/geninput_generator_sys

 - Prompt template that generates program variants
   - Datasets/TrickyBugs/PromptTemplates/genprog_aid
   - Datasets/EvalPlus/PromptTemplates/genprog_aid_*

 - Generated input generators 

 - Generated program variants
   - Datasets/TrickyBugs/GenProgs/aid_generated_progs_python/&lt;probID&gt;/&lt;probID&gt;_num&lt;variantID&gt;_parsed.py
   - Datasets/EvalPlus/GenProgs/aid_generated_progs/&lt;probID/&lt;variantID&gt;.py

 - Problem metadata
   - Datasets/TrickyBugs/atcoder_difficultiy.json      <- It is not typo in text, original file name is mis-spelled


 ### What do we need to implement for AID?
 - Setup Ollama + llama 3.3 local LLM
 - Consult local LLM to generate input generator
 - ~~Consult local LLM to generate program variants~~ Use provided program variants
 - Generate set of test cases (input, output)
    - Run inputs on PUT and variants, and get outputs
    - Among the outputs, choose one that is the majority of outputs of all variants, which disagrees with PUT's output
 - Run test cases with reference solution programs (called canonical program in paper), and compare the result
    - Reference solutions are in TrickyBugs/EvalPlus dataset, but not in dataset provided by the author of AID paper.
    - Thus, we have to get reference solutions from dataset by ourselves.
 - Measure statistical metrics of generated output


## AID directory structure
- **/datasets**: Has everything for reproducing AID approach. It contains PUTs, program variants, input generators, and reference solutions.
  - **/EvalPlus**: Data from EvalPlus dataset.
  - **/TrickyBugs**: Data from TrickyBugs dataset.
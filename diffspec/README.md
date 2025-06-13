# DiffSpec

## DiffSpec directory structure


- **/bug_categorization**
  - **/algorithmbugcategories.json**: JSON file defining common algorithmic bug patterns. Used to guide test generation with prior bug knowledge.

- **/utils/**: Utility scripts for data processing, prompt construction, and model interaction.
  - **data_utils.py**: Helper functions for cleaning model outputs, parsing fenced JSON, and file I/O.
  - **model_utils.py**: Loads the LLM and sends prompts for response.
  - **prompt_utils.py**: Constructs prompt templates for different stages of the test generation pipeline.

- **/test_generation.py**: Main pipeline for generating test inputs.
Uses preprocessed dataset and utility functions to generate executable test cases using the DiffSpec method.

- **/statistical_measure.py**: Executes programs on generated test cases and computes evaluation metrics.

- **/preprocess_dataset.py**: Loads and prepares datasets from the AID structure for DiffSpec usage.
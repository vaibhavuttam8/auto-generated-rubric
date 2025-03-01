# AutoRubric Generator for DSA Problems

This tool automatically generates rubrics for Data Structures and Algorithms (DSA) problems based on the methodology described in the paper "AutoRubric: Autograding Template-Based Exam Programs" by Jonathon Cai.

## Overview

The AutoRubric Generator analyzes correct and incorrect solutions to DSA problems and creates detailed rubrics that can be used for grading student submissions. It works by:

1. Analyzing patterns in correct solutions to identify key components
2. Examining incorrect solutions to identify common mistakes
3. Generating rubric items that check for algorithmic correctness and efficiency
4. (Optional) Using OpenAI's API to enhance the rubrics with more sophisticated criteria

## Features

- Automatic extraction of rubric items from reference solutions
- Analysis of variable initializations, loop structures, and conditional logic
- Detection of common algorithm patterns in Java code
- Support for enhanced rubrics using OpenAI API
- Output in YAML format compatible with various grading systems

## Requirements

- Python 3.7+
- Required Python packages:
  - PyYAML
  - openai (optional, for enhanced rubrics)

## Installation

1. Clone this repository:
```
git clone <repository-url>
cd auto-rubric-generator
```

2. Install required packages:
```
pip install pyyaml openai
```

## Usage

1. Organize your DSA problems in the following structure:
```
DSA Dataset/
├── Category1/
│   ├── Problem1/
│   │   ├── Question.txt
│   │   ├── Solution.java
│   │   └── submissions/
│   │       ├── Correct_1/
│   │       │   └── Solution.java
│   │       ├── Correct_2/
│   │       │   └── Solution.java
│   │       └── Wrong/
│   │           └── Solution.java
│   └── Problem2/
│       └── ...
└── Category2/
    └── ...
```

2. (Optional) Set your OpenAI API key in the `auto_rubric_generator.py` file:
```python
OPENAI_API_KEY = "your-api-key"
```
python run_pipeline.py --openai-key "your-openai-api-key-here"

3. Run the script:
```
python auto_rubric_generator.py
```

4. The generated rubrics will be saved in the `generated_rubrics` directory.

## Generated Rubrics

The generated rubrics are in YAML format and include:

- Problem name and category
- Total points available
- Reference solution
- Rubric items with:
  - Description
  - Code fragment to check
  - Blank/section number
  - Score value

Example rubric item:
```yaml
- item: "[Variable initialization] max = Integer.MIN_VALUE"
  code_fragment: "max = Integer.MIN_VALUE"
  blank: "1" 
  score: 1.0
```

## Customizing Rubrics

After generating the initial rubrics, you can manually edit the YAML files to:

- Adjust scoring weights
- Add additional criteria
- Modify code fragments to check
- Add dependencies between rubric items

## Limitations

- Currently only supports Java code
- Best suited for algorithmic problems with well-defined solutions
- May require manual adjustments for complex algorithms
- Pattern extraction is based on regex and may miss some patterns

## Acknowledgments

- Based on the methodology in "AutoRubric: Autograding Template-Based Exam Programs" by Jonathon Cai
- Uses OpenAI API for enhanced rubric generation 
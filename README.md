# Tool Action Hierarchy Research

Research for whether action-based or domain-based hierarchies are better for organizing LLM tool calling.

## Overview

This repository contains a comprehensive Jupyter notebook that explores different approaches to organizing tools when calling Large Language Models (LLMs):

- **Domain-based hierarchies**: Tools grouped by domain (e.g., all file operations together)
- **Action-based hierarchies**: Tools grouped by action type (e.g., all read operations together)

The notebook includes:
- Accuracy and confusion testing
- Embedding model comparisons
- Scalability analysis
- Hybrid approaches combining both hierarchies

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Launch Jupyter:
```bash
jupyter notebook
```

3. Open `tool_hierarchy_optimization.ipynb`

## What's Inside

The notebook covers:

1. **Tool Set Definition**: Example tools across multiple domains (file, database, API, email, calendar)
2. **Hierarchy Creation**: Both domain-based and action-based organizational structures
3. **Test Queries**: Realistic user queries that map to specific tools
4. **Embedding-based Selection**: Using sentence transformers for semantic matching
5. **Accuracy Evaluation**: Comparing flat vs hierarchical approaches
6. **Confusion Analysis**: Understanding which tools are commonly confused
7. **Similarity Scoring**: Analyzing confidence levels across approaches
8. **Performance by Category**: Breaking down accuracy by domain and action type
9. **Embedding Model Comparison**: Testing multiple embedding models
10. **Summary & Recommendations**: Key findings and best practices
11. **Hybrid Approach**: Combining domain and action signals
12. **Scalability Analysis**: Performance with increasing tool counts

## Key Findings

The notebook demonstrates that:
- Hierarchical approaches can improve both accuracy and performance
- Domain-based hierarchies work better when queries clearly indicate the domain
- Action-based hierarchies excel when the action is clear but domain is ambiguous
- Better embedding models improve accuracy at the cost of computation
- Hybrid approaches combining both signals provide the best results

## Requirements

- Python 3.12+
- Jupyter Notebook
- See `requirements.txt` for full dependency list

## Optional

To test with actual LLM APIs, you can install:
```bash
pip install openai anthropic
```

## License

MIT

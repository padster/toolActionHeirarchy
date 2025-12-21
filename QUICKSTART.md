# Quick Start Guide

## Getting Started with Tool Hierarchy Optimization

This guide will help you get up and running with the tool hierarchy optimization notebook.

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Jupyter Notebook

## Installation

1. **Clone the repository** (if you haven't already):
```bash
git clone https://github.com/padster/toolActionHeirarchy.git
cd toolActionHeirarchy
```

2. **Create a virtual environment** (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

This will install:
- numpy, pandas for data manipulation
- matplotlib, seaborn for visualization
- scikit-learn for metrics and analysis
- sentence-transformers for embeddings
- jupyter for running the notebook

## Running the Notebook

1. **Launch Jupyter**:
```bash
jupyter notebook
```

2. **Open the notebook**:
   - In the Jupyter interface, click on `tool_hierarchy_optimization.ipynb`

3. **Run the cells**:
   - Run all cells: `Cell` → `Run All`
   - Or run cells individually: `Shift + Enter`

## What You'll Learn

### 1. Tool Organization Strategies
- **Domain-based**: Grouping tools by what they do (file ops, database ops, etc.)
- **Action-based**: Grouping tools by how they do it (read, write, delete)

### 2. Accuracy Analysis
- Compare different approaches using real test queries
- See confusion matrices showing which tools get mixed up
- Understand confidence scores (similarity values)

### 3. Embedding Models
- Test different sentence transformer models
- Balance accuracy vs computational cost
- See which models work best for tool selection

### 4. Scalability
- Understand how each approach performs with growing tool sets
- Compare execution times
- See when hierarchies provide the biggest benefits

### 5. Hybrid Approaches
- Combine domain and action signals
- Get the best of both worlds

## Customization

### Add Your Own Tools

Edit the `tools` list in Section 1:

```python
tools = [
    {
        "id": "my_tool",
        "name": "My Custom Tool",
        "description": "What my tool does",
        "domain": "my_domain",
        "action": "read"  # or "write" or "delete"
    },
    # ... more tools
]
```

### Add Your Own Test Queries

Edit the `test_queries` list in Section 3:

```python
test_queries = [
    {
        "query": "My test query",
        "expected_tool": "my_tool"
    },
    # ... more queries
]
```

### Try Different Embedding Models

In Section 9, add models to test:

```python
embedding_models_to_test = [
    'all-MiniLM-L6-v2',           # Fast
    'all-mpnet-base-v2',          # Accurate
    'paraphrase-MiniLM-L6-v2',    # Paraphrase detection
    'your-favorite-model',        # Add your own!
]
```

## Expected Results

When you run the notebook, you'll see:

1. **Tool Statistics**: Distribution of tools by domain and action
2. **Accuracy Metrics**: Comparison of flat vs hierarchical approaches
3. **Confusion Matrices**: Visual representation of prediction errors
4. **Performance Graphs**: Execution time vs number of tools
5. **Summary Report**: Key findings and recommendations

## Troubleshooting

### Model Download Issues

The first time you run the notebook, it will download embedding models (~100MB). If you have network issues:
- Check your internet connection
- Try a different model
- Set up a proxy if needed

### Memory Issues

If you run out of memory with large tool sets:
- Reduce `tool_counts` in Section 12
- Use smaller embedding models
- Reduce the number of test queries

### Jupyter Not Starting

If Jupyter won't start:
```bash
# Install/reinstall Jupyter
pip install --upgrade jupyter

# Try with a specific port
jupyter notebook --port=8889
```

## Next Steps

After running the notebook:

1. **Experiment with your own tools**: Add tools from your actual use case
2. **Test with real LLM APIs**: Integrate OpenAI or Anthropic APIs
3. **Implement in production**: Use the findings to optimize your tool calling
4. **Share your results**: Contribute back with your findings

## Getting Help

- Check the notebook markdown cells for detailed explanations
- Review the code comments for implementation details
- Run the validation script: `python3 validate_notebook.py`
- Open an issue on GitHub if you find bugs

## Performance Tips

1. **Cache embeddings**: Don't regenerate them on every run
2. **Use GPU**: If available, sentence-transformers will use it automatically
3. **Batch queries**: Process multiple queries at once for better throughput
4. **Profile your code**: Use `%%time` magic command to identify bottlenecks

## Contributing

Found a bug or have an improvement?
- Open an issue
- Submit a pull request
- Share your findings in discussions

## License

MIT - See LICENSE file for details

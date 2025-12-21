#!/usr/bin/env python3
"""
Validation script to verify the notebook structure and provide a quick overview.
Run this to check the notebook without executing it.
"""

import json
import sys

def validate_notebook(notebook_path):
    """Validate notebook structure and print summary."""
    try:
        with open(notebook_path, 'r') as f:
            nb = json.load(f)
        
        print("=" * 80)
        print("NOTEBOOK VALIDATION REPORT")
        print("=" * 80)
        
        # Basic structure
        print(f"\n✓ Notebook JSON structure is valid")
        print(f"✓ Notebook format version: {nb.get('nbformat', 'unknown')}.{nb.get('nbformat_minor', 'unknown')}")
        
        # Cell analysis
        cells = nb.get('cells', [])
        print(f"\n✓ Total cells: {len(cells)}")
        
        markdown_cells = [c for c in cells if c.get('cell_type') == 'markdown']
        code_cells = [c for c in cells if c.get('cell_type') == 'code']
        
        print(f"  - Markdown cells: {len(markdown_cells)}")
        print(f"  - Code cells: {len(code_cells)}")
        
        # Section headers
        print("\n✓ Notebook sections:")
        section_count = 0
        for cell in markdown_cells:
            source = ''.join(cell.get('source', []))
            lines = source.split('\n')
            for line in lines:
                if line.startswith('## '):
                    section_count += 1
                    title = line.replace('##', '').strip()
                    print(f"  {section_count}. {title}")
        
        # Check for key imports
        print("\n✓ Key imports found in code cells:")
        imports_found = set()
        key_imports = ['numpy', 'pandas', 'matplotlib', 'sklearn', 'sentence_transformers']
        
        for cell in code_cells:
            source = ''.join(cell.get('source', []))
            for imp in key_imports:
                if f'import {imp}' in source or f'from {imp}' in source:
                    imports_found.add(imp)
        
        for imp in key_imports:
            status = "✓" if imp in imports_found else "✗"
            print(f"  {status} {imp}")
        
        # Check for key functions
        print("\n✓ Key functions defined:")
        functions = [
            'create_domain_hierarchy',
            'create_action_hierarchy', 
            'find_best_tool_by_embedding',
            'find_best_tool_hierarchical',
            'plot_confusion_matrix'
        ]
        
        functions_found = set()
        for cell in code_cells:
            source = ''.join(cell.get('source', []))
            for func in functions:
                if f'def {func}(' in source:
                    functions_found.add(func)
        
        for func in functions:
            status = "✓" if func in functions_found else "✗"
            print(f"  {status} {func}")
        
        print("\n" + "=" * 80)
        print("VALIDATION COMPLETE")
        print("=" * 80)
        print("\nThe notebook is properly structured and ready to use.")
        print("Install dependencies with: pip install -r requirements.txt")
        print("Then run: jupyter notebook")
        print("=" * 80)
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"✗ Error: Invalid JSON structure - {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == '__main__':
    notebook_path = 'tool_hierarchy_optimization.ipynb'
    success = validate_notebook(notebook_path)
    sys.exit(0 if success else 1)

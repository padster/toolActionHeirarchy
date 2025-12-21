#!/usr/bin/env python3
"""
Example standalone script demonstrating tool hierarchy concepts.
This shows how to use the notebook concepts in a real application.

Usage:
    python3 example_usage.py
"""

from typing import List, Dict, Tuple
from collections import defaultdict

# Mock implementations for when packages aren't installed
try:
    import numpy as np
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    PACKAGES_AVAILABLE = True
except ImportError:
    PACKAGES_AVAILABLE = False
    np = None  # Set to None when not available


class ToolHierarchy:
    """Manages tool hierarchies for LLM tool calling."""
    
    def __init__(self, tools: List[Dict], embedding_model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the tool hierarchy.
        
        Args:
            tools: List of tool dictionaries with id, name, description, domain, action
            embedding_model_name: Name of the sentence transformer model to use
        """
        self.tools = tools
        self.embedding_model_name = embedding_model_name
        
        if PACKAGES_AVAILABLE:
            self.model = SentenceTransformer(embedding_model_name)
            # Pre-compute tool embeddings
            self.tool_descriptions = [f"{t['name']}: {t['description']}" for t in tools]
            self.tool_embeddings = self.model.encode(self.tool_descriptions)
        else:
            self.model = None
            self.tool_embeddings = None
        
        # Create hierarchies
        self.domain_hierarchy = self._create_hierarchy('domain')
        self.action_hierarchy = self._create_hierarchy('action')
    
    def _create_hierarchy(self, key: str) -> Dict[str, List[Dict]]:
        """Create a hierarchy based on a key (domain or action)."""
        hierarchy = defaultdict(list)
        for tool in self.tools:
            hierarchy[tool[key]].append(tool)
        return dict(hierarchy)
    
    def find_best_tool_flat(self, query: str) -> Tuple[str, float]:
        """
        Find the best tool using flat (non-hierarchical) search.
        
        Args:
            query: User query string
            
        Returns:
            Tuple of (tool_id, similarity_score)
        """
        if not PACKAGES_AVAILABLE:
            print("Error: Required packages not installed")
            return None, 0.0
        
        query_embedding = self.model.encode([query])
        similarities = cosine_similarity(query_embedding, self.tool_embeddings)[0]
        best_idx = int(np.argmax(similarities))
        return self.tools[best_idx]['id'], float(similarities[best_idx])
    
    def find_best_tool_hierarchical(self, query: str, hierarchy_type: str = 'domain') -> Tuple[str, float, str]:
        """
        Find the best tool using hierarchical search.
        
        Args:
            query: User query string
            hierarchy_type: Either 'domain' or 'action'
            
        Returns:
            Tuple of (tool_id, similarity_score, category)
        """
        if not PACKAGES_AVAILABLE:
            print("Error: Required packages not installed")
            return None, 0.0, None
        
        hierarchy = self.domain_hierarchy if hierarchy_type == 'domain' else self.action_hierarchy
        
        # Stage 1: Find best category
        categories = list(hierarchy.keys())
        category_descriptions = [f"{cat} operations" for cat in categories]
        category_embeddings = self.model.encode(category_descriptions)
        
        query_embedding = self.model.encode([query])
        category_similarities = cosine_similarity(query_embedding, category_embeddings)[0]
        best_category_idx = int(np.argmax(category_similarities))
        best_category = categories[best_category_idx]
        
        # Stage 2: Find best tool within category
        category_tools = hierarchy[best_category]
        category_tool_descriptions = [f"{tool['name']}: {tool['description']}" for tool in category_tools]
        category_tool_embeddings = self.model.encode(category_tool_descriptions)
        
        tool_similarities = cosine_similarity(query_embedding, category_tool_embeddings)[0]
        best_tool_idx = int(np.argmax(tool_similarities))
        
        return category_tools[best_tool_idx]['id'], float(tool_similarities[best_tool_idx]), best_category
    
    def get_tool_info(self, tool_id: str) -> Dict:
        """Get information about a specific tool."""
        for tool in self.tools:
            if tool['id'] == tool_id:
                return tool
        return None


def example_usage():
    """Demonstrate usage of the ToolHierarchy class."""
    
    # Define example tools
    tools = [
        {"id": "file_read", "name": "Read File", "description": "Read contents of a file", 
         "domain": "file", "action": "read"},
        {"id": "file_write", "name": "Write File", "description": "Write contents to a file", 
         "domain": "file", "action": "write"},
        {"id": "db_query", "name": "Query Database", "description": "Execute a SELECT query on database", 
         "domain": "database", "action": "read"},
        {"id": "db_insert", "name": "Insert Database", "description": "Insert records into database", 
         "domain": "database", "action": "write"},
        {"id": "api_get", "name": "API GET", "description": "Make HTTP GET request to API", 
         "domain": "api", "action": "read"},
        {"id": "email_send", "name": "Send Email", "description": "Send an email message", 
         "domain": "email", "action": "write"},
    ]
    
    print("=" * 80)
    print("Tool Hierarchy Example Usage")
    print("=" * 80)
    
    # Initialize hierarchy
    print("\nInitializing tool hierarchy...")
    hierarchy = ToolHierarchy(tools)
    
    print(f"✓ Loaded {len(tools)} tools")
    print(f"✓ Domain hierarchy: {list(hierarchy.domain_hierarchy.keys())}")
    print(f"✓ Action hierarchy: {list(hierarchy.action_hierarchy.keys())}")
    
    if not PACKAGES_AVAILABLE:
        print("\n⚠ Install required packages to test tool selection:")
        print("  pip install -r requirements.txt")
        return
    
    # Test queries
    test_queries = [
        "Show me the contents of config.json",
        "Save this data to a file",
        "Get all users from the database",
        "Send an email to the team",
    ]
    
    print("\n" + "=" * 80)
    print("Testing Tool Selection")
    print("=" * 80)
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        
        # Flat approach
        tool_id, score = hierarchy.find_best_tool_flat(query)
        tool_info = hierarchy.get_tool_info(tool_id)
        print(f"  Flat approach:")
        print(f"    → {tool_info['name']} (confidence: {score:.3f})")
        
        # Domain hierarchy
        tool_id, score, category = hierarchy.find_best_tool_hierarchical(query, 'domain')
        tool_info = hierarchy.get_tool_info(tool_id)
        print(f"  Domain hierarchy:")
        print(f"    → {tool_info['name']} via '{category}' domain (confidence: {score:.3f})")
        
        # Action hierarchy
        tool_id, score, category = hierarchy.find_best_tool_hierarchical(query, 'action')
        tool_info = hierarchy.get_tool_info(tool_id)
        print(f"  Action hierarchy:")
        print(f"    → {tool_info['name']} via '{category}' action (confidence: {score:.3f})")
    
    print("\n" + "=" * 80)
    print("Example completed!")
    print("=" * 80)
    print("\nNext steps:")
    print("  1. Open the Jupyter notebook for detailed analysis")
    print("  2. Add your own tools and test queries")
    print("  3. Integrate with your LLM application")
    print("=" * 80)


if __name__ == '__main__':
    example_usage()

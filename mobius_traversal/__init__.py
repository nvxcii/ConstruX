"""
Mobius MCP Recursive File System Traversal Protocol

A semantic surface traversal engine (SSTE) that treats file systems as
non-orientable topological surfaces. Recursively traverses directories,
extracts semantic relevance, builds dependency graphs, and refines
queries through Mobius inversion -- where discovered content transforms
the original query vector.

Architecture:
    Phase 1: Topology Mapping
    Phase 2: Semantic Relevance Extraction
    Phase 3: Mobius Inversion (recursive query refinement)
    Phase 4: Dependency Graph Construction
    Phase 5: Synthesis & Return
"""

from mobius_traversal.core import MobiusMCPTraversal
from mobius_traversal.semantic import SemanticAnalyzer
from mobius_traversal.graph import DependencyGraph

__version__ = "2.0.0"
__all__ = ["MobiusMCPTraversal", "SemanticAnalyzer", "DependencyGraph"]

"""
Example usage of the Mobius MCP Recursive File Traversal Protocol.

Demonstrates both programmatic API usage and the key phases of the
Semantic Surface Traversal Engine (SSTE).
"""

from mobius_traversal.core import MobiusMCPTraversal


def example_basic_traversal():
    """
    Basic traversal: scan a directory tree with a conversation context
    and get back ranked relevant files with semantic analysis.
    """
    engine = MobiusMCPTraversal(
        root_directories=["./multi_ai_framework"],
        conversation_context=(
            "How does the multi-AI coordination system distribute tasks "
            "across different AI models and aggregate their results?"
        ),
        max_depth=10,
        max_recursion=3,
        relevance_floor=0.25,
        novelty_threshold=0.1,
        preview_lines=80,
        top_n=15,
    )

    results = engine.execute()

    # Access top relevant artifacts
    for artifact in results["relevant_artifacts"][:5]:
        print(f"[{artifact['relevance_score']:.3f}] {artifact['path']}")
        print(f"  entities: {artifact['entities'][:5]}")

    # Check hub documents
    for hub in results["semantic_network"]["hub_documents"]:
        print(f"Hub: {hub['path']} (centrality: {hub['centrality']:.4f})")

    # Export full results
    engine.export_results("traversal_output.json", results)

    return results


def example_custom_analysis():
    """
    Use individual phases for custom analysis workflows.
    """
    engine = MobiusMCPTraversal(
        root_directories=["."],
        conversation_context="evidence database and violation tracking",
    )

    # Phase 1: Just get the topology
    topo = engine.phase_1_topology_mapping()
    for root, data in topo.items():
        print(f"Root: {root} -> {data['file_count']} files, depth {data['depth']}")

    # Phase 2: Score files
    relevant = engine.phase_2_semantic_extraction(topo)
    print(f"\nTop 5 relevant files:")
    for path, data in relevant[:5]:
        print(f"  [{data['score']:.3f}] {path}")

    return relevant


if __name__ == "__main__":
    print("=" * 60)
    print("  Mobius MCP Traversal - Example Usage")
    print("=" * 60)
    print()
    example_basic_traversal()

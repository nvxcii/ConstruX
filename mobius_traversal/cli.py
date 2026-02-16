"""
Command-line interface for the Mobius MCP Recursive File Traversal Protocol.

Usage:
    python -m mobius_traversal <root_dir> [root_dir ...] --context "query text"
    python -m mobius_traversal /path/to/code --context "authentication flow"
    python -m mobius_traversal . --context-file query.txt --output results.json
"""

import argparse
import json
import logging
import sys
from datetime import datetime

from mobius_traversal.core import MobiusMCPTraversal


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mobius-traversal",
        description=(
            "Mobius MCP Recursive File System Traversal Protocol v2.0 -- "
            "Semantic Surface Traversal Engine (SSTE)"
        ),
    )

    parser.add_argument(
        "roots",
        nargs="+",
        metavar="ROOT_DIR",
        help="Root directories to traverse",
    )

    context_group = parser.add_mutually_exclusive_group(required=True)
    context_group.add_argument(
        "--context", "-c",
        type=str,
        help="Conversation context / query text",
    )
    context_group.add_argument(
        "--context-file", "-f",
        type=str,
        help="Read conversation context from a file",
    )

    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Output JSON file path (default: stdout)",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=10,
        help="Maximum directory traversal depth (default: 10)",
    )
    parser.add_argument(
        "--max-recursion",
        type=int,
        default=5,
        help="Maximum Mobius inversion recursion depth (default: 5)",
    )
    parser.add_argument(
        "--relevance-floor",
        type=float,
        default=0.3,
        help="Minimum relevance score threshold (default: 0.3)",
    )
    parser.add_argument(
        "--novelty-threshold",
        type=float,
        default=0.1,
        help="Novelty threshold for Mobius re-traversal (default: 0.1)",
    )
    parser.add_argument(
        "--preview-lines",
        type=int,
        default=50,
        help="Number of lines to preview per file (default: 50)",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=20,
        help="Number of top relevant files to return (default: 20)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="count",
        default=0,
        help="Increase verbosity (-v info, -vv debug)",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print a human-readable summary instead of JSON",
    )

    return parser


def configure_logging(verbosity: int) -> None:
    level = logging.WARNING
    if verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def print_summary(results: dict) -> None:
    """Print a human-readable summary of traversal results."""
    meta = results.get("traversal_metadata", {})
    artifacts = results.get("relevant_artifacts", [])
    network = results.get("semantic_network", {})
    gaps = results.get("continuity_gaps", [])
    insights = results.get("mobius_insights", {})

    print("=" * 70)
    print("  MOBIUS MCP TRAVERSAL RESULTS")
    print("=" * 70)
    print()

    print(f"  Recursion depth achieved : {meta.get('depth_achieved', 0)}")
    print(f"  Convergence score        : {meta.get('convergence_score', 0):.2%}")
    print(f"  Total files scanned      : {meta.get('total_files_scanned', 0)}")
    print(f"  Relevant files found     : {meta.get('relevant_files_found', 0)}")
    print()

    if artifacts:
        print("-" * 70)
        print("  TOP RELEVANT ARTIFACTS")
        print("-" * 70)
        for i, art in enumerate(artifacts, 1):
            score = art.get("relevance_score", 0)
            path = art.get("path", "?")
            entities = art.get("entities", [])[:5]
            print(f"  {i:2d}. [{score:.3f}] {path}")
            if entities:
                print(f"      entities: {', '.join(entities)}")
        print()

    hubs = network.get("hub_documents", [])
    if hubs:
        print("-" * 70)
        print("  HUB DOCUMENTS (highest betweenness centrality)")
        print("-" * 70)
        for hub in hubs:
            print(f"    [{hub.get('centrality', 0):.4f}] {hub.get('path', '?')}")
        print()

    clusters = network.get("document_clusters", [])
    if clusters:
        print("-" * 70)
        print("  SEMANTIC CLUSTERS")
        print("-" * 70)
        for cl in clusters:
            print(f"  Cluster {cl['cluster_id']} ({cl['size']} docs, {cl['internal_edges']} edges)")
            for doc in cl["documents"][:5]:
                print(f"    - {doc}")
            if cl["size"] > 5:
                print(f"    ... and {cl['size'] - 5} more")
        print()

    if gaps:
        print("-" * 70)
        print(f"  CONTINUITY GAPS ({len(gaps)} missing references)")
        print("-" * 70)
        for gap in gaps[:10]:
            ref = gap.get("missing_reference", "?")
            by = gap.get("referenced_by", [])
            print(f"    {ref}")
            if by:
                print(f"      referenced by: {', '.join(by[:3])}")
        print()

    evolution = insights.get("context_evolution", [])
    if evolution:
        print("-" * 70)
        print("  MOBIUS INSIGHTS: CONTEXT EVOLUTION")
        print("-" * 70)
        for step in evolution:
            depth = step.get("depth", "?")
            novelty = step.get("novelty_score")
            if novelty is not None:
                new_kw = step.get("new_keywords", 0)
                new_ent = step.get("new_entities", 0)
                print(f"    Depth {depth}: novelty={novelty:.1%}, +{new_kw} keywords, +{new_ent} entities")
        print()

    themes = insights.get("emergent_themes", [])
    if themes:
        print("  Emergent themes:", ", ".join(themes[:10]))
        print()

    queries = results.get("suggested_next_queries", [])
    if queries:
        print("-" * 70)
        print("  SUGGESTED FOLLOW-UP QUERIES")
        print("-" * 70)
        for q in queries:
            print(f"    -> {q}")
        print()

    print("=" * 70)


def main(argv: list = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    configure_logging(args.verbose)

    # Load context
    if args.context_file:
        try:
            with open(args.context_file, "r", encoding="utf-8") as fh:
                context = fh.read()
        except OSError as exc:
            print(f"Error reading context file: {exc}", file=sys.stderr)
            return 1
    else:
        context = args.context

    if not context.strip():
        print("Error: empty context provided", file=sys.stderr)
        return 1

    # Execute traversal
    engine = MobiusMCPTraversal(
        root_directories=args.roots,
        conversation_context=context,
        max_depth=args.max_depth,
        max_recursion=args.max_recursion,
        relevance_floor=args.relevance_floor,
        novelty_threshold=args.novelty_threshold,
        preview_lines=args.preview_lines,
        top_n=args.top_n,
    )

    results = engine.execute()

    # Output
    if args.summary:
        print_summary(results)
    elif args.output:
        engine.export_results(args.output, results)
        print(f"Results written to {args.output}", file=sys.stderr)
    else:
        def _default(obj):
            if isinstance(obj, set):
                return sorted(obj)
            raise TypeError(f"Not serializable: {type(obj)}")

        json.dump(results, sys.stdout, indent=2, default=_default)
        print()  # trailing newline

    return 0


if __name__ == "__main__":
    sys.exit(main())

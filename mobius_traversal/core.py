"""
Core Mobius MCP Recursive File System Traversal Engine.

Implements the five-phase Semantic Surface Traversal Engine (SSTE):
    Phase 1: Topology Mapping
    Phase 2: Semantic Relevance Extraction
    Phase 3: Mobius Inversion (recursive query refinement)
    Phase 4: Dependency Graph Construction
    Phase 5: Synthesis & Return

The key insight is the Mobius property: traversing the file system
recursively, discovered content transforms the original query vector,
causing the traversal to return to its starting point *transformed*
with enhanced understanding that becomes the next query.
"""

import os
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from mobius_traversal.semantic import SemanticAnalyzer
from mobius_traversal.graph import DependencyGraph

logger = logging.getLogger(__name__)


# File extensions considered readable text for preview extraction
TEXT_EXTENSIONS = frozenset({
    ".py", ".js", ".ts", ".jsx", ".tsx", ".json", ".yaml", ".yml",
    ".md", ".txt", ".html", ".css", ".scss", ".sql", ".sh", ".bash",
    ".toml", ".cfg", ".ini", ".env", ".csv", ".xml", ".rst", ".go",
    ".rs", ".java", ".c", ".cpp", ".h", ".hpp", ".rb", ".php",
    ".swift", ".kt", ".r", ".m", ".vue", ".svelte",
})

# Directories to always skip
SKIP_DIRS = frozenset({
    ".git", "__pycache__", "node_modules", ".venv", "venv", "env",
    ".tox", ".mypy_cache", ".pytest_cache", "dist", "build",
    ".eggs", "*.egg-info", ".idea", ".vscode",
})


class MobiusMCPTraversal:
    """
    Recursive file system traversal treating directories as
    non-orientable semantic surfaces.
    """

    def __init__(
        self,
        root_directories: List[str],
        conversation_context: str,
        max_depth: int = 10,
        max_recursion: int = 5,
        convergence_threshold: float = 0.95,
        relevance_floor: float = 0.3,
        novelty_threshold: float = 0.1,
        preview_lines: int = 50,
        top_n: int = 20,
    ):
        self.roots = [os.path.abspath(r) for r in root_directories]
        self.context = conversation_context
        self.max_depth = max_depth
        self.max_recursion = max_recursion
        self.convergence_threshold = convergence_threshold
        self.relevance_floor = relevance_floor
        self.novelty_threshold = novelty_threshold
        self.preview_lines = preview_lines
        self.top_n = top_n

        self.semantic = SemanticAnalyzer()
        self.traversal_depth = 0
        self.topology_map: Dict[str, Dict[str, Any]] = {}
        self.discovered_nodes: List[Tuple[str, Dict[str, Any]]] = []
        self._context_history: List[Dict[str, Any]] = []

    # ═══════════════════════════════════════════════════════════════
    # PUBLIC API
    # ═══════════════════════════════════════════════════════════════

    def execute(self) -> Dict[str, Any]:
        """
        Run the complete 5-phase Mobius traversal and return
        a synthesis of the results.
        """
        logger.info("Phase 1: Topology Mapping")
        topo = self.phase_1_topology_mapping()

        logger.info("Phase 2: Semantic Extraction")
        relevant = self.phase_2_semantic_extraction(topo)

        logger.info("Phase 3: Mobius Inversion")
        refined = self.phase_3_mobius_inversion(relevant)

        logger.info("Phase 4: Dependency Graph Construction")
        dep_graph = self.phase_4_dependency_graph(refined)

        logger.info("Phase 5: Synthesis")
        return self.phase_5_synthesis(dep_graph)

    # ═══════════════════════════════════════════════════════════════
    # PHASE 1: TOPOLOGY MAPPING
    # ═══════════════════════════════════════════════════════════════

    def phase_1_topology_mapping(self) -> Dict[str, Dict[str, Any]]:
        """
        Initial surface scan: recursively list all accessible
        directories and build a complete topology map.
        """
        for root in self.roots:
            if not os.path.isdir(root):
                logger.warning("Root directory does not exist: %s", root)
                continue

            tree = self._recursive_list(root, current_depth=0)
            flat_files = self._flatten_file_tree(tree)

            self.topology_map[root] = {
                "root": root,
                "structure": tree,
                "file_count": len(flat_files),
                "depth": tree.get("max_depth", 0),
                "files": flat_files,
            }

        total = sum(t["file_count"] for t in self.topology_map.values())
        logger.info(
            "Topology mapped: %d roots, %d total files",
            len(self.topology_map),
            total,
        )
        return self.topology_map

    def _recursive_list(
        self, path: str, current_depth: int
    ) -> Dict[str, Any]:
        """Recursive directory traversal with depth limiting."""
        if current_depth > self.max_depth:
            return {"files": [], "subdirectories": [], "max_depth": current_depth, "truncated": True}

        files: List[Dict[str, Any]] = []
        subdirs: List[Dict[str, Any]] = []
        max_child_depth = current_depth

        try:
            entries = sorted(os.listdir(path))
        except PermissionError:
            logger.debug("Permission denied: %s", path)
            return {"files": [], "subdirectories": [], "max_depth": current_depth, "error": "access_denied"}
        except OSError as exc:
            logger.debug("OS error listing %s: %s", path, exc)
            return {"files": [], "subdirectories": [], "max_depth": current_depth, "error": str(exc)}

        for entry in entries:
            full_path = os.path.join(path, entry)

            if os.path.isdir(full_path):
                if entry in SKIP_DIRS or entry.startswith("."):
                    continue
                subtree = self._recursive_list(full_path, current_depth + 1)
                subdirs.append({
                    "name": entry,
                    "path": full_path,
                    "contents": subtree,
                })
                child_depth = subtree.get("max_depth", current_depth)
                max_child_depth = max(max_child_depth, child_depth)
            else:
                ext = os.path.splitext(entry)[1].lower()
                try:
                    stat = os.stat(full_path)
                    mtime = stat.st_mtime
                    size = stat.st_size
                except OSError:
                    mtime = 0.0
                    size = 0

                files.append({
                    "name": entry,
                    "path": full_path,
                    "extension": ext,
                    "is_text": ext in TEXT_EXTENSIONS,
                    "size_bytes": size,
                    "modification_time": mtime,
                    "relevance_score": 0.0,
                })

        return {
            "files": files,
            "subdirectories": subdirs,
            "max_depth": max_child_depth,
        }

    @staticmethod
    def _flatten_file_tree(tree: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Flatten nested directory tree into a single file list."""
        result: List[Dict[str, Any]] = []
        result.extend(tree.get("files", []))
        for subdir in tree.get("subdirectories", []):
            result.extend(
                MobiusMCPTraversal._flatten_file_tree(subdir.get("contents", {}))
            )
        return result

    # ═══════════════════════════════════════════════════════════════
    # PHASE 2: SEMANTIC RELEVANCE EXTRACTION
    # ═══════════════════════════════════════════════════════════════

    def phase_2_semantic_extraction(
        self, topology_map: Dict[str, Dict[str, Any]]
    ) -> List[Tuple[str, Dict[str, Any]]]:
        """
        The Mobius Twist: Content defines container relevance.
        Score all text files against the conversation context.
        """
        scored: Dict[str, Dict[str, Any]] = {}

        for _root, structure in topology_map.items():
            for file_info in structure.get("files", []):
                if not file_info.get("is_text"):
                    continue
                if file_info.get("size_bytes", 0) == 0:
                    continue

                path = file_info["path"]
                preview = self._get_file_preview(path)
                if not preview:
                    continue

                relevance = self.semantic.calculate_semantic_overlap(
                    self.context,
                    preview,
                    path,
                    modification_time=file_info.get("modification_time"),
                )

                if relevance >= self.relevance_floor:
                    entities = self.semantic.extract_entities(preview)
                    file_refs = self.semantic.extract_file_references(preview)
                    scored[path] = {
                        "score": relevance,
                        "preview": preview,
                        "entities": entities,
                        "file_references": file_refs,
                        "metadata": {
                            "size": file_info.get("size_bytes", 0),
                            "modified": file_info.get("modification_time", 0),
                            "extension": file_info.get("extension", ""),
                        },
                    }

        # Sort by relevance score descending
        self.discovered_nodes = sorted(
            scored.items(), key=lambda x: x[1]["score"], reverse=True
        )[: self.top_n]

        logger.info(
            "Phase 2 complete: %d files scored above threshold (%.2f), top %d selected",
            len(scored),
            self.relevance_floor,
            len(self.discovered_nodes),
        )
        return self.discovered_nodes

    def _get_file_preview(self, path: str) -> str:
        """Read the first N lines of a file as a preview."""
        try:
            lines: List[str] = []
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                for i, line in enumerate(fh):
                    if i >= self.preview_lines:
                        break
                    lines.append(line)
            return "".join(lines)
        except (OSError, UnicodeDecodeError) as exc:
            logger.debug("Could not read preview of %s: %s", path, exc)
            return ""

    # ═══════════════════════════════════════════════════════════════
    # PHASE 3: MOBIUS INVERSION -- RECURSIVE QUERY REFINEMENT
    # ═══════════════════════════════════════════════════════════════

    def phase_3_mobius_inversion(
        self,
        discovered_nodes: List[Tuple[str, Dict[str, Any]]],
    ) -> List[Tuple[str, Dict[str, Any]]]:
        """
        THE CRITICAL MOBIUS OPERATION:
        Discovered content transforms the query itself.

        Extract new semantic vectors from discovered files, expand
        the context, and re-run Phase 2 if significant novelty is found.
        """
        original_keywords = self.semantic.extract_keywords(self.context)
        original_entities = self.semantic.extract_entities(self.context)

        # Record initial context state
        self._context_history.append({
            "depth": self.traversal_depth,
            "keywords": len(original_keywords),
            "entities": len(original_entities),
        })

        # Synthesize expanded context from discovered previews
        expanded_keywords: Set[str] = set(original_keywords)
        expanded_entities: Set[str] = set(original_entities)
        new_connections: List[Dict[str, str]] = []

        for _path, data in discovered_nodes:
            preview = data.get("preview", "")
            expanded_keywords.update(self.semantic.extract_keywords(preview))
            expanded_entities.update(data.get("entities", set()))

        new_keywords = expanded_keywords - original_keywords
        new_entities = expanded_entities - original_entities

        # Find unexpected connections between original and new entities
        for orig in original_entities:
            for new_ent in new_entities:
                # Check if any document mentions both
                for _path, data in discovered_nodes:
                    preview = data.get("preview", "")
                    if orig.lower() in preview.lower() and new_ent.lower() in preview.lower():
                        new_connections.append({
                            "original": orig,
                            "discovered": new_ent,
                            "bridge_document": _path,
                        })
                        break

        # Measure novelty
        novelty = self.semantic.measure_context_expansion(
            original_keywords, original_entities,
            expanded_keywords, expanded_entities,
        )

        logger.info(
            "Mobius Inversion depth %d: novelty=%.1f%%, new_keywords=%d, "
            "new_entities=%d, connections=%d",
            self.traversal_depth,
            novelty * 100,
            len(new_keywords),
            len(new_entities),
            len(new_connections),
        )

        self._context_history.append({
            "depth": self.traversal_depth,
            "novelty_score": novelty,
            "new_keywords": len(new_keywords),
            "new_entities": len(new_entities),
            "new_connections": len(new_connections),
            "sample_new_entities": list(new_entities)[:10],
        })

        if novelty > self.novelty_threshold:
            self.traversal_depth += 1
            if self.traversal_depth < self.max_recursion:
                logger.info(
                    "Mobius Inversion: context expanded by %.1f%%, "
                    "re-running Phase 2 at depth %d",
                    novelty * 100,
                    self.traversal_depth,
                )
                # Expand context with new keywords for next pass
                expansion_terms = " ".join(list(new_keywords)[:50])
                self.context = self.context + "\n" + expansion_terms
                return self.phase_2_semantic_extraction(self.topology_map)
            else:
                logger.info("Convergence depth limit reached (%d)", self.max_recursion)
        else:
            logger.info(
                "Convergence achieved at depth %d (novelty %.1f%% <= threshold %.1f%%)",
                self.traversal_depth,
                novelty * 100,
                self.novelty_threshold * 100,
            )

        return self.discovered_nodes

    # ═══════════════════════════════════════════════════════════════
    # PHASE 4: DEPENDENCY GRAPH CONSTRUCTION
    # ═══════════════════════════════════════════════════════════════

    def phase_4_dependency_graph(
        self,
        discovered_nodes: List[Tuple[str, Dict[str, Any]]],
    ) -> Dict[str, Any]:
        """
        Build semantic network showing how documents reference each other.
        Identify hub documents, clusters, and continuity gaps.
        """
        graph = DependencyGraph()
        all_references: Set[str] = set()
        node_paths = {path for path, _ in discovered_nodes}

        for path, data in discovered_nodes:
            graph.add_node(
                path,
                score=data.get("score", 0),
                entities=list(data.get("entities", set()))[:20],
                file_references=data.get("file_references", set()),
            )

            file_refs = data.get("file_references", set())
            all_references.update(file_refs)

            for ref in file_refs:
                # Match against discovered nodes by substring
                for candidate in node_paths:
                    if candidate == path:
                        continue
                    # Check if the reference matches the candidate path
                    ref_normalized = ref.replace("\\", "/")
                    cand_normalized = candidate.replace("\\", "/")
                    if (
                        ref_normalized in cand_normalized
                        or cand_normalized.endswith(ref_normalized)
                        or os.path.basename(ref_normalized)
                        == os.path.basename(cand_normalized)
                    ):
                        graph.add_edge(path, candidate)

        hub_docs = graph.hub_documents(top_n=5)
        clusters = graph.identify_clusters()
        gaps = graph.identify_continuity_gaps(all_references)
        bridges = graph.map_cluster_bridges(clusters)

        logger.info(
            "Phase 4 complete: %d nodes, %d edges, %d clusters, %d gaps",
            len(graph.nodes),
            graph.edge_count,
            len(clusters),
            len(gaps),
        )

        return {
            "graph": graph,
            "hub_documents": hub_docs,
            "clusters": clusters,
            "missing_links": gaps,
            "bridges": bridges,
        }

    # ═══════════════════════════════════════════════════════════════
    # PHASE 5: SYNTHESIS & RETURN
    # ═══════════════════════════════════════════════════════════════

    def phase_5_synthesis(
        self, dependency_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Present unified understanding as a comprehensive result dict.
        """
        graph: DependencyGraph = dependency_result["graph"]

        return {
            "traversal_metadata": {
                "depth_achieved": self.traversal_depth,
                "convergence_score": self._calculate_convergence(),
                "total_files_scanned": sum(
                    t["file_count"] for t in self.topology_map.values()
                ),
                "relevant_files_found": len(self.discovered_nodes),
                "roots_traversed": list(self.topology_map.keys()),
            },
            "relevant_artifacts": [
                {
                    "path": path,
                    "relevance_score": round(data["score"], 4),
                    "key_passage": data["preview"][:500],
                    "entities": sorted(data.get("entities", set()))[:15],
                    "metadata": data.get("metadata", {}),
                }
                for path, data in self.discovered_nodes[:15]
            ],
            "semantic_network": {
                "hub_documents": [
                    {"path": p, "centrality": round(c, 6)}
                    for p, c in dependency_result["hub_documents"]
                ],
                "document_clusters": [
                    {
                        "cluster_id": c["cluster_id"],
                        "documents": c["documents"],
                        "size": c["size"],
                        "internal_edges": c["internal_edges"],
                    }
                    for c in dependency_result["clusters"]
                ],
                "inter_cluster_connections": dependency_result["bridges"],
                "graph_summary": graph.to_dict(),
            },
            "continuity_gaps": dependency_result["missing_links"][:20],
            "suggested_next_queries": self._generate_follow_up_vectors(),
            "mobius_insights": {
                "context_evolution": self._context_history,
                "emergent_themes": self._identify_emergent_patterns(),
                "recursive_depth_value": self._assess_depth_contribution(),
            },
        }

    # ── Synthesis helpers ────────────────────────────────────────────

    def _calculate_convergence(self) -> float:
        """
        Calculate how well the traversal converged.
        Based on the last novelty score relative to the threshold.
        """
        if len(self._context_history) < 2:
            return 1.0
        last_novelty = self._context_history[-1].get("novelty_score", 0)
        if last_novelty <= self.novelty_threshold:
            return 1.0
        return max(0.0, 1.0 - last_novelty)

    def _identify_emergent_patterns(self) -> List[str]:
        """
        Identify themes that appeared during recursive traversal
        but were not present in the original context.
        """
        if len(self._context_history) < 2:
            return []

        patterns: List[str] = []
        for entry in self._context_history:
            sample = entry.get("sample_new_entities", [])
            for ent in sample:
                if ent not in patterns:
                    patterns.append(ent)
        return patterns[:20]

    def _assess_depth_contribution(self) -> Dict[str, Any]:
        """
        Assess how much each recursion depth contributed to
        the final understanding.
        """
        contributions: List[Dict[str, Any]] = []
        for entry in self._context_history:
            if "novelty_score" in entry:
                contributions.append({
                    "depth": entry["depth"],
                    "novelty_added": round(entry["novelty_score"], 4),
                    "new_keywords": entry.get("new_keywords", 0),
                    "new_entities": entry.get("new_entities", 0),
                })
        return {
            "total_depth": self.traversal_depth,
            "contributions": contributions,
        }

    def _generate_follow_up_vectors(self) -> List[str]:
        """
        Generate suggested follow-up queries based on discovered
        entities and gaps.
        """
        vectors: List[str] = []

        # From emergent entities
        patterns = self._identify_emergent_patterns()
        for entity in patterns[:5]:
            vectors.append(f"Explore connections to: {entity}")

        # From discovered but low-scoring files
        if len(self.discovered_nodes) > 5:
            tail = self.discovered_nodes[5:]
            for path, data in tail[:3]:
                name = os.path.basename(path)
                vectors.append(f"Deep-dive into: {name} (score: {data['score']:.2f})")

        return vectors

    # ── JSON export ──────────────────────────────────────────────────

    def export_results(self, output_path: str, results: Dict[str, Any]) -> str:
        """Export traversal results to a JSON file."""

        def _serialize(obj: Any) -> Any:
            if isinstance(obj, set):
                return sorted(obj)
            if isinstance(obj, datetime):
                return obj.isoformat()
            if isinstance(obj, DependencyGraph):
                return obj.to_dict()
            raise TypeError(f"Not serializable: {type(obj)}")

        out = os.path.abspath(output_path)
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(results, fh, indent=2, default=_serialize)
        logger.info("Results exported to %s", out)
        return out

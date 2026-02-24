"""
Core Mobius MCP Recursive File System Traversal Engine.

Implements the five-phase Semantic Surface Traversal Engine (SSTE):
    Phase 1: Topology Mapping  (directories ARE content)
    Phase 2: Semantic Relevance Extraction
    Phase 3: Mobius Inversion  (true inversion: re-evaluate the original
             query through discovered knowledge, not context accumulation)
    Phase 4: Dependency Graph Construction
    Phase 5: Synthesis & Return

Key design principles from the Mobius refinement:
    - Container / Content boundary dissolution: directories are semantic
      entities, not just holders of files. The nesting IS a sentence.
    - True inversion: the original query is preserved immutably.
      Discovered content produces a *lens*, not an expansion.
    - Surface closure: the traversal is complete when the set of
      discovered node paths stabilizes across passes.
    - Indexer, not holder: state can be saved and loaded so that each
      pass deepens structural awareness across invocations.
"""

import os
import json
import hashlib
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

    The traversal dissolves the container/content boundary:
    directories are scored as semantic entities alongside files.
    The Mobius inversion preserves the original query immutably
    and uses discovered knowledge as a lens for re-evaluation.
    Surface closure is detected when the discovered node set
    stabilizes across recursive passes.
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
        index_path: Optional[str] = None,
    ):
        self.roots = [os.path.abspath(r) for r in root_directories]
        self.original_context = conversation_context  # immutable original
        self.context = conversation_context            # working copy (lens-augmented)
        self.max_depth = max_depth
        self.max_recursion = max_recursion
        self.convergence_threshold = convergence_threshold
        self.relevance_floor = relevance_floor
        self.novelty_threshold = novelty_threshold
        self.preview_lines = preview_lines
        self.top_n = top_n
        self.index_path = index_path

        self.semantic = SemanticAnalyzer()
        self.traversal_depth = 0
        self.topology_map: Dict[str, Dict[str, Any]] = {}
        self.discovered_nodes: List[Tuple[str, Dict[str, Any]]] = []
        self.directory_nodes: List[Tuple[str, Dict[str, Any]]] = []
        self._context_history: List[Dict[str, Any]] = []

        # Surface closure tracking: the set of discovered paths per pass
        self._surface_snapshots: List[Set[str]] = []
        self._surface_closed = False

        # Persistent index: accumulated structural knowledge
        self._index: Dict[str, Any] = {}
        if index_path and os.path.isfile(index_path):
            self._load_index(index_path)

    # ═══════════════════════════════════════════════════════════════
    # PUBLIC API
    # ═══════════════════════════════════════════════════════════════

    def execute(self) -> Dict[str, Any]:
        """
        Run the complete 5-phase Mobius traversal and return
        a synthesis of the results.
        """
        logger.info("Phase 1: Topology Mapping (directories as content)")
        topo = self.phase_1_topology_mapping()

        logger.info("Phase 2: Semantic Extraction")
        relevant = self.phase_2_semantic_extraction(topo)

        logger.info("Phase 3: Mobius Inversion (true inversion)")
        refined = self.phase_3_mobius_inversion(relevant)

        logger.info("Phase 4: Dependency Graph Construction")
        dep_graph = self.phase_4_dependency_graph(refined)

        logger.info("Phase 5: Synthesis")
        results = self.phase_5_synthesis(dep_graph)

        # Persist index for future invocations
        if self.index_path:
            self._save_index(self.index_path)

        return results

    # ═══════════════════════════════════════════════════════════════
    # PHASE 1: TOPOLOGY MAPPING — DIRECTORIES AS CONTENT
    # ═══════════════════════════════════════════════════════════════

    def phase_1_topology_mapping(self) -> Dict[str, Dict[str, Any]]:
        """
        Initial surface scan. Key change from v1: directories are
        analyzed as semantic entities alongside files. A directory's
        name, position, siblings, and children encode meaning that
        is independent of the files it contains.
        """
        all_dirs: List[Dict[str, Any]] = []

        for root in self.roots:
            if not os.path.isdir(root):
                logger.warning("Root directory does not exist: %s", root)
                continue

            tree = self._recursive_list(root, current_depth=0)
            flat_files = self._flatten_file_tree(tree)
            flat_dirs = self._flatten_directory_tree(tree)
            all_dirs.extend(flat_dirs)

            self.topology_map[root] = {
                "root": root,
                "structure": tree,
                "file_count": len(flat_files),
                "directory_count": len(flat_dirs),
                "depth": tree.get("max_depth", 0),
                "files": flat_files,
                "directories": flat_dirs,
            }

        # Score directories against context (container = content)
        for dir_info in all_dirs:
            dir_semantics = self.semantic.analyze_directory_semantics(
                dir_info["path"]
            )
            relevance = self.semantic.score_directory_relevance(
                dir_semantics, self.context
            )
            dir_info["relevance_score"] = relevance
            dir_info["semantic_profile"] = dir_semantics

        self.directory_nodes = [
            (d["path"], d) for d in all_dirs if d.get("relevance_score", 0) > 0.1
        ]
        self.directory_nodes.sort(key=lambda x: x[1]["relevance_score"], reverse=True)

        total_files = sum(t["file_count"] for t in self.topology_map.values())
        total_dirs = sum(t["directory_count"] for t in self.topology_map.values())
        logger.info(
            "Topology mapped: %d roots, %d files, %d directories "
            "(%d dirs scored as relevant content)",
            len(self.topology_map),
            total_files,
            total_dirs,
            len(self.directory_nodes),
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

    @staticmethod
    def _flatten_directory_tree(tree: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Flatten nested directory tree into a list of directory entries."""
        result: List[Dict[str, Any]] = []
        for subdir in tree.get("subdirectories", []):
            result.append({
                "name": subdir["name"],
                "path": subdir["path"],
                "child_count": (
                    len(subdir.get("contents", {}).get("files", []))
                    + len(subdir.get("contents", {}).get("subdirectories", []))
                ),
            })
            result.extend(
                MobiusMCPTraversal._flatten_directory_tree(subdir.get("contents", {}))
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

        Uses the *working* context (which may include lens terms from
        prior inversion passes), but the original query is preserved
        immutably for true re-evaluation in Phase 3.
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

        # Record surface snapshot for closure detection
        current_surface = {path for path, _ in self.discovered_nodes}
        self._surface_snapshots.append(current_surface)

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
    # PHASE 3: MOBIUS INVERSION — TRUE INVERSION
    # ═══════════════════════════════════════════════════════════════
    #
    # The v1 approach appended discovered keywords to the context,
    # making it grow monotonically. This is *accumulation*, not
    # *inversion*.
    #
    # True Mobius inversion:
    #   1. The original query is preserved immutably.
    #   2. Discovered content produces a LENS — a set of focal terms
    #      that reweight the original query's attention, not replace it.
    #   3. The re-evaluation asks: "Given what I now know exists in
    #      this file system, which parts of my ORIGINAL question
    #      become more important?"
    #   4. Surface closure: if the discovered node set is unchanged
    #      between passes, the surface is closed — traversal is done.

    def phase_3_mobius_inversion(
        self,
        discovered_nodes: List[Tuple[str, Dict[str, Any]]],
    ) -> List[Tuple[str, Dict[str, Any]]]:
        """
        THE CRITICAL MOBIUS OPERATION:
        Discovered content transforms *how the query is read*,
        not the query itself.
        """
        original_keywords = self.semantic.extract_keywords(self.original_context)
        original_entities = self.semantic.extract_entities(self.original_context)

        # Record initial context state
        self._context_history.append({
            "depth": self.traversal_depth,
            "phase": "initial",
            "keywords": len(original_keywords),
            "entities": len(original_entities),
        })

        # Extract the LENS: what the file system teaches us about
        # the original query
        lens_keywords: Set[str] = set()
        lens_entities: Set[str] = set()
        new_connections: List[Dict[str, str]] = []

        for _path, data in discovered_nodes:
            preview = data.get("preview", "")
            file_kw = self.semantic.extract_keywords(preview)
            file_ent = data.get("entities", set())

            # Only keep terms that BRIDGE original context to new content.
            # A lens term must appear in the file AND relate to the
            # original query (share at least one keyword).
            if file_kw & original_keywords:
                # This file is relevant; its novel terms form the lens
                lens_keywords.update(file_kw - original_keywords)
                lens_entities.update(file_ent - original_entities)

        # Also extract lens from directory-as-content
        for dir_path, dir_data in self.directory_nodes:
            profile = dir_data.get("semantic_profile", {})
            dir_tokens = set(profile.get("tokens", []))
            child_tokens = set(profile.get("child_tokens", []))
            if dir_tokens & original_keywords or child_tokens & original_keywords:
                lens_keywords.update(dir_tokens - original_keywords)
                lens_keywords.update(child_tokens - original_keywords)

        # Find unexpected connections: original entities co-occurring
        # with new entities in the same document
        for orig in list(original_entities)[:20]:
            for _path, data in discovered_nodes:
                preview_lower = data.get("preview", "").lower()
                if orig.lower() not in preview_lower:
                    continue
                for new_ent in list(lens_entities)[:50]:
                    if new_ent.lower() in preview_lower:
                        new_connections.append({
                            "original": orig,
                            "discovered": new_ent,
                            "bridge_document": _path,
                        })

        # Measure novelty using lens terms
        novelty = self.semantic.measure_context_expansion(
            original_keywords, original_entities,
            original_keywords | lens_keywords,
            original_entities | lens_entities,
        )

        # Surface closure check: has the discovered set stabilized?
        surface_stable = self._check_surface_closure()

        logger.info(
            "Mobius Inversion depth %d: novelty=%.1f%%, lens_keywords=%d, "
            "lens_entities=%d, connections=%d, surface_closed=%s",
            self.traversal_depth,
            novelty * 100,
            len(lens_keywords),
            len(lens_entities),
            len(new_connections),
            surface_stable,
        )

        self._context_history.append({
            "depth": self.traversal_depth,
            "phase": "inversion",
            "novelty_score": novelty,
            "lens_keywords": len(lens_keywords),
            "lens_entities": len(lens_entities),
            "new_connections": len(new_connections),
            "sample_lens_entities": sorted(lens_entities)[:10],
            "surface_closed": surface_stable,
            "connections": new_connections[:20],
        })

        # Decision: recurse or converge
        if surface_stable:
            logger.info(
                "Surface CLOSED at depth %d — discovered node set is stable",
                self.traversal_depth,
            )
            self._surface_closed = True
            return self.discovered_nodes

        if novelty > self.novelty_threshold:
            self.traversal_depth += 1
            if self.traversal_depth < self.max_recursion:
                logger.info(
                    "Mobius Inversion: building lens (%.1f%% novelty), "
                    "re-evaluating at depth %d",
                    novelty * 100,
                    self.traversal_depth,
                )
                # Build the LENS-augmented context: original query
                # PLUS the most relevant bridging terms
                top_lens = sorted(lens_keywords, key=lambda k: (
                    sum(1 for p, d in discovered_nodes
                        if k in d.get("preview", "").lower())
                ), reverse=True)[:30]

                # The lens is a re-weighting, not an expansion.
                # We prepend focal terms so they influence scoring
                # but the original query remains the anchor.
                self.context = (
                    " ".join(top_lens) + "\n" + self.original_context
                )
                # Re-run Phase 2 with the lens-augmented context
                return self.phase_2_semantic_extraction(self.topology_map)
            else:
                logger.info(
                    "Maximum recursion depth reached (%d)",
                    self.max_recursion,
                )
        else:
            logger.info(
                "Convergence achieved at depth %d (novelty %.1f%% <= threshold %.1f%%)",
                self.traversal_depth,
                novelty * 100,
                self.novelty_threshold * 100,
            )

        return self.discovered_nodes

    def _check_surface_closure(self) -> bool:
        """
        The surface is closed when the set of discovered node paths
        is identical between the last two passes. This means the
        traversal has returned to its starting point — the Mobius
        property is satisfied.
        """
        if len(self._surface_snapshots) < 2:
            return False
        return self._surface_snapshots[-1] == self._surface_snapshots[-2]

    # ═══════════════════════════════════════════════════════════════
    # PHASE 4: DEPENDENCY GRAPH CONSTRUCTION
    # ═══════════════════════════════════════════════════════════════

    def phase_4_dependency_graph(
        self,
        discovered_nodes: List[Tuple[str, Dict[str, Any]]],
    ) -> Dict[str, Any]:
        """
        Build semantic network showing how documents reference each other.
        Directories are included as first-class nodes (container = content).
        """
        graph = DependencyGraph()
        all_references: Set[str] = set()
        node_paths = {path for path, _ in discovered_nodes}

        # Add file nodes
        for path, data in discovered_nodes:
            graph.add_node(
                path,
                node_type="file",
                score=data.get("score", 0),
                entities=list(data.get("entities", set()))[:20],
                file_references=data.get("file_references", set()),
            )

            file_refs = data.get("file_references", set())
            all_references.update(file_refs)

            for ref in file_refs:
                for candidate in node_paths:
                    if candidate == path:
                        continue
                    ref_normalized = ref.replace("\\", "/")
                    cand_normalized = candidate.replace("\\", "/")
                    if (
                        ref_normalized in cand_normalized
                        or cand_normalized.endswith(ref_normalized)
                        or os.path.basename(ref_normalized)
                        == os.path.basename(cand_normalized)
                    ):
                        graph.add_edge(path, candidate)

        # Add directory nodes (container = content)
        for dir_path, dir_data in self.directory_nodes[:10]:
            graph.add_node(
                dir_path,
                node_type="directory",
                score=dir_data.get("relevance_score", 0),
                semantic_sentence=dir_data.get("semantic_profile", {}).get(
                    "semantic_sentence", ""
                ),
            )
            # Connect directories to the files they contain
            for file_path, _ in discovered_nodes:
                if file_path.startswith(dir_path + os.sep):
                    graph.add_edge(dir_path, file_path)

        hub_docs = graph.hub_documents(top_n=5)
        clusters = graph.identify_clusters()
        gaps = graph.identify_continuity_gaps(all_references)
        bridges = graph.map_cluster_bridges(clusters)

        logger.info(
            "Phase 4 complete: %d nodes (%d dirs), %d edges, %d clusters, %d gaps",
            len(graph.nodes),
            len([d for d in self.directory_nodes[:10]]),
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
        Present unified understanding. Includes the new Mobius
        refinement outputs: surface closure status, directory
        semantics, lens terms, and persistent index metadata.
        """
        graph: DependencyGraph = dependency_result["graph"]

        return {
            "traversal_metadata": {
                "depth_achieved": self.traversal_depth,
                "surface_closed": self._surface_closed,
                "convergence_score": self._calculate_convergence(),
                "total_files_scanned": sum(
                    t["file_count"] for t in self.topology_map.values()
                ),
                "total_directories_scanned": sum(
                    t["directory_count"] for t in self.topology_map.values()
                ),
                "relevant_files_found": len(self.discovered_nodes),
                "relevant_directories_found": len(self.directory_nodes),
                "roots_traversed": list(self.topology_map.keys()),
                "original_query_preserved": True,
            },
            "relevant_artifacts": [
                {
                    "path": path,
                    "type": "file",
                    "relevance_score": round(data["score"], 4),
                    "key_passage": data["preview"][:500],
                    "entities": sorted(data.get("entities", set()))[:15],
                    "metadata": data.get("metadata", {}),
                }
                for path, data in self.discovered_nodes[:15]
            ],
            "relevant_directories": [
                {
                    "path": dir_path,
                    "type": "directory",
                    "relevance_score": round(dir_data.get("relevance_score", 0), 4),
                    "semantic_sentence": dir_data.get("semantic_profile", {}).get(
                        "semantic_sentence", ""
                    ),
                    "children": dir_data.get("semantic_profile", {}).get(
                        "child_names", []
                    )[:10],
                }
                for dir_path, dir_data in self.directory_nodes[:10]
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
                "surface_closure": {
                    "closed": self._surface_closed,
                    "passes": len(self._surface_snapshots),
                    "node_set_sizes": [len(s) for s in self._surface_snapshots],
                    "stability": self._surface_stability(),
                },
                "emergent_themes": self._identify_emergent_patterns(),
                "recursive_depth_value": self._assess_depth_contribution(),
                "original_query": self.original_context,
            },
        }

    # ── Synthesis helpers ────────────────────────────────────────────

    def _calculate_convergence(self) -> float:
        """
        Calculate how well the traversal converged.
        1.0 means perfect convergence (surface closed or novelty
        dropped below threshold). Lower values indicate forced
        termination at recursion limit.
        """
        if self._surface_closed:
            return 1.0
        if len(self._context_history) < 2:
            return 1.0
        last = [e for e in self._context_history if "novelty_score" in e]
        if not last:
            return 1.0
        last_novelty = last[-1]["novelty_score"]
        if last_novelty <= self.novelty_threshold:
            return 1.0
        return max(0.0, 1.0 - last_novelty)

    def _surface_stability(self) -> float:
        """
        Measure how stable the discovered surface is across passes.
        Returns the Jaccard similarity between the last two snapshots,
        or 1.0 if only one pass was made.
        """
        if len(self._surface_snapshots) < 2:
            return 1.0
        a = self._surface_snapshots[-2]
        b = self._surface_snapshots[-1]
        if not a and not b:
            return 1.0
        intersection = len(a & b)
        union = len(a | b)
        return intersection / union if union > 0 else 1.0

    def _identify_emergent_patterns(self) -> List[str]:
        """
        Identify themes that appeared through lens construction
        but were not present in the original context.
        """
        if len(self._context_history) < 2:
            return []

        patterns: List[str] = []
        for entry in self._context_history:
            sample = entry.get("sample_lens_entities", [])
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
                    "lens_keywords": entry.get("lens_keywords", 0),
                    "lens_entities": entry.get("lens_entities", 0),
                    "surface_closed": entry.get("surface_closed", False),
                })
        return {
            "total_depth": self.traversal_depth,
            "contributions": contributions,
        }

    def _generate_follow_up_vectors(self) -> List[str]:
        """
        Generate suggested follow-up queries based on discovered
        entities, directory semantics, and continuity gaps.
        """
        vectors: List[str] = []

        # From emergent entities
        patterns = self._identify_emergent_patterns()
        for entity in patterns[:5]:
            vectors.append(f"Explore connections to: {entity}")

        # From directory-as-content insights
        for dir_path, dir_data in self.directory_nodes[:3]:
            profile = dir_data.get("semantic_profile", {})
            sentence = profile.get("semantic_sentence", "")
            if sentence:
                vectors.append(f"Investigate directory surface: {sentence}")

        # From discovered but low-scoring files
        if len(self.discovered_nodes) > 5:
            tail = self.discovered_nodes[5:]
            for path, data in tail[:3]:
                name = os.path.basename(path)
                vectors.append(f"Deep-dive into: {name} (score: {data['score']:.2f})")

        return vectors

    # ═══════════════════════════════════════════════════════════════
    # PERSISTENT INDEX — CLAUDE AS INDEXER, NOT HOLDER
    # ═══════════════════════════════════════════════════════════════
    #
    # The constraint: finite context window.
    # The transmutation: Claude becomes an indexer.
    # Each invocation maps structure. Each recursion tightens the
    # surface. The index persists across invocations, accumulating
    # structural awareness without holding content in memory.

    def _load_index(self, path: str) -> None:
        """Load persistent index from a previous traversal."""
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            self._index = data
            logger.info(
                "Loaded persistent index: %d entries from %s",
                len(data.get("file_signatures", {})),
                path,
            )
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("Could not load index from %s: %s", path, exc)
            self._index = {}

    def _save_index(self, path: str) -> None:
        """
        Save persistent index. Stores:
          - File path -> content hash (detect changes between runs)
          - File path -> relevance score (accumulated knowledge)
          - Directory semantic profiles
          - Surface closure history
        """
        file_sigs: Dict[str, str] = {}
        file_scores: Dict[str, float] = {}
        for fpath, data in self.discovered_nodes:
            preview = data.get("preview", "")
            file_sigs[fpath] = hashlib.sha256(preview.encode()).hexdigest()[:16]
            file_scores[fpath] = data.get("score", 0)

        dir_profiles: Dict[str, Dict[str, Any]] = {}
        for dir_path, dir_data in self.directory_nodes:
            profile = dir_data.get("semantic_profile", {})
            dir_profiles[dir_path] = {
                "name": profile.get("name", ""),
                "tokens": profile.get("tokens", []),
                "semantic_sentence": profile.get("semantic_sentence", ""),
                "relevance_score": dir_data.get("relevance_score", 0),
            }

        # Merge with existing index (accumulate, don't replace)
        existing_sigs = self._index.get("file_signatures", {})
        existing_scores = self._index.get("file_scores", {})
        existing_dirs = self._index.get("directory_profiles", {})

        existing_sigs.update(file_sigs)
        existing_scores.update(file_scores)
        existing_dirs.update(dir_profiles)

        index_data = {
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "traversal_count": self._index.get("traversal_count", 0) + 1,
            "original_query": self.original_context,
            "roots": self.roots,
            "file_signatures": existing_sigs,
            "file_scores": existing_scores,
            "directory_profiles": existing_dirs,
            "surface_closure_history": [
                sorted(s) for s in self._surface_snapshots
            ],
        }

        try:
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(index_data, fh, indent=2)
            logger.info("Saved persistent index to %s (%d files, %d dirs)",
                        path, len(existing_sigs), len(existing_dirs))
        except OSError as exc:
            logger.warning("Could not save index to %s: %s", path, exc)

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

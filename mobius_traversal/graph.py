"""
Dependency graph construction for the Mobius traversal protocol.

Builds and analyzes inter-document reference networks without requiring
external graph libraries. Identifies hub documents, semantic clusters,
and continuity gaps (referenced but missing files).
"""

from collections import defaultdict, deque
from typing import Dict, List, Set, Tuple, Any, Optional


class DependencyGraph:
    """
    Directed graph of inter-document references with analysis
    capabilities for hub detection, clustering, and gap identification.
    """

    def __init__(self):
        self._adjacency: Dict[str, Set[str]] = defaultdict(set)
        self._reverse: Dict[str, Set[str]] = defaultdict(set)
        self._node_data: Dict[str, Dict[str, Any]] = {}

    @property
    def nodes(self) -> Set[str]:
        return set(self._node_data.keys())

    @property
    def edge_count(self) -> int:
        return sum(len(targets) for targets in self._adjacency.values())

    def add_node(self, path: str, **data: Any) -> None:
        """Add a node (document) with associated metadata."""
        self._node_data[path] = data

    def add_edge(self, source: str, target: str) -> None:
        """Add a directed edge (reference) from source to target."""
        self._adjacency[source].add(target)
        self._reverse[target].add(source)

    def get_node_data(self, path: str) -> Dict[str, Any]:
        return self._node_data.get(path, {})

    def neighbors(self, path: str) -> Set[str]:
        return self._adjacency.get(path, set())

    def predecessors(self, path: str) -> Set[str]:
        return self._reverse.get(path, set())

    def degree(self, path: str) -> int:
        """Total degree (in + out)."""
        return len(self._adjacency.get(path, set())) + len(
            self._reverse.get(path, set())
        )

    # ── Hub Detection ────────────────────────────────────────────────

    def betweenness_centrality(self) -> Dict[str, float]:
        """
        Approximate betweenness centrality using BFS from each node.
        For each node s, compute shortest paths through all other nodes
        and accumulate centrality scores.
        """
        centrality: Dict[str, float] = {n: 0.0 for n in self._node_data}
        nodes = list(self._node_data.keys())

        for source in nodes:
            # BFS from source
            stack: List[str] = []
            predecessors: Dict[str, List[str]] = {n: [] for n in nodes}
            sigma: Dict[str, int] = {n: 0 for n in nodes}
            sigma[source] = 1
            dist: Dict[str, int] = {n: -1 for n in nodes}
            dist[source] = 0
            queue: deque = deque([source])

            while queue:
                v = queue.popleft()
                stack.append(v)
                # Traverse both directions for undirected centrality
                all_neighbors = self._adjacency.get(v, set()) | self._reverse.get(
                    v, set()
                )
                for w in all_neighbors:
                    if w not in dist or dist[w] < 0:
                        dist[w] = dist[v] + 1
                        queue.append(w)
                    if dist[w] == dist[v] + 1:
                        sigma[w] += sigma[v]
                        predecessors[w].append(v)

            # Back-propagation
            delta: Dict[str, float] = {n: 0.0 for n in nodes}
            while stack:
                w = stack.pop()
                for v in predecessors[w]:
                    if sigma[w] > 0:
                        delta[v] += (sigma[v] / sigma[w]) * (1.0 + delta[w])
                if w != source:
                    centrality[w] += delta[w]

        # Normalize
        n = len(nodes)
        if n > 2:
            norm = 1.0 / ((n - 1) * (n - 2))
            centrality = {k: v * norm for k, v in centrality.items()}

        return centrality

    def hub_documents(self, top_n: int = 5) -> List[Tuple[str, float]]:
        """Return the top-N documents by betweenness centrality."""
        centrality = self.betweenness_centrality()
        ranked = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_n]

    # ── Clustering ───────────────────────────────────────────────────

    def identify_clusters(self) -> List[Dict[str, Any]]:
        """
        Find connected components in the undirected view of the graph
        as semantic clusters.
        """
        visited: Set[str] = set()
        clusters: List[Dict[str, Any]] = []

        for node in self._node_data:
            if node in visited:
                continue

            # BFS to find component
            component: List[str] = []
            queue: deque = deque([node])
            while queue:
                current = queue.popleft()
                if current in visited:
                    continue
                visited.add(current)
                component.append(current)
                neighbors = self._adjacency.get(current, set()) | self._reverse.get(
                    current, set()
                )
                for neighbor in neighbors:
                    if neighbor not in visited and neighbor in self._node_data:
                        queue.append(neighbor)

            if component:
                clusters.append(
                    {
                        "cluster_id": len(clusters),
                        "documents": component,
                        "size": len(component),
                        "internal_edges": self._count_internal_edges(set(component)),
                    }
                )

        return clusters

    def _count_internal_edges(self, component: Set[str]) -> int:
        count = 0
        for node in component:
            for target in self._adjacency.get(node, set()):
                if target in component:
                    count += 1
        return count

    # ── Gap Detection ────────────────────────────────────────────────

    def identify_continuity_gaps(
        self, all_references: Set[str]
    ) -> List[Dict[str, Any]]:
        """
        Detect references that point to files not present in the graph.
        Returns a list of missing references with the nodes that reference them.
        """
        existing = set(self._node_data.keys())
        missing = all_references - existing
        gaps: List[Dict[str, Any]] = []

        for ref in missing:
            referenced_by = []
            for node in existing:
                node_data = self._node_data.get(node, {})
                file_refs = node_data.get("file_references", set())
                if ref in file_refs:
                    referenced_by.append(node)

            gaps.append(
                {
                    "missing_reference": ref,
                    "referenced_by": referenced_by,
                    "suggested_search": _generate_search_vector(ref),
                }
            )

        return gaps

    # ── Serialization ────────────────────────────────────────────────

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the graph to a JSON-compatible dictionary."""
        edges = []
        for source, targets in self._adjacency.items():
            for target in targets:
                edges.append({"source": source, "target": target})

        return {
            "nodes": [
                {"path": p, "degree": self.degree(p)}
                for p in self._node_data
            ],
            "edges": edges,
            "node_count": len(self._node_data),
            "edge_count": self.edge_count,
        }

    # ── Inter-cluster bridge detection ───────────────────────────────

    def map_cluster_bridges(
        self, clusters: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Find edges that connect nodes in different clusters.
        """
        node_to_cluster: Dict[str, int] = {}
        for cluster in clusters:
            for doc in cluster["documents"]:
                node_to_cluster[doc] = cluster["cluster_id"]

        bridges: List[Dict[str, Any]] = []
        seen: Set[Tuple[int, int]] = set()

        for source, targets in self._adjacency.items():
            src_cluster = node_to_cluster.get(source)
            if src_cluster is None:
                continue
            for target in targets:
                tgt_cluster = node_to_cluster.get(target)
                if tgt_cluster is None or tgt_cluster == src_cluster:
                    continue
                pair = (min(src_cluster, tgt_cluster), max(src_cluster, tgt_cluster))
                if pair not in seen:
                    seen.add(pair)
                    bridges.append(
                        {
                            "from_cluster": pair[0],
                            "to_cluster": pair[1],
                            "bridge_edge": {"source": source, "target": target},
                        }
                    )

        return bridges


def _generate_search_vector(reference: str) -> str:
    """Generate a search suggestion for a missing reference."""
    # Strip path prefixes and extensions for a generic search term
    import os

    name = os.path.splitext(os.path.basename(reference))[0]
    return f"Search for files matching: *{name}*"

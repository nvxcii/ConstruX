"""
Semantic analysis utilities for the Mobius traversal protocol.

Provides keyword extraction, entity recognition, directory-as-content
analysis, and multi-dimensional relevance scoring. The core insight:
directories are not containers -- they are semantic content. A path
like ``intelligence/evidence_database.py`` carries meaning independent
of the file it names; the nesting *is* a sentence.
"""

import os
import re
import math
from collections import Counter
from datetime import datetime, timezone
from typing import Any, Set, Dict, Optional, List, Tuple


# Common English stop words for keyword filtering
STOP_WORDS = frozenset({
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "shall",
    "should", "may", "might", "must", "can", "could", "am", "it", "its",
    "this", "that", "these", "those", "i", "me", "my", "we", "our", "you",
    "your", "he", "him", "his", "she", "her", "they", "them", "their",
    "what", "which", "who", "whom", "where", "when", "why", "how",
    "all", "each", "every", "both", "few", "more", "most", "other",
    "some", "such", "no", "not", "only", "same", "so", "than", "too",
    "very", "just", "because", "as", "until", "while", "of", "at", "by",
    "for", "with", "about", "against", "between", "through", "during",
    "before", "after", "above", "below", "to", "from", "up", "down",
    "in", "out", "on", "off", "over", "under", "again", "further",
    "then", "once", "here", "there", "and", "but", "or", "nor", "if",
    "else", "def", "class", "return", "import", "from", "none", "true",
    "false", "self", "try", "except", "finally", "raise", "pass",
})

# Patterns for entity extraction
_CAMEL_CASE = re.compile(r"[A-Z][a-z]+(?:[A-Z][a-z]+)+")
_UPPER_ACRONYM = re.compile(r"\b[A-Z]{2,6}\b")
_FILE_REFERENCE = re.compile(
    r"[\w./\\-]+\.(?:py|js|ts|json|yaml|yml|md|txt|html|css|sql|sh|toml|cfg|ini)"
)
_URL_PATTERN = re.compile(r"https?://[^\s<>\"']+")
_IMPORT_PATTERN = re.compile(r"(?:from|import)\s+([\w.]+)")
_QUOTED_STRING = re.compile(r"[\"']([^\"']{3,60})[\"']")


class SemanticAnalyzer:
    """Multi-dimensional semantic analysis for file content."""

    def __init__(self):
        self._idf_cache: Dict[str, float] = {}
        self._corpus_size = 0

    def extract_keywords(self, text: str, max_keywords: int = 100) -> Set[str]:
        """
        Extract meaningful keywords from text by tokenizing, lowercasing,
        removing stop words, and filtering short tokens.
        """
        tokens = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]{2,}", text.lower())
        filtered = [t for t in tokens if t not in STOP_WORDS and len(t) > 2]
        counts = Counter(filtered)
        return set(kw for kw, _ in counts.most_common(max_keywords))

    def extract_entities(self, text: str) -> Set[str]:
        """
        Extract named entities: CamelCase identifiers, acronyms,
        file references, imports, and quoted strings.
        """
        entities: Set[str] = set()

        # CamelCase identifiers (class names, etc.)
        entities.update(_CAMEL_CASE.findall(text))

        # Uppercase acronyms (API, OSHA, ADA, etc.)
        entities.update(_UPPER_ACRONYM.findall(text))

        # File references
        entities.update(_FILE_REFERENCE.findall(text))

        # Python import paths
        for match in _IMPORT_PATTERN.finditer(text):
            entities.add(match.group(1))

        # Quoted strings (names, descriptions, identifiers)
        for match in _QUOTED_STRING.finditer(text):
            candidate = match.group(1).strip()
            if (
                not candidate.startswith(("http", "/", ".", "#", "(", ")", "{"))
                and "\n" not in candidate
                and not candidate.endswith(("(", ")", "{", "}", "[", "]", ","))
                and candidate.count(" ") < 8
            ):
                entities.add(candidate)

        return entities

    def extract_file_references(self, text: str) -> Set[str]:
        """Extract paths and file references from text content."""
        refs: Set[str] = set()
        refs.update(_FILE_REFERENCE.findall(text))
        refs.update(_URL_PATTERN.findall(text))
        for match in _IMPORT_PATTERN.finditer(text):
            module = match.group(1)
            refs.add(module.replace(".", "/") + ".py")
        return refs

    def calculate_semantic_overlap(
        self,
        context: str,
        file_content: str,
        file_path: str,
        modification_time: Optional[float] = None,
    ) -> float:
        """
        Multi-dimensional relevance scoring combining:
          1. Keyword intersection (30%)
          2. Entity overlap (30%)
          3. Temporal proximity / recency (20%)
          4. Path semantic analysis (20%)
        """
        score = 0.0

        # 1. Keyword intersection
        context_kw = self.extract_keywords(context)
        file_kw = self.extract_keywords(file_content)
        if context_kw:
            kw_overlap = len(context_kw & file_kw) / len(context_kw)
            score += kw_overlap * 0.3

        # 2. Entity overlap
        context_ent = self.extract_entities(context)
        file_ent = self.extract_entities(file_content)
        if context_ent:
            ent_overlap = len(context_ent & file_ent) / len(context_ent)
            score += ent_overlap * 0.3

        # 3. Temporal proximity
        if modification_time is not None:
            recency = self._calculate_recency(modification_time)
            score += recency * 0.2

        # 4. Path semantic analysis
        path_score = self._path_semantic_analysis(file_path, context)
        score += path_score * 0.2

        return min(score, 1.0)

    def measure_context_expansion(
        self,
        original_keywords: Set[str],
        original_entities: Set[str],
        expanded_keywords: Set[str],
        expanded_entities: Set[str],
    ) -> float:
        """
        Measure how much new information was discovered relative to
        the original context. Returns a novelty score in [0, 1].
        """
        new_keywords = expanded_keywords - original_keywords
        new_entities = expanded_entities - original_entities

        kw_novelty = len(new_keywords) / max(len(original_keywords), 1)
        ent_novelty = len(new_entities) / max(len(original_entities), 1)

        # Weighted combination, clamped
        return min((kw_novelty * 0.4 + ent_novelty * 0.6), 1.0)

    def build_tf_idf(
        self, documents: List[Tuple[str, str]]
    ) -> Dict[str, Dict[str, float]]:
        """
        Build TF-IDF vectors for a list of (path, content) documents.
        Returns {path: {term: tf_idf_score}}.
        """
        self._corpus_size = len(documents)
        doc_freq: Counter = Counter()
        doc_terms: Dict[str, Counter] = {}

        for path, content in documents:
            terms = list(re.findall(r"[a-zA-Z_][a-zA-Z0-9_]{2,}", content.lower()))
            terms = [t for t in terms if t not in STOP_WORDS]
            tf = Counter(terms)
            doc_terms[path] = tf
            for term in set(terms):
                doc_freq[term] += 1

        result: Dict[str, Dict[str, float]] = {}
        for path, tf in doc_terms.items():
            total = sum(tf.values()) or 1
            tfidf: Dict[str, float] = {}
            for term, count in tf.items():
                tf_val = count / total
                idf_val = math.log(self._corpus_size / (1 + doc_freq[term]))
                tfidf[term] = tf_val * idf_val
            result[path] = tfidf

        return result

    def cosine_similarity(
        self, vec_a: Dict[str, float], vec_b: Dict[str, float]
    ) -> float:
        """Cosine similarity between two sparse term vectors."""
        all_terms = set(vec_a) | set(vec_b)
        dot = sum(vec_a.get(t, 0) * vec_b.get(t, 0) for t in all_terms)
        mag_a = math.sqrt(sum(v ** 2 for v in vec_a.values())) or 1e-10
        mag_b = math.sqrt(sum(v ** 2 for v in vec_b.values())) or 1e-10
        return dot / (mag_a * mag_b)

    # ── Directory-as-Content analysis ────────────────────────────────

    def analyze_directory_semantics(self, dir_path: str) -> Dict[str, Any]:
        """
        Treat a directory as a semantic entity, not a container.

        A directory's meaning is encoded in:
          - Its name (the primary semantic signal)
          - Its depth / position in the hierarchy (scope)
          - Its siblings (what it's grouped with = category)
          - Its children (what it contains = definition)
          - Its parent (what subsumes it = context)

        Returns a semantic profile for the directory as content.
        """
        name = os.path.basename(dir_path)
        parent = os.path.basename(os.path.dirname(dir_path))

        # Decompose directory name into semantic tokens
        # Handle snake_case, kebab-case, CamelCase, dot.notation
        tokens = self._decompose_name(name)

        # Sibling directories = semantic category peers
        siblings: List[str] = []
        parent_dir = os.path.dirname(dir_path)
        if os.path.isdir(parent_dir):
            try:
                siblings = [
                    e for e in os.listdir(parent_dir)
                    if os.path.isdir(os.path.join(parent_dir, e))
                    and e != name
                    and not e.startswith(".")
                ]
            except OSError:
                pass

        # Child entries = the directory's "definition"
        children: List[str] = []
        try:
            children = [e for e in os.listdir(dir_path) if not e.startswith(".")]
        except OSError:
            pass

        child_tokens: Set[str] = set()
        for child in children:
            child_tokens.update(self._decompose_name(child))

        return {
            "path": dir_path,
            "name": name,
            "tokens": tokens,
            "parent_name": parent,
            "sibling_names": siblings,
            "child_names": children,
            "child_tokens": child_tokens,
            "depth": dir_path.count(os.sep),
            # The "sentence" this directory speaks:
            # parent > name > [children]
            "semantic_sentence": f"{parent}/{name} containing [{', '.join(children[:10])}]",
        }

    def score_directory_relevance(
        self, dir_semantics: Dict[str, Any], context: str
    ) -> float:
        """
        Score a directory's relevance to the conversation context.
        The directory IS content; its structure IS meaning.
        """
        context_kw = self.extract_keywords(context)
        if not context_kw:
            return 0.0

        score = 0.0

        # Directory name tokens vs context (40% -- strongest signal)
        dir_tokens = set(t.lower() for t in dir_semantics["tokens"])
        name_overlap = len(dir_tokens & context_kw) / max(len(dir_tokens), 1)
        score += name_overlap * 0.4

        # Child tokens vs context (30% -- what it contains defines it)
        child_tokens = set(t.lower() for t in dir_semantics["child_tokens"])
        if child_tokens:
            child_overlap = len(child_tokens & context_kw) / max(len(child_tokens), 1)
            score += child_overlap * 0.3

        # Sibling names vs context (20% -- categorical peers)
        sibling_tokens: Set[str] = set()
        for sib in dir_semantics["sibling_names"]:
            sibling_tokens.update(t.lower() for t in self._decompose_name(sib))
        if sibling_tokens:
            sib_overlap = len(sibling_tokens & context_kw) / max(len(sibling_tokens), 1)
            score += sib_overlap * 0.2

        # Semantic sentence match (10% -- full path context)
        sentence = dir_semantics["semantic_sentence"].lower()
        sentence_matches = sum(1 for kw in context_kw if kw in sentence)
        score += min(sentence_matches / max(len(context_kw), 1), 1.0) * 0.1

        return min(score, 1.0)

    @staticmethod
    def _decompose_name(name: str) -> List[str]:
        """
        Break a file/directory name into semantic tokens.
        Handles: snake_case, kebab-case, CamelCase, dot.notation.
        Strips extensions.
        """
        # Remove extension
        name = os.path.splitext(name)[0]
        # Split on separators
        parts = re.split(r"[_\-./\\]+", name)
        # Further split CamelCase
        expanded: List[str] = []
        for part in parts:
            camel_parts = re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|\d|\b)", part)
            if camel_parts:
                expanded.extend(camel_parts)
            elif part:
                expanded.append(part)
        return [t.lower() for t in expanded if len(t) > 1]

    # ── private helpers ──────────────────────────────────────────────

    @staticmethod
    def _calculate_recency(modification_time: float) -> float:
        """
        Score [0,1] based on how recently a file was modified.
        Files modified within the last day score 1.0, decaying
        logarithmically over 365 days.
        """
        now = datetime.now(timezone.utc).timestamp()
        age_days = (now - modification_time) / 86400
        if age_days <= 0:
            return 1.0
        if age_days > 365:
            return 0.0
        return max(0.0, 1.0 - math.log1p(age_days) / math.log1p(365))

    @staticmethod
    def _path_semantic_analysis(file_path: str, context: str) -> float:
        """
        Score [0,1] based on how many path segments appear as
        keywords in the context.
        """
        segments = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]{2,}", file_path.lower())
        if not segments:
            return 0.0
        context_lower = context.lower()
        matches = sum(1 for seg in segments if seg in context_lower)
        return min(matches / len(segments), 1.0)

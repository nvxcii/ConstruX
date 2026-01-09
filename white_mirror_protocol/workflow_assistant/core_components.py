"""
AI Dynamic Workflow Assistant
Analyzes files, recognizes patterns, and suggests deployments with adaptive learning
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import os
import time
import json
import hashlib

# Will integrate with Multi-AI Framework
try:
    from multi_ai_framework.core.ai_coordinator import AIJusticeLeague
    MULTI_AI_AVAILABLE = True
except ImportError:
    MULTI_AI_AVAILABLE = False

# Will integrate with White Mirror Protocol for meta-learning
try:
    from white_mirror_protocol import WhiteMirrorProtocol
    WHITE_MIRROR_AVAILABLE = True
except ImportError:
    WHITE_MIRROR_AVAILABLE = False


@dataclass
class FileAnalysis:
    """Result of analyzing a single file"""
    file_path: str
    file_type: str
    language: Optional[str]
    purpose: str
    key_points: List[str]
    dependencies: List[str]
    deployment_readiness: float  # 0-1
    suggestions: List[str]
    metadata: Dict[str, Any]
    timestamp: float


@dataclass
class WorkflowPattern:
    """Identified workflow pattern"""
    pattern_id: str
    pattern_type: str  # 'deployment', 'testing', 'integration', etc.
    files_involved: List[str]
    sequence: List[str]  # Ordered steps
    confidence: float
    occurrences: int
    last_seen: float
    effectiveness: float  # Learned over time


@dataclass
class DeploymentSuggestion:
    """Suggested deployment strategy"""
    strategy_name: str
    description: str
    steps: List[Dict[str, Any]]
    prerequisites: List[str]
    estimated_time: str
    confidence: float
    risks: List[str]
    benefits: List[str]


class FileAnalyzer:
    """
    Analyzes files using AI to extract purpose, key points, and insights
    """

    def __init__(self, ai_league: Optional[Any] = None):
        self.ai_league = ai_league
        self.analysis_cache: Dict[str, FileAnalysis] = {}

    def analyze_file(self, file_path: str) -> FileAnalysis:
        """Analyze a single file"""

        # Check cache first
        file_hash = self._get_file_hash(file_path)
        if file_hash in self.analysis_cache:
            return self.analysis_cache[file_hash]

        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return self._create_error_analysis(file_path, str(e))

        # Detect file type
        file_type, language = self._detect_file_type(file_path, content)

        # Analyze with AI if available
        if self.ai_league and MULTI_AI_AVAILABLE:
            analysis = self._ai_analyze(file_path, content, file_type, language)
        else:
            analysis = self._heuristic_analyze(file_path, content, file_type, language)

        # Cache the analysis
        self.analysis_cache[file_hash] = analysis

        return analysis

    def _ai_analyze(self, file_path: str, content: str,
                    file_type: str, language: Optional[str]) -> FileAnalysis:
        """Analyze file using Multi-AI Framework"""

        # Use Claude for comprehensive analysis
        prompt = f"""
        Analyze this {file_type} file and provide:

        1. Primary purpose (1-2 sentences)
        2. Key points (3-5 bullet points)
        3. Dependencies (libraries, frameworks, other files)
        4. Deployment readiness (0-100%)
        5. Suggestions for improvement

        File: {file_path}
        Language: {language or 'Unknown'}

        Content:
        ```
        {content[:2000]}  # First 2000 chars
        ```

        Respond in JSON format.
        """

        # Distribute to AI models
        try:
            results = self.ai_league.distribute_research({
                'file_path': file_path,
                'analysis_prompt': prompt
            })

            # Extract analysis from Claude's response
            claude_result = results.get('claude')
            if claude_result and claude_result.success:
                return self._parse_ai_response(
                    file_path, claude_result.response.content,
                    file_type, language
                )
        except Exception as e:
            print(f"AI analysis failed: {e}")

        # Fallback to heuristic
        return self._heuristic_analyze(file_path, content, file_type, language)

    def _heuristic_analyze(self, file_path: str, content: str,
                          file_type: str, language: Optional[str]) -> FileAnalysis:
        """Heuristic analysis without AI"""

        key_points = []
        dependencies = []
        suggestions = []

        # Extract based on file type
        if file_type == 'python':
            # Find imports
            for line in content.split('\n'):
                if line.strip().startswith(('import ', 'from ')):
                    dependencies.append(line.strip())

            # Find classes and functions
            if 'class ' in content:
                key_points.append("Contains class definitions")
            if 'def ' in content:
                key_points.append("Contains function definitions")

            # Check for documentation
            if '"""' in content or "'''" in content:
                key_points.append("Has documentation strings")
            else:
                suggestions.append("Add documentation strings")

        elif file_type in ['javascript', 'typescript']:
            # Find imports/requires
            for line in content.split('\n'):
                if 'import ' in line or 'require(' in line:
                    dependencies.append(line.strip())

            if 'function' in content or '=>' in content:
                key_points.append("Contains function definitions")
            if 'class ' in content:
                key_points.append("Contains class definitions")

        elif file_type == 'markdown':
            # Count headers
            headers = [line for line in content.split('\n') if line.startswith('#')]
            key_points.append(f"Has {len(headers)} section headers")

            # Check for code blocks
            if '```' in content:
                key_points.append("Contains code examples")

        # Determine deployment readiness
        deployment_readiness = self._assess_deployment_readiness(
            content, file_type, key_points
        )

        # Generate purpose
        purpose = self._infer_purpose(file_path, content, file_type)

        return FileAnalysis(
            file_path=file_path,
            file_type=file_type,
            language=language,
            purpose=purpose,
            key_points=key_points or ["Standard file structure"],
            dependencies=dependencies,
            deployment_readiness=deployment_readiness,
            suggestions=suggestions or ["File appears complete"],
            metadata={'analysis_method': 'heuristic'},
            timestamp=time.time()
        )

    def _detect_file_type(self, file_path: str, content: str) -> Tuple[str, Optional[str]]:
        """Detect file type and language"""
        ext = Path(file_path).suffix.lower()

        type_map = {
            '.py': ('python', 'Python'),
            '.js': ('javascript', 'JavaScript'),
            '.ts': ('typescript', 'TypeScript'),
            '.tsx': ('typescript', 'TypeScript'),
            '.jsx': ('javascript', 'JavaScript'),
            '.md': ('markdown', None),
            '.json': ('json', None),
            '.yaml': ('yaml', None),
            '.yml': ('yaml', None),
            '.sh': ('shell', 'Bash'),
            '.txt': ('text', None),
            '.html': ('html', 'HTML'),
            '.css': ('css', 'CSS'),
            '.go': ('go', 'Go'),
            '.rs': ('rust', 'Rust'),
            '.java': ('java', 'Java'),
        }

        return type_map.get(ext, ('unknown', None))

    def _get_file_hash(self, file_path: str) -> str:
        """Get hash of file for caching"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return hashlib.md5(file_path.encode()).hexdigest()

    def _assess_deployment_readiness(self, content: str, file_type: str,
                                    key_points: List[str]) -> float:
        """Assess how ready a file is for deployment"""
        score = 0.5  # Base score

        # Has documentation
        if any('documentation' in kp.lower() for kp in key_points):
            score += 0.15

        # Has tests (if code)
        if file_type in ['python', 'javascript', 'typescript']:
            if 'test' in content.lower():
                score += 0.15

        # Not too short
        if len(content) > 100:
            score += 0.1

        # Has error handling
        if 'try:' in content or 'catch' in content or 'except' in content:
            score += 0.1

        return min(1.0, score)

    def _infer_purpose(self, file_path: str, content: str, file_type: str) -> str:
        """Infer file purpose from path and content"""
        path = Path(file_path)

        # From path
        if 'test' in path.name.lower():
            return "Testing and validation"
        elif 'config' in path.name.lower():
            return "Configuration file"
        elif 'README' in path.name:
            return "Documentation and project overview"
        elif path.name == '__init__.py':
            return "Package initialization"

        # From content
        if file_type == 'python':
            if 'class' in content and 'def __init__' in content:
                return "Class definition and implementation"
            elif 'def main' in content:
                return "Main executable script"
            elif 'import' in content[:200]:
                return "Module with utilities or functions"

        return f"{file_type.title()} file"

    def _create_error_analysis(self, file_path: str, error: str) -> FileAnalysis:
        """Create analysis for file that couldn't be read"""
        return FileAnalysis(
            file_path=file_path,
            file_type='unknown',
            language=None,
            purpose='Unable to analyze',
            key_points=[f"Error: {error}"],
            dependencies=[],
            deployment_readiness=0.0,
            suggestions=["Fix file access issues"],
            metadata={'error': error},
            timestamp=time.time()
        )

    def _parse_ai_response(self, file_path: str, response: str,
                          file_type: str, language: Optional[str]) -> FileAnalysis:
        """Parse AI response into FileAnalysis"""
        try:
            # Try to extract JSON
            if '{' in response and '}' in response:
                start = response.index('{')
                end = response.rindex('}') + 1
                data = json.loads(response[start:end])

                return FileAnalysis(
                    file_path=file_path,
                    file_type=file_type,
                    language=language,
                    purpose=data.get('purpose', 'AI-analyzed file'),
                    key_points=data.get('key_points', []),
                    dependencies=data.get('dependencies', []),
                    deployment_readiness=data.get('deployment_readiness', 0.5) / 100.0,
                    suggestions=data.get('suggestions', []),
                    metadata={'analysis_method': 'ai', 'model': 'claude'},
                    timestamp=time.time()
                )
        except:
            pass

        # Fallback: use heuristic
        return self._heuristic_analyze(file_path, "", file_type, language)


class WorkflowPatternRecognizer:
    """
    Recognizes patterns in file operations and workflows
    """

    def __init__(self):
        self.patterns: Dict[str, WorkflowPattern] = {}
        self.operation_history: List[Dict[str, Any]] = []

    def record_operation(self, operation_type: str, files: List[str],
                        result: Optional[str] = None):
        """Record an operation for pattern learning"""
        self.operation_history.append({
            'type': operation_type,
            'files': files,
            'result': result,
            'timestamp': time.time()
        })

        # Trigger pattern recognition
        if len(self.operation_history) >= 3:
            self._identify_patterns()

    def _identify_patterns(self):
        """Identify patterns from operation history"""
        # Look for repeated sequences
        recent = self.operation_history[-10:]

        # Find file co-occurrence patterns
        file_pairs = {}
        for op in recent:
            files = op['files']
            for i, f1 in enumerate(files):
                for f2 in files[i+1:]:
                    pair = tuple(sorted([f1, f2]))
                    file_pairs[pair] = file_pairs.get(pair, 0) + 1

        # Create patterns from frequent pairs
        for pair, count in file_pairs.items():
            if count >= 2:
                pattern_id = hashlib.md5(str(pair).encode()).hexdigest()[:12]

                if pattern_id in self.patterns:
                    pattern = self.patterns[pattern_id]
                    pattern.occurrences += 1
                    pattern.last_seen = time.time()
                    pattern.confidence = min(1.0, pattern.occurrences / 10.0)
                else:
                    self.patterns[pattern_id] = WorkflowPattern(
                        pattern_id=pattern_id,
                        pattern_type='file_collaboration',
                        files_involved=list(pair),
                        sequence=['analyze', 'compare', 'integrate'],
                        confidence=0.3,
                        occurrences=1,
                        last_seen=time.time(),
                        effectiveness=0.7
                    )

    def get_patterns_for_files(self, files: List[str]) -> List[WorkflowPattern]:
        """Get relevant patterns for given files"""
        relevant = []

        for pattern in self.patterns.values():
            # Check if any pattern files overlap with input files
            overlap = set(pattern.files_involved) & set(files)
            if overlap:
                relevant.append(pattern)

        # Sort by confidence
        return sorted(relevant, key=lambda p: p.confidence, reverse=True)

    def learn_from_feedback(self, pattern_id: str, effectiveness: float):
        """Update pattern effectiveness from user feedback"""
        if pattern_id in self.patterns:
            pattern = self.patterns[pattern_id]
            # Moving average
            pattern.effectiveness = (pattern.effectiveness * 0.7) + (effectiveness * 0.3)


class DeploymentSuggester:
    """
    Suggests deployment strategies based on file analysis
    """

    def __init__(self):
        self.suggestion_history: List[DeploymentSuggestion] = []

    def suggest_deployment(self, analyses: List[FileAnalysis],
                          patterns: List[WorkflowPattern]) -> List[DeploymentSuggestion]:
        """Generate deployment suggestions based on analyses and patterns"""
        suggestions = []

        # Determine overall project type
        file_types = [a.file_type for a in analyses]

        # Python project
        if 'python' in file_types:
            suggestions.append(self._suggest_python_deployment(analyses))

        # Web project
        if any(ft in file_types for ft in ['javascript', 'typescript', 'html']):
            suggestions.append(self._suggest_web_deployment(analyses))

        # Documentation
        if 'markdown' in file_types:
            suggestions.append(self._suggest_docs_deployment(analyses))

        # API project
        if any('api' in a.file_path.lower() for a in analyses):
            suggestions.append(self._suggest_api_deployment(analyses))

        return [s for s in suggestions if s is not None]

    def _suggest_python_deployment(self, analyses: List[FileAnalysis]) -> DeploymentSuggestion:
        """Suggest Python project deployment"""

        # Check readiness
        avg_readiness = sum(a.deployment_readiness for a in analyses) / len(analyses)

        steps = [
            {'step': 1, 'action': 'Install dependencies', 'command': 'pip install -r requirements.txt'},
            {'step': 2, 'action': 'Run tests', 'command': 'pytest tests/'},
            {'step': 3, 'action': 'Build package', 'command': 'python setup.py sdist bdist_wheel'},
            {'step': 4, 'action': 'Deploy to PyPI', 'command': 'twine upload dist/*'}
        ]

        return DeploymentSuggestion(
            strategy_name="Python Package Deployment",
            description="Standard Python package deployment workflow",
            steps=steps,
            prerequisites=['requirements.txt', 'setup.py', 'tests passing'],
            estimated_time="15-30 minutes",
            confidence=avg_readiness,
            risks=["Breaking changes in dependencies", "Test failures in production environment"],
            benefits=["Easy installation via pip", "Version management", "Distribution"]
        )

    def _suggest_web_deployment(self, analyses: List[FileAnalysis]) -> DeploymentSuggestion:
        """Suggest web project deployment"""

        return DeploymentSuggestion(
            strategy_name="Vercel/Netlify Deployment",
            description="Deploy web application to serverless platform",
            steps=[
                {'step': 1, 'action': 'Build project', 'command': 'npm run build'},
                {'step': 2, 'action': 'Test build', 'command': 'npm test'},
                {'step': 3, 'action': 'Deploy to Vercel', 'command': 'vercel deploy --prod'}
            ],
            prerequisites=['package.json', 'build script', 'tests passing'],
            estimated_time="10-20 minutes",
            confidence=0.8,
            risks=["Environment variables not configured", "Build failures"],
            benefits=["Fast global CDN", "Automatic HTTPS", "Zero downtime deployments"]
        )

    def _suggest_docs_deployment(self, analyses: List[FileAnalysis]) -> Optional[DeploymentSuggestion]:
        """Suggest documentation deployment"""

        return DeploymentSuggestion(
            strategy_name="Documentation Site Deployment",
            description="Deploy documentation to GitHub Pages or similar",
            steps=[
                {'step': 1, 'action': 'Build docs', 'command': 'mkdocs build'},
                {'step': 2, 'action': 'Deploy to GitHub Pages', 'command': 'mkdocs gh-deploy'}
            ],
            prerequisites=['mkdocs.yml or similar', 'Markdown files'],
            estimated_time="5-10 minutes",
            confidence=0.9,
            risks=["Broken links", "Missing assets"],
            benefits=["Free hosting", "Version history", "Easy updates"]
        )

    def _suggest_api_deployment(self, analyses: List[FileAnalysis]) -> DeploymentSuggestion:
        """Suggest API deployment"""

        return DeploymentSuggestion(
            strategy_name="API Deployment (Docker + Cloud)",
            description="Containerize and deploy API to cloud platform",
            steps=[
                {'step': 1, 'action': 'Create Dockerfile', 'command': 'docker build -t api .'},
                {'step': 2, 'action': 'Test container', 'command': 'docker run -p 8000:8000 api'},
                {'step': 3, 'action': 'Push to registry', 'command': 'docker push registry/api'},
                {'step': 4, 'action': 'Deploy to cloud', 'command': 'kubectl apply -f deployment.yaml'}
            ],
            prerequisites=['Dockerfile', 'API tests', 'Cloud account'],
            estimated_time="30-60 minutes",
            confidence=0.75,
            risks=["Container security", "Scaling issues", "Database migrations"],
            benefits=["Consistent environment", "Easy scaling", "Rollback capability"]
        )


def compare_files(analysis1: FileAnalysis, analysis2: FileAnalysis) -> Dict[str, Any]:
    """Compare two file analyses"""

    return {
        'files': [analysis1.file_path, analysis2.file_path],
        'similarity': _calculate_similarity(analysis1, analysis2),
        'common_dependencies': list(set(analysis1.dependencies) & set(analysis2.dependencies)),
        'readiness_difference': abs(analysis1.deployment_readiness - analysis2.deployment_readiness),
        'comparison_summary': _generate_comparison_summary(analysis1, analysis2)
    }


def _calculate_similarity(a1: FileAnalysis, a2: FileAnalysis) -> float:
    """Calculate similarity between two analyses"""
    score = 0.0

    # Same type
    if a1.file_type == a2.file_type:
        score += 0.3

    # Similar dependencies
    if a1.dependencies and a2.dependencies:
        common = set(a1.dependencies) & set(a2.dependencies)
        total = set(a1.dependencies) | set(a2.dependencies)
        score += (len(common) / len(total)) * 0.4 if total else 0

    # Similar readiness
    readiness_sim = 1.0 - abs(a1.deployment_readiness - a2.deployment_readiness)
    score += readiness_sim * 0.3

    return score


def _generate_comparison_summary(a1: FileAnalysis, a2: FileAnalysis) -> str:
    """Generate textual comparison summary"""
    summaries = []

    if a1.file_type == a2.file_type:
        summaries.append(f"Both files are {a1.file_type} files")
    else:
        summaries.append(f"Different types: {a1.file_type} vs {a2.file_type}")

    if a1.deployment_readiness > a2.deployment_readiness:
        summaries.append(f"{Path(a1.file_path).name} is more deployment-ready")
    elif a2.deployment_readiness > a1.deployment_readiness:
        summaries.append(f"{Path(a2.file_path).name} is more deployment-ready")
    else:
        summaries.append("Similar deployment readiness")

    return "; ".join(summaries)

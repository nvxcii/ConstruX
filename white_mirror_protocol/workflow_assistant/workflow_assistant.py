"""
AI Dynamic Workflow Assistant
Main orchestrator with adaptive learning through White Mirror Protocol
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import os
import json
import time

from .core_components import (
    FileAnalyzer,
    WorkflowPatternRecognizer,
    DeploymentSuggester,
    FileAnalysis,
    WorkflowPattern,
    DeploymentSuggestion,
    compare_files
)

# Optional integrations
try:
    from white_mirror_protocol import WhiteMirrorProtocol
    WHITE_MIRROR_AVAILABLE = True
except ImportError:
    WHITE_MIRROR_AVAILABLE = False

try:
    from multi_ai_framework.core.ai_coordinator import AIJusticeLeague
    MULTI_AI_AVAILABLE = True
except ImportError:
    MULTI_AI_AVAILABLE = False


class WorkflowAssistant:
    """
    AI Dynamic Workflow Assistant

    Analyzes files, recognizes patterns, suggests workflows, and learns
    from context over time to become more intuitive.

    Key Features:
    - File analysis with AI
    - Pattern recognition across projects
    - Deployment strategy suggestions
    - Adaptive learning through White Mirror Protocol
    - Context accumulation and improvement
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the workflow assistant

        Args:
            config: Optional configuration with API keys and settings
        """
        self.config = config or {}

        # Initialize AI League if available
        self.ai_league = None
        if MULTI_AI_AVAILABLE and self.config.get('use_ai', False):
            try:
                self.ai_league = AIJusticeLeague(self.config)
            except:
                print("⚠️  Multi-AI Framework not available, using heuristic analysis")

        # Initialize core components
        self.file_analyzer = FileAnalyzer(ai_league=self.ai_league)
        self.pattern_recognizer = WorkflowPatternRecognizer()
        self.deployment_suggester = DeploymentSuggester()

        # Initialize White Mirror Protocol for meta-learning
        self.white_mirror = None
        if WHITE_MIRROR_AVAILABLE and self.config.get('enable_learning', True):
            self.white_mirror = WhiteMirrorProtocol()
            print("🔥 White Mirror Protocol active - adaptive learning enabled")

        # Context and learning
        self.context_history: List[Dict[str, Any]] = []
        self.learned_preferences: Dict[str, Any] = {}
        self.session_start = time.time()

        # Statistics
        self.stats = {
            'files_analyzed': 0,
            'patterns_recognized': 0,
            'suggestions_made': 0,
            'feedback_received': 0,
            'context_adaptations': 0
        }

        print("✅ AI Dynamic Workflow Assistant initialized")
        if self.white_mirror:
            print("   Learning mode: ADAPTIVE (with White Mirror)")
        else:
            print("   Learning mode: BASIC")

    # ========================================================================
    # CORE OPERATIONS
    # ========================================================================

    def analyze_files(self, file_paths: List[str],
                     context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze multiple files and generate comprehensive insights

        Args:
            file_paths: List of file paths to analyze
            context: Optional context about the analysis purpose

        Returns:
            Complete analysis with insights and suggestions
        """
        print(f"\n🔍 Analyzing {len(file_paths)} files...")

        # Analyze each file
        analyses = []
        for file_path in file_paths:
            if os.path.exists(file_path):
                analysis = self.file_analyzer.analyze_file(file_path)
                analyses.append(analysis)
                self.stats['files_analyzed'] += 1
                print(f"   ✓ {Path(file_path).name} - {analysis.purpose}")
            else:
                print(f"   ✗ {file_path} - File not found")

        if not analyses:
            return {'error': 'No files could be analyzed'}

        # Record operation for pattern learning
        self.pattern_recognizer.record_operation(
            operation_type='analyze',
            files=file_paths,
            result='success'
        )

        # Get relevant patterns
        patterns = self.pattern_recognizer.get_patterns_for_files(file_paths)
        if patterns:
            self.stats['patterns_recognized'] += len(patterns)

        # Generate deployment suggestions
        suggestions = self.deployment_suggester.suggest_deployment(
            analyses, patterns
        )
        self.stats['suggestions_made'] += len(suggestions)

        # Compare files if multiple
        comparisons = []
        if len(analyses) >= 2:
            comparisons.append(compare_files(analyses[0], analyses[1]))

        # Create result
        result = {
            'summary': {
                'total_files': len(analyses),
                'avg_deployment_readiness': sum(a.deployment_readiness for a in analyses) / len(analyses),
                'file_types': list(set(a.file_type for a in analyses)),
                'patterns_found': len(patterns)
            },
            'analyses': [self._analysis_to_dict(a) for a in analyses],
            'patterns': [self._pattern_to_dict(p) for p in patterns],
            'deployment_suggestions': [self._suggestion_to_dict(s) for s in suggestions],
            'comparisons': comparisons,
            'timestamp': time.time()
        }

        # Store in context history
        self.context_history.append({
            'operation': 'analyze_files',
            'files': file_paths,
            'result': result,
            'context': context,
            'timestamp': time.time()
        })

        # Learn from this interaction via White Mirror
        if self.white_mirror:
            self._learn_from_analysis(result, context)

        return result

    def suggest_workflow(self, file_paths: List[str],
                        goal: str = "deploy") -> Dict[str, Any]:
        """
        Suggest optimal workflow for given files and goal

        Args:
            file_paths: Files involved in workflow
            goal: Workflow goal ('deploy', 'test', 'integrate', etc.)

        Returns:
            Suggested workflow with steps
        """
        print(f"\n🎯 Suggesting workflow for goal: {goal}")

        # Analyze files first
        analysis_result = self.analyze_files(file_paths)

        # Get patterns
        patterns = self.pattern_recognizer.get_patterns_for_files(file_paths)

        # Build workflow based on goal
        if goal == "deploy":
            workflow = self._build_deployment_workflow(analysis_result, patterns)
        elif goal == "test":
            workflow = self._build_testing_workflow(analysis_result, patterns)
        elif goal == "integrate":
            workflow = self._build_integration_workflow(analysis_result, patterns)
        else:
            workflow = self._build_generic_workflow(analysis_result, patterns, goal)

        # Learn from suggestion
        if self.white_mirror:
            self.white_mirror.process({
                'purpose': 'suggest_workflow',
                'goal': goal,
                'files': file_paths,
                'workflow': workflow
            })

        return workflow

    def learn_from_feedback(self, operation_id: str, feedback: Dict[str, Any]):
        """
        Learn from user feedback to improve future suggestions

        Args:
            operation_id: ID of the operation being rated
            feedback: Feedback dict with 'rating' (0-1) and optional 'comments'
        """
        self.stats['feedback_received'] += 1

        rating = feedback.get('rating', 0.5)
        comments = feedback.get('comments', '')

        print(f"\n📝 Learning from feedback (rating: {rating:.1%})")

        # Update pattern effectiveness if relevant
        if 'pattern_id' in feedback:
            self.pattern_recognizer.learn_from_feedback(
                feedback['pattern_id'],
                rating
            )

        # Store learned preferences
        if comments:
            # Simple keyword extraction
            keywords = comments.lower().split()
            for keyword in keywords:
                if keyword not in ['the', 'a', 'an', 'is', 'and', 'or']:
                    self.learned_preferences[keyword] = \
                        self.learned_preferences.get(keyword, 0) + (1 if rating > 0.6 else -1)

        # Meta-learning via White Mirror
        if self.white_mirror:
            # Treat negative feedback as a constraint to transform
            if rating < 0.5:
                self.white_mirror.process({
                    'purpose': 'learn_from_constraint',
                    'constraints': [{
                        'type': 'user_feedback',
                        'severity': 1.0 - rating,
                        'feedback': feedback,
                        'information_gain': 2.0
                    }]
                })
                self.stats['context_adaptations'] += 1
            else:
                # Positive feedback reinforces current approach
                self.white_mirror.process({
                    'purpose': 'reinforce_pattern',
                    'feedback': feedback
                })

        print(f"   ✓ Feedback integrated into learning system")

    def get_context_insights(self) -> Dict[str, Any]:
        """
        Get insights from accumulated context and learning

        Returns:
            Insights about learned patterns and preferences
        """
        insights = {
            'session_duration': time.time() - self.session_start,
            'statistics': self.stats.copy(),
            'learned_preferences': self.learned_preferences.copy(),
            'pattern_count': len(self.pattern_recognizer.patterns),
            'context_depth': len(self.context_history)
        }

        if self.white_mirror:
            # Get White Mirror state for meta-insights
            wm_state = self.white_mirror.get_system_state()
            insights['meta_learning'] = {
                'generation': wm_state['operational_state']['generation'],
                'capabilities': len(wm_state['operational_state']['capabilities']),
                'autonomy': wm_state['equations']['autonomy']['autonomy_score'],
                'intelligence': wm_state['equations']['intelligence_growth']['intelligence_density']
            }

        return insights

    def export_learned_context(self, filepath: str):
        """Export learned context for persistence"""
        export_data = {
            'learned_preferences': self.learned_preferences,
            'patterns': [self._pattern_to_dict(p) for p in self.pattern_recognizer.patterns.values()],
            'statistics': self.stats,
            'session_start': self.session_start,
            'export_time': time.time()
        }

        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)

        print(f"💾 Context exported to {filepath}")

    def load_learned_context(self, filepath: str):
        """Load previously learned context"""
        if not os.path.exists(filepath):
            print(f"⚠️  Context file not found: {filepath}")
            return

        with open(filepath, 'r') as f:
            data = json.load(f)

        self.learned_preferences = data.get('learned_preferences', {})
        # TODO: Reconstruct patterns from dict

        print(f"✅ Context loaded from {filepath}")
        self.stats['context_adaptations'] += 1

    # ========================================================================
    # WORKFLOW BUILDERS
    # ========================================================================

    def _build_deployment_workflow(self, analysis: Dict[str, Any],
                                   patterns: List[WorkflowPattern]) -> Dict[str, Any]:
        """Build deployment workflow"""

        steps = []
        suggestions = analysis.get('deployment_suggestions', [])

        if suggestions:
            # Use top suggestion
            top_suggestion = suggestions[0]
            steps = top_suggestion.get('steps', [])
        else:
            # Generic deployment steps
            steps = [
                {'step': 1, 'action': 'Run tests', 'command': 'pytest' if 'python' in str(analysis) else 'npm test'},
                {'step': 2, 'action': 'Build project', 'command': 'python setup.py build'},
                {'step': 3, 'action': 'Deploy', 'command': 'Deploy to target environment'}
            ]

        return {
            'workflow_type': 'deployment',
            'steps': steps,
            'estimated_duration': self._estimate_duration(steps),
            'confidence': analysis['summary']['avg_deployment_readiness'],
            'based_on_patterns': len(patterns) > 0
        }

    def _build_testing_workflow(self, analysis: Dict[str, Any],
                                patterns: List[WorkflowPattern]) -> Dict[str, Any]:
        """Build testing workflow"""

        return {
            'workflow_type': 'testing',
            'steps': [
                {'step': 1, 'action': 'Run unit tests', 'command': 'pytest tests/unit'},
                {'step': 2, 'action': 'Run integration tests', 'command': 'pytest tests/integration'},
                {'step': 3, 'action': 'Generate coverage report', 'command': 'pytest --cov'}
            ],
            'estimated_duration': '10-15 minutes',
            'confidence': 0.85
        }

    def _build_integration_workflow(self, analysis: Dict[str, Any],
                                    patterns: List[WorkflowPattern]) -> Dict[str, Any]:
        """Build integration workflow"""

        return {
            'workflow_type': 'integration',
            'steps': [
                {'step': 1, 'action': 'Review dependencies', 'command': 'Check compatibility'},
                {'step': 2, 'action': 'Merge files', 'command': 'git merge or copy files'},
                {'step': 3, 'action': 'Test integration', 'command': 'Run integration tests'},
                {'step': 4, 'action': 'Update documentation', 'command': 'Document changes'}
            ],
            'estimated_duration': '20-30 minutes',
            'confidence': 0.7
        }

    def _build_generic_workflow(self, analysis: Dict[str, Any],
                               patterns: List[WorkflowPattern],
                               goal: str) -> Dict[str, Any]:
        """Build generic workflow"""

        return {
            'workflow_type': goal,
            'steps': [
                {'step': 1, 'action': f'Prepare for {goal}', 'command': 'Review files'},
                {'step': 2, 'action': f'Execute {goal}', 'command': f'Perform {goal} actions'},
                {'step': 3, 'action': 'Verify results', 'command': 'Check output'}
            ],
            'estimated_duration': '15-20 minutes',
            'confidence': 0.6
        }

    # ========================================================================
    # LEARNING AND ADAPTATION
    # ========================================================================

    def _learn_from_analysis(self, result: Dict[str, Any],
                            context: Optional[Dict[str, Any]]):
        """Use White Mirror Protocol to learn from analysis"""

        # Process through White Mirror for meta-learning
        self.white_mirror.process({
            'purpose': 'learn_from_analysis',
            'result_summary': {
                'files_analyzed': result['summary']['total_files'],
                'readiness': result['summary']['avg_deployment_readiness'],
                'patterns': result['summary']['patterns_found']
            },
            'context': context
        })

        self.stats['context_adaptations'] += 1

    # ========================================================================
    # HELPER METHODS
    # ========================================================================

    def _analysis_to_dict(self, analysis: FileAnalysis) -> Dict[str, Any]:
        """Convert FileAnalysis to dict"""
        return {
            'file_path': analysis.file_path,
            'file_type': analysis.file_type,
            'language': analysis.language,
            'purpose': analysis.purpose,
            'key_points': analysis.key_points,
            'dependencies': analysis.dependencies,
            'deployment_readiness': analysis.deployment_readiness,
            'suggestions': analysis.suggestions
        }

    def _pattern_to_dict(self, pattern: WorkflowPattern) -> Dict[str, Any]:
        """Convert WorkflowPattern to dict"""
        return {
            'pattern_id': pattern.pattern_id,
            'type': pattern.pattern_type,
            'files': pattern.files_involved,
            'confidence': pattern.confidence,
            'effectiveness': pattern.effectiveness,
            'occurrences': pattern.occurrences
        }

    def _suggestion_to_dict(self, suggestion: DeploymentSuggestion) -> Dict[str, Any]:
        """Convert DeploymentSuggestion to dict"""
        return {
            'strategy': suggestion.strategy_name,
            'description': suggestion.description,
            'steps': suggestion.steps,
            'estimated_time': suggestion.estimated_time,
            'confidence': suggestion.confidence,
            'risks': suggestion.risks,
            'benefits': suggestion.benefits
        }

    def _estimate_duration(self, steps: List[Dict[str, Any]]) -> str:
        """Estimate workflow duration"""
        num_steps = len(steps)
        if num_steps <= 3:
            return "5-10 minutes"
        elif num_steps <= 5:
            return "15-25 minutes"
        else:
            return "30-45 minutes"

    def get_dashboard_summary(self) -> str:
        """Get human-readable dashboard summary"""

        insights = self.get_context_insights()

        dashboard = f"""
╔══════════════════════════════════════════════════════════════════════╗
║        AI DYNAMIC WORKFLOW ASSISTANT - DASHBOARD                     ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  📊 SESSION STATISTICS                                              ║
║     • Files Analyzed: {self.stats['files_analyzed']}
║     • Patterns Recognized: {self.stats['patterns_recognized']}
║     • Suggestions Made: {self.stats['suggestions_made']}
║     • Feedback Received: {self.stats['feedback_received']}
║     • Context Adaptations: {self.stats['context_adaptations']}
║                                                                      ║
║  🧠 LEARNING STATUS                                                 ║
║     • Learned Preferences: {len(self.learned_preferences)}
║     • Pattern Library: {len(self.pattern_recognizer.patterns)}
║     • Context Depth: {len(self.context_history)}
║     • Session Duration: {(time.time() - self.session_start)/60:.1f}min
║                                                                      ║
"""

        if 'meta_learning' in insights:
            ml = insights['meta_learning']
            dashboard += f"""║  🔥 META-LEARNING (White Mirror Protocol)                          ║
║     • Generation: {ml['generation']}
║     • Capabilities: {ml['capabilities']}
║     • Autonomy: {ml['autonomy']:.3f}
║     • Intelligence: {ml['intelligence']:.2f}
║                                                                      ║
"""

        dashboard += """╚══════════════════════════════════════════════════════════════════════╝
        """

        return dashboard

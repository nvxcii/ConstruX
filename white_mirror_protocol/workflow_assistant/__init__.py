"""
AI Dynamic Workflow Assistant
Analyzes files, recognizes patterns, suggests workflows with adaptive learning
"""

from .workflow_assistant import WorkflowAssistant
from .core_components import (
    FileAnalyzer,
    WorkflowPatternRecognizer,
    DeploymentSuggester,
    FileAnalysis,
    WorkflowPattern,
    DeploymentSuggestion,
    compare_files
)

__all__ = [
    'WorkflowAssistant',
    'FileAnalyzer',
    'WorkflowPatternRecognizer',
    'DeploymentSuggester',
    'FileAnalysis',
    'WorkflowPattern',
    'DeploymentSuggestion',
    'compare_files'
]

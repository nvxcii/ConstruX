"""
AI Dynamic Workflow Assistant - Example Usage
Demonstrates file analysis, pattern recognition, and adaptive learning
"""

import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from white_mirror_protocol.workflow_assistant import WorkflowAssistant


def main():
    print("\n" + "=" * 70)
    print("AI DYNAMIC WORKFLOW ASSISTANT - DEMONSTRATION")
    print("=" * 70 + "\n")

    # Initialize the assistant
    assistant = WorkflowAssistant(config={
        'enable_learning': True,  # Enable White Mirror integration
        'use_ai': False  # Set True if you have API keys configured
    })

    # ========================================================================
    # DEMO 1: Analyze Files
    # ========================================================================
    print("\n" + "-" * 70)
    print("DEMO 1: File Analysis")
    print("-" * 70 + "\n")

    # Analyze some files from the White Mirror Protocol
    files_to_analyze = [
        'white_mirror_protocol/white_mirror_protocol.py',
        'white_mirror_protocol/core/primal_variables.py',
        'WHITE_MIRROR_PROTOCOL.md'
    ]

    result = assistant.analyze_files(files_to_analyze, context={
        'purpose': 'understand_white_mirror_structure',
        'project': 'White Mirror Protocol'
    })

    print(f"\n📊 Analysis Summary:")
    print(f"   Files analyzed: {result['summary']['total_files']}")
    print(f"   Avg deployment readiness: {result['summary']['avg_deployment_readiness']:.1%}")
    print(f"   File types: {', '.join(result['summary']['file_types'])}")
    print(f"   Patterns found: {result['summary']['patterns_found']}")

    print(f"\n📄 Individual File Analyses:")
    for analysis in result['analyses']:
        print(f"\n   {Path(analysis['file_path']).name}:")
        print(f"     • Purpose: {analysis['purpose']}")
        print(f"     • Deployment readiness: {analysis['deployment_readiness']:.1%}")
        print(f"     • Key points:")
        for point in analysis['key_points'][:3]:
            print(f"       - {point}")

    if result.get('deployment_suggestions'):
        print(f"\n💡 Deployment Suggestions:")
        for i, suggestion in enumerate(result['deployment_suggestions'][:2], 1):
            print(f"\n   {i}. {suggestion['strategy']}")
            print(f"      {suggestion['description']}")
            print(f"      Confidence: {suggestion['confidence']:.1%}")
            print(f"      Est. time: {suggestion['estimated_time']}")

    # ========================================================================
    # DEMO 2: Workflow Suggestion
    # ========================================================================
    print("\n\n" + "-" * 70)
    print("DEMO 2: Workflow Suggestion")
    print("-" * 70 + "\n")

    workflow = assistant.suggest_workflow(
        file_paths=files_to_analyze,
        goal="deploy"
    )

    print(f"🎯 Suggested Workflow: {workflow['workflow_type'].title()}")
    print(f"   Estimated duration: {workflow['estimated_duration']}")
    print(f"   Confidence: {workflow['confidence']:.1%}")
    print(f"\n📋 Steps:")
    for step in workflow['steps']:
        print(f"   {step['step']}. {step['action']}")
        if 'command' in step:
            print(f"      Command: {step['command']}")

    # ========================================================================
    # DEMO 3: Pattern Recognition
    # ========================================================================
    print("\n\n" + "-" * 70)
    print("DEMO 3: Pattern Recognition (Learning)")
    print("-" * 70 + "\n")

    # Simulate multiple operations to learn patterns
    print("Simulating file operations to learn patterns...\n")

    operations = [
        (['file1.py', 'file2.py'], 'integrate'),
        (['file1.py', 'file3.py'], 'test'),
        (['file1.py', 'file2.py'], 'deploy'),  # Repeat pattern
        (['file2.py', 'file4.py'], 'integrate')
    ]

    for files, op_type in operations:
        assistant.pattern_recognizer.record_operation(op_type, files, 'success')
        print(f"   ✓ Recorded: {op_type} on {', '.join(files)}")

    patterns = list(assistant.pattern_recognizer.patterns.values())
    print(f"\n📈 Patterns Recognized: {len(patterns)}")
    for pattern in patterns[:3]:
        print(f"\n   Pattern: {pattern.pattern_type}")
        print(f"     Files: {', '.join(pattern.files_involved)}")
        print(f"     Confidence: {pattern.confidence:.1%}")
        print(f"     Occurrences: {pattern.occurrences}")

    # ========================================================================
    # DEMO 4: Learning from Feedback
    # ========================================================================
    print("\n\n" + "-" * 70)
    print("DEMO 4: Adaptive Learning from Feedback")
    print("-" * 70 + "\n")

    # Positive feedback
    assistant.learn_from_feedback(
        operation_id='demo_001',
        feedback={
            'rating': 0.9,
            'comments': 'Great suggestion, deploy workflow worked perfectly'
        }
    )

    # Negative feedback (treated as constraint to transform)
    assistant.learn_from_feedback(
        operation_id='demo_002',
        feedback={
            'rating': 0.3,
            'comments': 'Testing steps were missing, need more comprehensive test coverage'
        }
    )

    print(f"\n🧠 Learned Preferences:")
    for pref, score in sorted(assistant.learned_preferences.items(),
                              key=lambda x: abs(x[1]), reverse=True)[:5]:
        sentiment = "positive" if score > 0 else "negative"
        print(f"   • '{pref}': {sentiment} ({score:+d})")

    # ========================================================================
    # DEMO 5: Context Insights
    # ========================================================================
    print("\n\n" + "-" * 70)
    print("DEMO 5: Context Insights & Meta-Learning")
    print("-" * 70 + "\n")

    insights = assistant.get_context_insights()

    print(f"📊 Session Statistics:")
    for key, value in insights['statistics'].items():
        print(f"   • {key.replace('_', ' ').title()}: {value}")

    if 'meta_learning' in insights:
        print(f"\n🔥 Meta-Learning (White Mirror Protocol):")
        ml = insights['meta_learning']
        print(f"   • Generation: {ml['generation']}")
        print(f"   • Capabilities developed: {ml['capabilities']}")
        print(f"   • System autonomy: {ml['autonomy']:.3f}")
        print(f"   • Intelligence density: {ml['intelligence']:.2f}")

    # ========================================================================
    # DEMO 6: Dashboard
    # ========================================================================
    print("\n\n" + "-" * 70)
    print("DEMO 6: Dashboard")
    print("-" * 70 + "\n")

    dashboard = assistant.get_dashboard_summary()
    print(dashboard)

    # ========================================================================
    # DEMO 7: Export/Import Context
    # ========================================================================
    print("\n" + "-" * 70)
    print("DEMO 7: Context Persistence")
    print("-" * 70 + "\n")

    export_path = '/tmp/workflow_assistant_context.json'
    assistant.export_learned_context(export_path)

    print(f"\n   Context can be loaded in future sessions to preserve learning")

    # ========================================================================
    # Summary
    # ========================================================================
    print("\n\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("\nKey Features Demonstrated:")
    print("  ✓ File analysis with purpose detection")
    print("  ✓ Deployment strategy suggestions")
    print("  ✓ Workflow pattern recognition")
    print("  ✓ Adaptive learning from feedback")
    print("  ✓ Meta-learning with White Mirror Protocol")
    print("  ✓ Context accumulation and insights")
    print("  ✓ Persistent learning across sessions")
    print("\nThe assistant learns and adapts over time, becoming more intuitive!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

"""
White Mirror Protocol - Meta-Orchestration Example
Demonstrates integration with Multi-AI Justice League
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from white_mirror_protocol.integration.multi_ai_integration import WhiteMirrorAIOrchestrator


def main():
    print("\n" + "=" * 70)
    print("WHITE MIRROR PROTOCOL - META-ORCHESTRATION DEMONSTRATION")
    print("=" * 70 + "\n")

    # Initialize meta-orchestrator
    # Note: This requires API keys to be set in environment variables
    orchestrator = WhiteMirrorAIOrchestrator()

    print("\n" + "-" * 70)
    print("DEMONSTRATION 1: System Evolution (No API Calls)")
    print("-" * 70 + "\n")

    # Evolve the orchestration system
    evolution_results = orchestrator.evolve_orchestration(iterations=3)

    print(f"✓ Orchestration system evolved")
    print(f"  Evolution iterations: {len(evolution_results)}")

    print("\n" + "-" * 70)
    print("DEMONSTRATION 2: Meta-Orchestration Dashboard")
    print("-" * 70 + "\n")

    # Display combined dashboard
    dashboard = orchestrator.get_meta_orchestration_dashboard()
    print(dashboard)

    print("\n" + "-" * 70)
    print("DEMONSTRATION 3: Coordination Insights")
    print("-" * 70 + "\n")

    insights = orchestrator.get_coordination_insights()
    print("Coordination Insights:")
    for key, value in insights.items():
        print(f"  {key}: {value}")

    print("\n" + "-" * 70)
    print("DEMONSTRATION 4: State Export")
    print("-" * 70 + "\n")

    # Export meta-orchestration state
    export_path = '/tmp/meta_orchestration_state.json'
    orchestrator.export_meta_state(export_path)

    print("\n" + "=" * 70)
    print("META-ORCHESTRATION DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("\nTo execute a full mission with multi-AI coordination, use:")
    print("  orchestrator.execute_mission_with_meta_orchestration(case_data)")
    print("\nThis requires valid API keys for: Claude, Gemini, DeepSeek, ChatGPT\n")


def demonstrate_full_mission():
    """
    Demonstrates full mission execution with meta-orchestration
    Requires API keys to be configured
    """
    # Sample case data
    case_data = {
        'case_id': 'demo_001',
        'mission_name': 'White Mirror Demo Mission',
        'summary': 'Demonstration of meta-orchestrated AI coordination',
        'legal_issues': 'Sample legal analysis',
        'regulatory_context': 'Sample regulatory framework',
        'human_story': 'Sample human impact narrative'
    }

    orchestrator = WhiteMirrorAIOrchestrator()

    # Execute mission with meta-orchestration
    results = orchestrator.execute_mission_with_meta_orchestration(
        case_data=case_data,
        export_dir='./output/demo_mission'
    )

    print("\n✓ Mission complete!")
    print(f"  White Mirror generation: {results['meta_orchestration']['white_mirror_state']['operational_state']['generation']}")
    print(f"  System autonomy: {results['meta_orchestration']['coherence']['coherence']:.3f}")


if __name__ == "__main__":
    main()

    # Uncomment to run full mission (requires API keys)
    # demonstrate_full_mission()

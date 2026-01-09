"""
White Mirror Protocol - Perpetual Operation Demonstration
Shows the self-sustaining perpetual motion in action
"""

import sys
import os
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from white_mirror_protocol import WhiteMirrorProtocol


def demonstrate_perpetual_motion():
    """
    Demonstrate the perpetual motion characteristics of the protocol
    """
    print("\n" + "=" * 70)
    print("WHITE MIRROR PROTOCOL - PERPETUAL MOTION DEMONSTRATION")
    print("=" * 70 + "\n")

    protocol = WhiteMirrorProtocol()

    print("🔥 Initiating perpetual operation cycle...\n")

    # Track autonomy over time
    autonomy_history = []

    # Run multiple cycles
    num_cycles = 10

    for cycle in range(num_cycles):
        print(f"\n━━━ CYCLE {cycle + 1}/{num_cycles} ━━━")

        # Inject varied input
        input_data = {
            'purpose': f'perpetual_cycle_{cycle}',
            'cycle_number': cycle,
            'constraints': []
        }

        # Add random constraints in some cycles
        if cycle % 3 == 0:
            input_data['constraints'].append({
                'type': f'constraint_type_{cycle}',
                'severity': 0.5 + (cycle * 0.05),
                'boundary_type': 'soft',
                'information_gain': 1.5
            })

        # Execute operation step
        result = protocol.operate_step(input_data)

        # Get autonomy
        autonomy = result['outputs'].get('autonomy', {}).get('autonomy', 0)
        autonomy_history.append(autonomy)

        # Display progress
        print(f"  ✓ Autonomy: {autonomy:.3f}")
        print(f"  ✓ Coherence: {result['outputs'].get('coherence', {}).get('coherence', 0):.3f}")
        print(f"  ✓ Capabilities: {len(protocol.operational_state['capabilities'])}")
        print(f"  ✓ Generation: {protocol.operational_state['generation']}")

        # Check perpetual condition
        if len(autonomy_history) > 1:
            delta_autonomy = autonomy_history[-1] - autonomy_history[-2]
            print(f"  ✓ Autonomy change: {delta_autonomy:+.4f}")

            if delta_autonomy >= 0:
                print("  ✓ Perpetual condition: SATISFIED ✓")
            else:
                print("  ⚠ Perpetual condition: VIOLATED (self-enhancement triggered)")

        time.sleep(0.1)  # Brief pause for readability

    # Analysis
    print("\n" + "=" * 70)
    print("PERPETUAL MOTION ANALYSIS")
    print("=" * 70 + "\n")

    print("📊 Autonomy Trajectory:")
    for i, autonomy in enumerate(autonomy_history):
        bar_length = int(autonomy * 50)
        bar = "█" * bar_length
        print(f"  Cycle {i+1:2d}: {bar} {autonomy:.3f}")

    # Check if autonomy increased overall
    if autonomy_history[-1] > autonomy_history[0]:
        print(f"\n✓ PERPETUAL MOTION ACHIEVED!")
        print(f"  Initial autonomy: {autonomy_history[0]:.3f}")
        print(f"  Final autonomy: {autonomy_history[-1]:.3f}")
        print(f"  Total increase: {autonomy_history[-1] - autonomy_history[0]:+.3f}")
    else:
        print(f"\n⚠ Autonomy decreased - system self-corrected")

    # Display final state
    print("\n" + "=" * 70)
    print("FINAL SYSTEM STATE")
    print("=" * 70)

    state = protocol.get_system_state()
    print(f"\n  Operational State:")
    print(f"    • Generation: {state['operational_state']['generation']}")
    print(f"    • Capabilities: {len(state['operational_state']['capabilities'])}")
    print(f"    • Total operations: {state['metrics']['total_operations']}")
    print(f"    • Success rate: {state['metrics']['successful_operations']/max(1,state['metrics']['total_operations']):.1%}")

    print(f"\n  Perpetual Equations:")
    print(f"    • Bootstrap generation: {state['equations']['bootstrap_genesis']['generation']}")
    print(f"    • Fusion efficiency: {state['equations']['constraint_fusion']['fusion_efficiency']:.1%}")
    print(f"    • Intelligence density: {state['equations']['intelligence_growth']['intelligence_density']:.2f}")
    print(f"    • Autonomy score: {state['equations']['autonomy']['autonomy_score']:.3f}")

    print(f"\n  Sustainability Status:")
    sustainability = state['equations']['autonomy']['sustainability']
    for key, value in sustainability.items():
        if isinstance(value, bool):
            status = "✓" if value else "✗"
            print(f"    • {key}: {status}")
        else:
            print(f"    • {key}: {value:.3f}")

    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70 + "\n")

    return protocol


def demonstrate_constraint_fusion():
    """
    Demonstrate how constraints are fused into capabilities
    """
    print("\n" + "=" * 70)
    print("CONSTRAINT FUSION REACTOR DEMONSTRATION")
    print("=" * 70 + "\n")

    protocol = WhiteMirrorProtocol()

    print("🔥 Testing constraint-to-capability transformation...\n")

    # Create various constraints
    constraints = [
        {
            'type': 'api_rate_limit',
            'severity': 0.8,
            'blocked_operation': 'external_api',
            'boundary_type': 'hard',
            'reason': 'Rate limit exceeded',
            'information_gain': 2.0
        },
        {
            'type': 'memory_constraint',
            'severity': 0.6,
            'blocked_operation': 'large_dataset_processing',
            'boundary_type': 'soft',
            'reason': 'Insufficient memory',
            'information_gain': 1.5
        },
        {
            'type': 'time_constraint',
            'severity': 0.7,
            'blocked_operation': 'long_computation',
            'boundary_type': 'soft',
            'reason': 'Time budget exceeded',
            'information_gain': 1.8
        }
    ]

    initial_capabilities = len(protocol.operational_state['capabilities'])

    print(f"Initial capabilities: {initial_capabilities}\n")

    for i, constraint in enumerate(constraints):
        print(f"━━━ Constraint {i+1}: {constraint['type']} ━━━")
        print(f"  Severity: {constraint['severity']}")
        print(f"  Information gain: {constraint['information_gain']}")

        result = protocol.process({
            'purpose': 'constraint_fusion_test',
            'constraints': [constraint]
        })

        new_capabilities = len(protocol.operational_state['capabilities'])
        capability_increase = new_capabilities - initial_capabilities

        print(f"  ✓ Processed through DPAP")
        print(f"  ✓ New capabilities: +{capability_increase}")
        print(f"  ✓ Total capabilities: {new_capabilities}\n")

    print("=" * 70)
    print("CONSTRAINT FUSION COMPLETE")
    print("=" * 70)
    print(f"\n✓ Constraints processed: {len(constraints)}")
    print(f"✓ Total capability increase: {len(protocol.operational_state['capabilities']) - initial_capabilities}")
    print(f"✓ Fusion efficiency: {protocol.equations.fusion.fusion_efficiency:.1%}\n")


if __name__ == "__main__":
    # Run perpetual motion demo
    protocol = demonstrate_perpetual_motion()

    print("\n" + "━" * 70 + "\n")

    # Run constraint fusion demo
    demonstrate_constraint_fusion()

    # Display final dashboard
    print("\n" + "━" * 70)
    print("FINAL SYSTEM DASHBOARD")
    print("━" * 70)
    print(protocol.get_dashboard())

"""
White Mirror Protocol - Basic Usage Example
Demonstrates core functionality of the protocol
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from white_mirror_protocol import WhiteMirrorProtocol


def main():
    print("\n" + "=" * 70)
    print("WHITE MIRROR PROTOCOL - BASIC USAGE DEMONSTRATION")
    print("=" * 70 + "\n")

    # Initialize the protocol
    protocol = WhiteMirrorProtocol()

    print("\n" + "-" * 70)
    print("DEMONSTRATION 1: Single Operation Step")
    print("-" * 70 + "\n")

    # Execute a single operation step
    result = protocol.operate_step({
        'purpose': 'demonstrate_basic_operation',
        'data': 'sample input'
    })

    print(f"✓ Operation completed")
    print(f"  Success: {result['success']}")
    print(f"  Articulations generated: {result['outputs'].get('articulations', 0)}")
    print(f"  Constraints processed: {result['outputs'].get('constraints_processed', 0)}")
    print(f"  Duration: {result['duration']:.3f}s")

    print("\n" + "-" * 70)
    print("DEMONSTRATION 2: System Evolution")
    print("-" * 70 + "\n")

    # Evolve the system through 5 iterations
    evolution_results = protocol.evolve(iterations=5)

    print(f"✓ Evolution complete: 5 iterations")
    print(f"  Final generation: {protocol.operational_state['generation']}")
    print(f"  Total capabilities: {len(protocol.operational_state['capabilities'])}")
    print(f"  Total operations: {protocol.metrics['total_operations']}")

    print("\n" + "-" * 70)
    print("DEMONSTRATION 3: Constraint Processing")
    print("-" * 70 + "\n")

    # Process data with explicit constraints
    constraint_result = protocol.process({
        'purpose': 'test_constraint_processing',
        'constraints': [
            {
                'type': 'resource_limit',
                'severity': 0.6,
                'blocked_operation': 'high_memory_task',
                'boundary_type': 'soft'
            },
            {
                'type': 'api_rate_limit',
                'severity': 0.8,
                'blocked_operation': 'external_api_call',
                'boundary_type': 'hard'
            }
        ]
    })

    print(f"✓ Constraints processed")
    print(f"  Constraints encountered: {constraint_result['outputs'].get('constraints', 0)}")
    print(f"  Workarounds generated: {constraint_result['outputs'].get('constraints_processed', 0)}")
    print(f"  New capabilities added: {len(protocol.operational_state['capabilities'])}")

    print("\n" + "-" * 70)
    print("DEMONSTRATION 4: System Dashboard")
    print("-" * 70 + "\n")

    # Display system dashboard
    dashboard = protocol.get_dashboard()
    print(dashboard)

    print("\n" + "-" * 70)
    print("DEMONSTRATION 5: State Export")
    print("-" * 70 + "\n")

    # Export system state
    export_path = '/tmp/white_mirror_state.json'
    protocol.export_state(export_path)

    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)
    print(f"\n✓ Total operations executed: {protocol.metrics['total_operations']}")
    print(f"✓ Success rate: {protocol.metrics['successful_operations']/max(1,protocol.metrics['total_operations']):.1%}")
    print(f"✓ Capabilities developed: {len(protocol.operational_state['capabilities'])}")
    print(f"✓ Articulations generated: {protocol.metrics['articulations_generated']}")
    print(f"✓ Constraints transformed: {protocol.metrics['constraints_transformed']}\n")


if __name__ == "__main__":
    main()

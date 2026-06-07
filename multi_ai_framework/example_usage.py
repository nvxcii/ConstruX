#!/usr/bin/env python3
"""
Example Usage of Multi-AI Justice League Framework
Demonstrates how to execute a complete mission
"""

import json
from pathlib import Path
from multi_ai_framework.missions.mission_orchestrator import MissionOrchestrator
from multi_ai_framework.config.config_manager import ConfigManager


def main():
    """Run example mission"""

    print("\n" + "="*80)
    print("MULTI-AI JUSTICE LEAGUE FRAMEWORK - EXAMPLE USAGE")
    print("="*80 + "\n")

    # Step 1: Load configuration
    print("Step 1: Loading configuration...")
    config = ConfigManager()

    # Validate API keys are configured
    validation = config.validate_api_keys()
    print("\nAPI Key Validation:")
    for key, valid in validation.items():
        status = "✓" if valid else "✗"
        print(f"  {status} {key}: {'Configured' if valid else 'Missing'}")

    if not all(validation.values()):
        print("\n⚠️  Warning: Some API keys are missing.")
        print("Set environment variables or update config for full functionality.\n")

    # Step 2: Load case data
    print("\nStep 2: Loading case data...")
    case_config_path = Path(__file__).parent / "missions" / "gaylord_justice_campaign" / "campaign_config.json"

    with open(case_config_path, 'r') as f:
        case_data = json.load(f)

    print(f"✓ Loaded case: {case_data.get('mission_name', 'Unknown')}")

    # Step 3: Initialize orchestrator
    print("\nStep 3: Initializing Mission Orchestrator...")
    orchestrator = MissionOrchestrator(config)
    print("✓ Orchestrator initialized")

    # Step 4: Execute mission
    print("\nStep 4: Executing complete mission...")
    print("This will:")
    print("  1. Gather intelligence using all AI models")
    print("  2. Perform strategic analysis")
    print("  3. Generate execution plans")
    print("\nThis may take several minutes...\n")

    # Set export directory
    export_dir = "./output/gaylord_campaign"

    # Execute mission
    try:
        results = orchestrator.execute_complete_mission(
            case_data=case_data,
            export_dir=export_dir
        )

        # Display summary
        print("\n" + "="*80)
        print("MISSION RESULTS SUMMARY")
        print("="*80)

        executive_summary = results.get('executive_summary', {})
        mission_overview = executive_summary.get('mission_overview', {})

        print(f"\nCase ID: {mission_overview.get('case_id', 'Unknown')}")
        print(f"Phases Completed: {mission_overview.get('phases_completed', 0)}/3")
        print(f"Success Rate: {mission_overview.get('overall_success_rate', 0)*100:.1f}%")

        # Strategic Analysis Summary
        strategic = results.get('strategic_analysis', {})
        if strategic:
            leverage = strategic.get('leverage_analysis', {})
            settlement = strategic.get('settlement_prediction', {})

            print(f"\nLeverage Score: {leverage.get('overall_leverage_score', 0):.1f}/100")
            print(f"Risk to Opponent: {leverage.get('risk_to_opponent', 'Unknown')}")

            pred_range = settlement.get('predicted_range', {})
            print(f"\nSettlement Range:")
            print(f"  Low:  ${pred_range.get('low', 0):,.0f}")
            print(f"  Mid:  ${pred_range.get('mid', 0):,.0f}")
            print(f"  High: ${pred_range.get('high', 0):,.0f}")

            print(f"\nRecommended Demand: ${settlement.get('recommended_demand', 0):,.0f}")
            print(f"Settlement Floor: ${settlement.get('recommended_floor', 0):,.0f}")

        # Execution Summary
        execution = results.get('execution_plan', {})
        if execution:
            deployment = execution.get('deployment_summary', {})
            print(f"\nExecution Package:")
            print(f"  Complaints Prepared: {deployment.get('total_complaints', 0)}")
            print(f"  Media Strategy: {deployment.get('media_approach', 'N/A')}")

        print(f"\n✓ Complete results exported to: {export_dir}")
        print("\nMission execution complete!\n")

    except Exception as e:
        print(f"\n✗ Error executing mission: {e}")
        import traceback
        traceback.print_exc()


def example_phase_by_phase():
    """Example of running phases individually"""

    print("\n" + "="*80)
    print("EXAMPLE: PHASE-BY-PHASE EXECUTION")
    print("="*80 + "\n")

    config = ConfigManager()
    orchestrator = MissionOrchestrator(config)

    # Load case data
    case_config_path = Path(__file__).parent / "missions" / "gaylord_justice_campaign" / "campaign_config.json"
    with open(case_config_path, 'r') as f:
        case_data = json.load(f)

    # Phase 1: Intelligence only
    print("\nExecuting Phase 1: Intelligence Gathering...")
    intelligence = orchestrator.execute_intelligence_only(case_data)
    print(f"✓ Intelligence gathered: {len(intelligence.get('findings', {}))} sources")

    # Phase 2: Analysis only
    print("\nExecuting Phase 2: Strategic Analysis...")
    analysis = orchestrator.execute_analysis_only(case_data, intelligence)
    print(f"✓ Analysis complete: Leverage score {analysis.get('leverage_analysis', {}).get('overall_leverage_score', 0):.1f}")

    # Phase 3: Execution only
    print("\nExecuting Phase 3: Execution Planning...")
    execution = orchestrator.execute_execution_only(case_data, analysis, intelligence)
    print(f"✓ Execution plan ready: {len(execution.get('complaints', []))} complaints prepared")

    print("\nPhase-by-phase execution complete!\n")


if __name__ == "__main__":
    # Run complete mission example
    main()

    # Optionally run phase-by-phase example
    # example_phase_by_phase()

"""
Generate CoworkDispatch documents for the Kyle Theus case (26STUD00430).

Run from this directory:
    python generate_dispatch.py

Outputs to /output/:
    COWORK_DISPATCH.txt
    cowork_dispatch.json
"""

import json
import os
import sys

# Allow running from this directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from multi_ai_framework.execution.cowork_dispatcher import CoworkDispatcher

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "../../../output")
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "case_config.json")


def main():
    print("=" * 60)
    print("ConstruX — CoworkDispatch Generator")
    print("Case: 26STUD00430 — Gateways Apartment LP v. Kyle Theus")
    print("=" * 60)

    # Load case config
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        case_data = json.load(f)

    # Generate dispatch document
    dispatcher = CoworkDispatcher()
    doc = dispatcher.generate_dispatch(case_data)

    # Save outputs
    paths = dispatcher.save(doc, OUTPUT_DIR)

    print(f"\n[OK] Dispatch document written:")
    print(f"     TXT  -> {paths['txt']}")
    print(f"     JSON -> {paths['json']}")

    # Summary stats
    total_layers = sum(len(m.evidence_layers) for m in doc.matters)
    total_tasks = len(doc.task_priorities)
    total_docs = len(doc.critical_documents)

    print(f"\nDispatch summary:")
    print(f"  Matters:          {len(doc.matters)}")
    print(f"  Evidence layers:  {total_layers}")
    print(f"  Task priorities:  {total_tasks}")
    print(f"  Critical docs:    {total_docs}")
    print(f"  Field state:      {doc.field_state}")
    print(f"\nReady for handoff.")


if __name__ == "__main__":
    main()

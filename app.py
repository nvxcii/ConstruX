"""
ConstruX Web Interface
Chat-style UI for running Multi-AI Framework missions.
"""
import json
import threading
import uuid
import os
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "construx-dev-key")

_lock = threading.Lock()
_missions: dict = {}  # mission_id → {status, phase, phase_label, result, error}

STEPS = [
    ("description", "What's the situation? Describe the case you want analyzed."),
    ("employer",    "What's the name of the employer or organization involved?"),
    ("client",      "What's the client's name?"),
    ("violations",  "What violations or issues should we focus on? (comma-separated, e.g. unsafe conditions, unpaid wages, discrimination)"),
]


@app.route("/")
def index():
    session.clear()
    return render_template("chat.html")


@app.route("/api/start", methods=["POST"])
def start():
    session["step"] = 0
    session["answers"] = {}
    return jsonify({"messages": [{"role": "assistant", "text": (
        "Welcome to the Multi-AI Mission Interface. I'll help you run a full "
        "3-phase analysis using Claude, Gemini, DeepSeek, and ChatGPT in parallel.\n\n"
        + STEPS[0][1]
    )}]})


@app.route("/api/message", methods=["POST"])
def message():
    text = (request.json or {}).get("text", "").strip()
    if not text:
        return jsonify({"error": "empty"}), 400

    step    = session.get("step", 0)
    answers = session.get("answers", {})
    replies = []

    if isinstance(step, int) and step < len(STEPS):
        key = STEPS[step][0]
        answers[key] = text
        session["answers"] = answers
        next_step = step + 1

        if next_step < len(STEPS):
            session["step"] = next_step
            replies.append({"role": "assistant", "text": STEPS[next_step][1]})
        else:
            session["step"] = "confirm"
            summary = (
                "Here's what I have:\n\n"
                f"**Situation:** {answers['description']}\n"
                f"**Employer:** {answers['employer']}\n"
                f"**Client:** {answers['client']}\n"
                f"**Issues:** {answers['violations']}\n\n"
                "Ready to run the 3-phase live analysis? This will make real API calls "
                "to all four AI providers.\n\nType **yes** to proceed."
            )
            replies.append({"role": "assistant", "text": summary})

    elif step == "confirm":
        if text.lower() in ("yes", "y", "run", "go", "proceed", "start"):
            mission_id = uuid.uuid4().hex[:8]
            session["mission_id"] = mission_id
            session["step"] = "running"

            case_data = {
                "mission_name": f"{answers.get('client', 'Case')} v. {answers.get('employer', 'Employer')}",
                "case_id": f"CASE-{mission_id.upper()}",
                "client_name": answers.get("client", ""),
                "employer_name": answers.get("employer", ""),
                "situation_description": answers.get("description", ""),
                "violations": [v.strip() for v in answers.get("violations", "").split(",")],
            }

            with _lock:
                _missions[mission_id] = {
                    "status": "running",
                    "phase": 0,
                    "phase_label": "Initializing",
                    "result": None,
                    "error": None,
                }

            threading.Thread(
                target=_run_mission, args=(mission_id, case_data), daemon=True
            ).start()

            replies.append({
                "role": "assistant",
                "text": f"Mission `{mission_id}` started. Running Phase 1: Intelligence Gathering…",
                "mission_id": mission_id,
            })
        else:
            replies.append({
                "role": "assistant",
                "text": "No problem — type **yes** when ready, or tell me what to change.",
            })

    elif step == "running":
        replies.append({
            "role": "assistant",
            "text": "The mission is still running. I'll update you when it finishes.",
        })

    return jsonify({"messages": replies})


@app.route("/api/mission/<mission_id>")
def mission_status(mission_id):
    with _lock:
        mission = dict(_missions.get(mission_id) or {})
    if not mission:
        return jsonify({"error": "not found"}), 404
    return app.response_class(
        json.dumps(mission, default=str), mimetype="application/json"
    )


def _run_mission(mission_id: str, case_data: dict) -> None:
    def update(**kwargs):
        with _lock:
            _missions[mission_id].update(kwargs)

    try:
        from multi_ai_framework.missions.mission_orchestrator import MissionOrchestrator
        from multi_ai_framework.config.config_manager import ConfigManager

        config = ConfigManager()
        orchestrator = MissionOrchestrator(config)

        update(phase=1, phase_label="Intelligence Gathering")
        intelligence = orchestrator.execute_intelligence_only(case_data)

        update(phase=2, phase_label="Strategic Analysis")
        analysis = orchestrator.execute_analysis_only(case_data, intelligence)

        update(phase=3, phase_label="Execution Planning")
        execution = orchestrator.execute_execution_only(case_data, analysis, intelligence)

        update(status="complete", result={
            "intelligence": intelligence,
            "strategic_analysis": analysis,
            "execution_plan": execution,
        })
    except Exception as exc:
        import traceback
        update(status="error", error=str(exc), traceback=traceback.format_exc())


if __name__ == "__main__":
    app.run(debug=True, port=5000)

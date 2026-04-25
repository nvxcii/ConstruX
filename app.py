"""
ConstruX Web Interface
Chat-style UI for running Multi-AI Framework missions with file upload support.
"""
import json
import os
import threading
import uuid
from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "construx-dev-key")
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024  # 32 MB max per upload

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXT = {
    ".pdf", ".txt", ".md", ".csv", ".rtf",   # documents
    ".docx", ".doc",                           # Word
    ".png", ".jpg", ".jpeg", ".gif", ".webp",  # images
}

_lock = threading.Lock()
_missions: dict = {}

STEPS = [
    ("description", "What's the situation? Describe the case you want analyzed."),
    ("employer",    "What's the name of the employer or organization involved?"),
    ("client",      "What's the client's name?"),
    ("violations",  "What violations or issues should we focus on? (comma-separated, e.g. unsafe conditions, unpaid wages)"),
]


# ── File helpers ──────────────────────────────────────────────────────────────

def _file_ext(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()


def _extract_text(path: str, filename: str):
    """Extract readable text from a document. Returns None for images."""
    ext = _file_ext(filename)
    try:
        if ext in (".txt", ".md", ".csv", ".rtf"):
            with open(path, "r", errors="replace") as f:
                return f.read(400_000)

        if ext == ".pdf":
            try:
                from pypdf import PdfReader
            except ImportError:
                try:
                    from PyPDF2 import PdfReader
                except ImportError:
                    return "[PDF — run: pip install pypdf]"
            reader = PdfReader(path)
            return "\n".join(p.extract_text() or "" for p in reader.pages)[:400_000]

        if ext in (".docx", ".doc"):
            try:
                import docx
                doc = docx.Document(path)
                return "\n".join(p.text for p in doc.paragraphs)[:400_000]
            except ImportError:
                return "[DOCX — run: pip install python-docx]"

    except Exception as exc:
        return f"[Could not read file: {exc}]"

    return None  # images and unsupported types


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    session.clear()
    return render_template("chat.html")


@app.route("/api/start", methods=["POST"])
def start():
    session["step"] = 0
    session["answers"] = {}
    session["uploads"] = []
    return jsonify({"messages": [{"role": "assistant", "text": (
        "Welcome to the Λ Mission Interface. I'll guide you through a live "
        "3-phase analysis across Claude, Gemini, DeepSeek, and ChatGPT.\n\n"
        "You can attach supporting documents or media at any time using the "
        "attach button below.\n\n"
        + STEPS[0][1]
    )}]})


@app.route("/api/upload", methods=["POST"])
def upload():
    f = request.files.get("file")
    if not f or not f.filename:
        return jsonify({"error": "No file provided"}), 400

    ext = _file_ext(f.filename)
    if ext not in ALLOWED_EXT:
        return jsonify({"error": f"File type '{ext}' not supported"}), 400

    uploads = session.get("uploads", [])
    if len(uploads) >= 10:
        return jsonify({"error": "Maximum 10 files per session"}), 400

    safe  = secure_filename(f.filename)
    stored = f"{uuid.uuid4().hex[:8]}_{safe}"
    path  = os.path.join(UPLOAD_DIR, stored)
    f.save(path)

    is_image = ext in (".png", ".jpg", ".jpeg", ".gif", ".webp")
    entry = {"name": safe, "stored": stored, "size": os.path.getsize(path), "is_image": is_image}

    uploads.append(entry)
    session["uploads"] = uploads
    session.modified = True

    return jsonify({"name": safe, "size": entry["size"], "is_image": is_image, "index": len(uploads) - 1})


@app.route("/api/remove_upload", methods=["POST"])
def remove_upload():
    idx = (request.json or {}).get("index")
    uploads = session.get("uploads", [])
    if idx is None or not (0 <= idx < len(uploads)):
        return jsonify({"error": "invalid index"}), 400

    entry = uploads.pop(idx)
    session["uploads"] = uploads
    session.modified = True

    try:
        os.remove(os.path.join(UPLOAD_DIR, entry["stored"]))
    except OSError:
        pass

    return jsonify({"ok": True})


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
            uploads = session.get("uploads", [])
            n = len(uploads)
            doc_note = f"\n**Attached:** {n} file{'s' if n != 1 else ''}" if n else ""
            summary = (
                "Here's what I have:\n\n"
                f"**Situation:** {answers['description']}\n"
                f"**Employer:** {answers['employer']}\n"
                f"**Client:** {answers['client']}\n"
                f"**Issues:** {answers['violations']}"
                f"{doc_note}\n\n"
                "Ready to run the live 3-phase analysis? Type **yes** to proceed."
            )
            replies.append({"role": "assistant", "text": summary})

    elif step == "confirm":
        if text.lower() in ("yes", "y", "run", "go", "proceed", "start"):
            mission_id = uuid.uuid4().hex[:8]
            session["mission_id"] = mission_id
            session["step"] = "running"

            # Extract text from uploaded documents
            uploads = session.get("uploads", [])
            doc_texts = []
            for u in uploads:
                if not u["is_image"]:
                    path = os.path.join(UPLOAD_DIR, u["stored"])
                    extracted = _extract_text(path, u["name"])
                    if extracted:
                        doc_texts.append(f"[{u['name']}]\n{extracted}")

            situation = answers.get("description", "")
            if doc_texts:
                situation += "\n\nSupporting documentation:\n\n" + "\n\n---\n\n".join(doc_texts)

            case_data = {
                "mission_name": f"{answers.get('client', 'Case')} v. {answers.get('employer', 'Employer')}",
                "case_id": f"CASE-{mission_id.upper()}",
                "client_name": answers.get("client", ""),
                "employer_name": answers.get("employer", ""),
                "situation_description": situation,
                "violations": [v.strip() for v in answers.get("violations", "").split(",")],
                "attached_files": [u["name"] for u in uploads],
            }

            with _lock:
                _missions[mission_id] = {
                    "status": "running", "phase": 0,
                    "phase_label": "Initializing", "result": None, "error": None,
                }

            threading.Thread(target=_run_mission, args=(mission_id, case_data), daemon=True).start()

            replies.append({
                "role": "assistant",
                "text": f"Mission `{mission_id}` started. Running Phase 1: Intelligence Gathering…",
                "mission_id": mission_id,
            })
        else:
            replies.append({"role": "assistant", "text": "No problem — type **yes** when ready, or tell me what to change."})

    elif step == "running":
        replies.append({"role": "assistant", "text": "The mission is still running. I'll update you when it finishes."})

    return jsonify({"messages": replies})


@app.route("/api/mission/<mission_id>")
def mission_status(mission_id):
    with _lock:
        mission = dict(_missions.get(mission_id) or {})
    if not mission:
        return jsonify({"error": "not found"}), 404
    return app.response_class(json.dumps(mission, default=str), mimetype="application/json")


# ── Mission runner ────────────────────────────────────────────────────────────

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
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, port=port)

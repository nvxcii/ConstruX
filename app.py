"""
ConstruX — Multi-AI Mission Dashboard
"""
import json
import os
import sqlite3
import sys
import threading
import uuid
from datetime import datetime

import flask
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "construx-dev-key")
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
DB_PATH    = os.path.join(os.path.dirname(__file__), "construx.db")
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXT = {
    ".pdf", ".txt", ".md", ".csv", ".rtf",
    ".docx", ".doc",
    ".png", ".jpg", ".jpeg", ".gif", ".webp",
}

_lock    = threading.Lock()
_missions: dict = {}

STEPS = [
    ("description", "What's the situation? Describe the case you want analyzed."),
    ("employer",    "What's the name of the employer or organization involved?"),
    ("client",      "What's the client's name?"),
    ("violations",  "What violations or issues should we focus on? (comma-separated)"),
]


# ── Database ──────────────────────────────────────────────────────────────────

def _db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def _db_init():
    with _db() as c:
        c.execute('''CREATE TABLE IF NOT EXISTS missions (
            id               TEXT PRIMARY KEY,
            name             TEXT,
            case_id          TEXT,
            client_name      TEXT,
            employer_name    TEXT,
            violations       TEXT,
            status           TEXT DEFAULT "running",
            created_at       TEXT,
            completed_at     TEXT,
            leverage_score   REAL,
            risk_to_opponent TEXT,
            settlement_low   REAL,
            settlement_mid   REAL,
            settlement_high  REAL,
            recommended_demand REAL,
            settlement_floor REAL,
            total_complaints INTEGER,
            media_approach   TEXT,
            result_json      TEXT,
            error_text       TEXT,
            attached_files   TEXT
        )''')
        c.commit()

_db_init()

def _db_save_start(mid: str, case_data: dict):
    with _db() as c:
        c.execute(
            '''INSERT OR IGNORE INTO missions
               (id,name,case_id,client_name,employer_name,violations,status,created_at,attached_files)
               VALUES (?,?,?,?,?,?,"running",?,?)''',
            (mid,
             case_data.get("mission_name",""),
             case_data.get("case_id",""),
             case_data.get("client_name",""),
             case_data.get("employer_name",""),
             ", ".join(case_data.get("violations",[])),
             datetime.utcnow().isoformat(sep=" ", timespec="seconds"),
             json.dumps(case_data.get("attached_files",[])))
        )
        c.commit()

def _db_save_complete(mid: str, result: dict):
    s  = result.get("strategic_analysis", {})
    lv = s.get("leverage_analysis", {})
    st = s.get("settlement_prediction", {})
    rg = st.get("predicted_range", {})
    ex = result.get("execution_plan", {})
    dp = ex.get("deployment_summary", {})
    with _db() as c:
        c.execute(
            '''UPDATE missions SET
               status="complete", completed_at=?,
               leverage_score=?, risk_to_opponent=?,
               settlement_low=?, settlement_mid=?, settlement_high=?,
               recommended_demand=?, settlement_floor=?,
               total_complaints=?, media_approach=?, result_json=?
               WHERE id=?''',
            (datetime.utcnow().isoformat(sep=" ", timespec="seconds"),
             lv.get("overall_leverage_score"), lv.get("risk_to_opponent"),
             rg.get("low"), rg.get("mid"), rg.get("high"),
             st.get("recommended_demand"), st.get("recommended_floor"),
             dp.get("total_complaints"), dp.get("media_approach"),
             json.dumps(result, default=str), mid)
        )
        c.commit()

def _db_save_error(mid: str, error: str):
    with _db() as c:
        c.execute(
            'UPDATE missions SET status="error",completed_at=?,error_text=? WHERE id=?',
            (datetime.utcnow().isoformat(sep=" ", timespec="seconds"), error, mid)
        )
        c.commit()


# ── File helpers ──────────────────────────────────────────────────────────────

def _ext(f): return os.path.splitext(f)[1].lower()

def _extract_text(path: str, filename: str):
    e = _ext(filename)
    try:
        if e in (".txt",".md",".csv",".rtf"):
            return open(path, "r", errors="replace").read(400_000)
        if e == ".pdf":
            try:
                from pypdf import PdfReader
            except ImportError:
                from PyPDF2 import PdfReader
            return "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)[:400_000]
        if e in (".docx",".doc"):
            import docx
            return "\n".join(p.text for p in docx.Document(path).paragraphs)[:400_000]
    except Exception as ex:
        return f"[Could not read: {ex}]"
    return None


# ── Template helpers ──────────────────────────────────────────────────────────

@app.template_filter("usd")
def usd(v):
    try:
        return f"${int(v):,}"
    except (TypeError, ValueError):
        return "N/A"

@app.template_filter("shortdate")
def shortdate(v):
    if not v:
        return "—"
    try:
        return datetime.fromisoformat(str(v)).strftime("%b %d, %Y")
    except Exception:
        return str(v)[:10]


# ── Dashboard ─────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    with _db() as c:
        stats = c.execute('''SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN status="complete" THEN 1 ELSE 0 END) AS completed,
            SUM(CASE WHEN status="running"  THEN 1 ELSE 0 END) AS running,
            SUM(CASE WHEN status="error"    THEN 1 ELSE 0 END) AS errors,
            ROUND(AVG(CASE WHEN status="complete" THEN leverage_score END),1) AS avg_leverage,
            SUM(CASE WHEN status="complete" THEN COALESCE(recommended_demand,0) END) AS total_demand
            FROM missions''').fetchone()
        recent = c.execute('''SELECT id,name,status,leverage_score,
            settlement_mid,recommended_demand,created_at
            FROM missions ORDER BY created_at DESC LIMIT 6''').fetchall()
    return render_template("dashboard.html", stats=stats, recent=recent)


# ── History ───────────────────────────────────────────────────────────────────

@app.route("/history")
def history():
    with _db() as c:
        missions = c.execute('''SELECT id,name,client_name,employer_name,status,
            leverage_score,recommended_demand,total_complaints,created_at,completed_at
            FROM missions ORDER BY created_at DESC''').fetchall()
    return render_template("history.html", missions=missions)


# ── Mission detail + export ───────────────────────────────────────────────────

@app.route("/mission/new")
def new_mission():
    session.clear()
    return render_template("chat.html")

@app.route("/mission/<mid>")
def mission_detail(mid):
    with _db() as c:
        m = c.execute("SELECT * FROM missions WHERE id=?", (mid,)).fetchone()
    if not m:
        return "Mission not found", 404
    result = json.loads(m["result_json"]) if m["result_json"] else {}
    files  = json.loads(m["attached_files"]) if m["attached_files"] else []
    return render_template("mission_detail.html", m=m, result=result, files=files)

@app.route("/mission/<mid>/export.json")
def export_mission(mid):
    with _db() as c:
        row = c.execute("SELECT result_json, name FROM missions WHERE id=?", (mid,)).fetchone()
    if not row or not row["result_json"]:
        return "No results available", 404
    return app.response_class(
        row["result_json"], mimetype="application/json",
        headers={"Content-Disposition": f'attachment; filename="mission-{mid}.json"'}
    )


# ── Settings ──────────────────────────────────────────────────────────────────

@app.route("/settings")
def settings():
    keys = ["ANTHROPIC_API_KEY","GOOGLE_API_KEY","OPENAI_API_KEY","DEEPSEEK_API_KEY"]
    api_status = {k: bool(os.environ.get(k)) for k in keys}
    sys_info = {
        "Python":  sys.version.split()[0],
        "Flask":   flask.__version__,
        "Database": DB_PATH,
        "Uploads":  UPLOAD_DIR,
    }
    return render_template("settings.html", api_status=api_status, sys_info=sys_info)


# ── Chat API ──────────────────────────────────────────────────────────────────

@app.route("/api/start", methods=["POST"])
def start():
    session["step"]    = 0
    session["answers"] = {}
    session["uploads"] = []
    return jsonify({"messages": [{"role": "assistant", "text": (
        "Welcome to the Λ Mission Interface. I'll guide you through a live "
        "3-phase analysis across Claude, Gemini, DeepSeek, and ChatGPT.\n\n"
        "Attach supporting documents or media at any time using the button below.\n\n"
        + STEPS[0][1]
    )}]})

@app.route("/api/upload", methods=["POST"])
def upload():
    f = request.files.get("file")
    if not f or not f.filename:
        return jsonify({"error": "No file provided"}), 400
    e = _ext(f.filename)
    if e not in ALLOWED_EXT:
        return jsonify({"error": f"File type '{e}' not supported"}), 400
    uploads = session.get("uploads", [])
    if len(uploads) >= 10:
        return jsonify({"error": "Maximum 10 files per session"}), 400
    safe   = secure_filename(f.filename)
    stored = f"{uuid.uuid4().hex[:8]}_{safe}"
    path   = os.path.join(UPLOAD_DIR, stored)
    f.save(path)
    is_img = e in (".png",".jpg",".jpeg",".gif",".webp")
    entry  = {"name": safe, "stored": stored, "size": os.path.getsize(path), "is_image": is_img}
    uploads.append(entry)
    session["uploads"] = uploads
    session.modified = True
    return jsonify({"name": safe, "size": entry["size"], "is_image": is_img, "index": len(uploads)-1})

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
        nxt = step + 1
        if nxt < len(STEPS):
            session["step"] = nxt
            replies.append({"role": "assistant", "text": STEPS[nxt][1]})
        else:
            session["step"] = "confirm"
            uploads = session.get("uploads", [])
            n = len(uploads)
            doc_note = f"\n**Attached:** {n} file{'s' if n!=1 else ''}" if n else ""
            replies.append({"role": "assistant", "text": (
                "Here's what I have:\n\n"
                f"**Situation:** {answers['description']}\n"
                f"**Employer:** {answers['employer']}\n"
                f"**Client:** {answers['client']}\n"
                f"**Issues:** {answers['violations']}"
                f"{doc_note}\n\n"
                "Ready to run the live 3-phase analysis? Type **yes** to proceed."
            )})

    elif step == "confirm":
        if text.lower() in ("yes","y","run","go","proceed","start"):
            mid = uuid.uuid4().hex[:8]
            session["mission_id"] = mid
            session["step"] = "running"

            uploads = session.get("uploads", [])
            doc_texts = []
            for u in uploads:
                if not u["is_image"]:
                    t = _extract_text(os.path.join(UPLOAD_DIR, u["stored"]), u["name"])
                    if t:
                        doc_texts.append(f"[{u['name']}]\n{t}")

            situation = answers.get("description","")
            if doc_texts:
                situation += "\n\nSupporting documentation:\n\n" + "\n\n---\n\n".join(doc_texts)

            case_data = {
                "mission_name": f"{answers.get('client','Case')} v. {answers.get('employer','Employer')}",
                "case_id": f"CASE-{mid.upper()}",
                "client_name": answers.get("client",""),
                "employer_name": answers.get("employer",""),
                "situation_description": situation,
                "violations": [v.strip() for v in answers.get("violations","").split(",")],
                "attached_files": [u["name"] for u in uploads],
            }

            with _lock:
                _missions[mid] = {"status":"running","phase":0,"phase_label":"Initializing","result":None,"error":None}

            threading.Thread(target=_run_mission, args=(mid, case_data), daemon=True).start()
            replies.append({
                "role": "assistant",
                "text": f"Mission `{mid}` started. Running Phase 1: Intelligence Gathering…",
                "mission_id": mid,
            })
        else:
            replies.append({"role":"assistant","text":"No problem — type **yes** when ready, or tell me what to change."})

    elif step == "running":
        replies.append({"role":"assistant","text":"Mission is still running. I'll update you when it finishes."})

    return jsonify({"messages": replies})

@app.route("/api/mission/<mid>")
def mission_status(mid):
    with _lock:
        m = dict(_missions.get(mid) or {})
    if not m:
        with _db() as c:
            row = c.execute("SELECT status,result_json,error_text FROM missions WHERE id=?", (mid,)).fetchone()
        if row:
            m = {"status": row["status"],
                 "result": json.loads(row["result_json"] or "null"),
                 "error":  row["error_text"]}
        else:
            return jsonify({"error":"not found"}), 404
    return app.response_class(json.dumps(m, default=str), mimetype="application/json")


# ── Mission runner ────────────────────────────────────────────────────────────

def _run_mission(mid: str, case_data: dict):
    def upd(**kw):
        with _lock:
            _missions[mid].update(kw)

    _db_save_start(mid, case_data)
    try:
        from multi_ai_framework.missions.mission_orchestrator import MissionOrchestrator
        from multi_ai_framework.config.config_manager import ConfigManager

        orch = MissionOrchestrator(ConfigManager())

        upd(phase=1, phase_label="Intelligence Gathering")
        intel = orch.execute_intelligence_only(case_data)

        upd(phase=2, phase_label="Strategic Analysis")
        analysis = orch.execute_analysis_only(case_data, intel)

        upd(phase=3, phase_label="Execution Planning")
        execution = orch.execute_execution_only(case_data, analysis, intel)

        result = {"intelligence": intel, "strategic_analysis": analysis, "execution_plan": execution}
        upd(status="complete", result=result)
        _db_save_complete(mid, result)

    except Exception as exc:
        import traceback
        err = str(exc)
        upd(status="error", error=err, traceback=traceback.format_exc())
        _db_save_error(mid, err)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, port=port)

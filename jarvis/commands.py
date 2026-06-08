"""
Jarvis command handlers — dispatch, report, status, cases, output
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

REPO_ROOT = Path(__file__).parent.parent
MISSIONS_DIR = REPO_ROOT / "multi_ai_framework" / "missions"
OUTPUT_DIR = REPO_ROOT / "output"

# Map short names → mission directories
CASE_ALIASES = {
    "kyle":    "kyle_theus_dispatch",
    "theus":   "kyle_theus_dispatch",
    "26stud":  "kyle_theus_dispatch",
}


def _resolve_case(name: Optional[str]) -> Optional[Path]:
    """Return mission directory path for a case alias or directory name."""
    if not name:
        # Default to first available mission
        missions = [d for d in MISSIONS_DIR.iterdir() if d.is_dir() and not d.name.startswith("_")]
        return missions[0] if missions else None

    key = name.lower().replace("-", "_")
    alias = CASE_ALIASES.get(key)
    if alias:
        return MISSIONS_DIR / alias

    # Try direct match
    candidate = MISSIONS_DIR / key
    if candidate.is_dir():
        return candidate

    return None


def _load_config(mission_dir: Path) -> Optional[dict]:
    cfg = mission_dir / "case_config.json"
    if cfg.exists():
        return json.loads(cfg.read_text())
    return None


def cmd_dispatch(console: Console, args: list):
    mission_dir = _resolve_case(args[0] if args else None)
    if not mission_dir:
        console.print("[red]Case not found. Run [bold]cases[/bold] to list available cases.[/red]")
        return

    script = mission_dir / "generate_dispatch.py"
    if not script.exists():
        console.print(f"[red]No generate_dispatch.py in {mission_dir.name}[/red]")
        return

    console.print(f"[bold blue]▶ Generating CoworkDispatch for [cyan]{mission_dir.name}[/cyan]...[/bold blue]")
    console.print()

    with Progress(
        SpinnerColumn(style="blue"),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Running dispatch generator...", total=None)
        result = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True,
            text=True,
            cwd=str(mission_dir),
        )

    if result.returncode == 0:
        console.print(result.stdout)
        _show_output_files(console, ["COWORK_DISPATCH.txt", "cowork_dispatch.json"])
    else:
        console.print(f"[red]Error:[/red]\n{result.stderr}")


def cmd_report(console: Console, args: list):
    mission_dir = _resolve_case(args[0] if args else None)
    if not mission_dir:
        console.print("[red]Case not found. Run [bold]cases[/bold] to list available cases.[/red]")
        return

    script = mission_dir / "generate_case_report.py"
    if not script.exists():
        console.print(f"[red]No generate_case_report.py in {mission_dir.name}[/red]")
        return

    console.print(f"[bold blue]▶ Generating PDF Report for [cyan]{mission_dir.name}[/cyan]...[/bold blue]")
    console.print()

    with Progress(
        SpinnerColumn(style="blue"),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Building PDF with ReportLab...", total=None)
        result = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True,
            text=True,
            cwd=str(mission_dir),
        )

    if result.returncode == 0:
        console.print(result.stdout)
        pdfs = list(OUTPUT_DIR.glob("*.pdf"))
        if pdfs:
            latest = max(pdfs, key=lambda f: f.stat().st_mtime)
            size_kb = latest.stat().st_size / 1024
            console.print(Panel(
                f"[bold green]✓  {latest.name}[/bold green]  [dim]({size_kb:.1f} KB)[/dim]\n"
                f"[dim]{latest}[/dim]",
                title="PDF Ready",
                border_style="green",
                box=box.ROUNDED,
            ))
    else:
        console.print(f"[red]Error:[/red]\n{result.stderr}")


def cmd_status(console: Console, args: list):
    mission_dir = _resolve_case(args[0] if args else None)
    if not mission_dir:
        console.print("[red]Case not found.[/red]")
        return

    cfg = _load_config(mission_dir)
    if not cfg:
        console.print(f"[red]No case_config.json in {mission_dir}[/red]")
        return

    _render_case_status(console, cfg)


def _render_case_status(console: Console, cfg: dict):
    field = cfg.get("field_state", "UNKNOWN")
    matters = cfg.get("matters", [])

    # Pull identity from first matter's case_identity block
    identity = matters[0].get("case_identity", {}) if matters else {}

    header_text = (
        f"[bold white]{identity.get('defendant', cfg.get('case_name', 'Unknown'))}[/bold white]\n"
        f"[cyan]{identity.get('case_number', cfg.get('case_id', ''))}[/cyan]  ·  "
        f"[dim]{identity.get('court', '')}[/dim]\n"
        f"[dim]Judgment: {identity.get('judgment_entered', 'N/A')}  ·  "
        f"Writ: {identity.get('writ_issued', 'N/A')}[/dim]"
    )
    console.print(Panel(header_text, title="[bold blue]Case Identity[/bold blue]",
                        border_style="blue", box=box.ROUNDED))
    console.print()

    console.print(f"[bold]Field State:[/bold] [yellow]{field}[/yellow]")
    console.print()

    # Matters summary table
    if matters:
        tbl = Table(title="Active Matters", box=box.ROUNDED, border_style="blue",
                    header_style="bold cyan", title_style="bold white")
        tbl.add_column("ID", style="bold yellow", width=12)
        tbl.add_column("Title", style="white")
        tbl.add_column("Urgency", style="red", width=12)
        tbl.add_column("Evidence", style="cyan", justify="right", width=10)
        tbl.add_column("Defects", style="red", justify="right", width=8)

        for m in matters:
            urgency = m.get("urgency", "")
            color = "red" if urgency == "IMMEDIATE" else "yellow" if urgency == "HIGH" else "green"
            tbl.add_row(
                m.get("matter_id", ""),
                m.get("title", ""),
                f"[{color}]{urgency}[/{color}]",
                str(len(m.get("evidence_layers", []))),
                str(len(m.get("legal_defects", []))),
            )
        console.print(tbl)
        console.print()

    # Task priorities
    tasks = cfg.get("task_priorities", [])
    if tasks:
        tbl2 = Table(title="Task Queue", box=box.ROUNDED, border_style="yellow",
                     header_style="bold cyan", title_style="bold white")
        tbl2.add_column("P#", style="bold yellow", width=4)
        tbl2.add_column("Matter", style="cyan", width=10)
        tbl2.add_column("Title", style="white")
        tbl2.add_column("Urgency", style="red", width=12)

        for t in tasks:
            urgency = t.get("urgency", "")
            color = "red" if urgency == "IMMEDIATE" else "yellow" if urgency in ("HIGH", "URGENT") else "green"
            tbl2.add_row(
                str(t.get("priority_number", "")),
                t.get("matter", ""),
                t.get("title", ""),
                f"[{color}]{urgency}[/{color}]",
            )
        console.print(tbl2)
        console.print()

    # Critical docs
    docs = cfg.get("critical_documents", [])
    console.print(
        f"[bold]Critical Documents:[/bold] [dim]{len(docs)} on record[/dim]"
    )
    console.print()


def cmd_cases(console: Console, _args):
    if not MISSIONS_DIR.exists():
        console.print("[red]missions/ directory not found[/red]")
        return

    dirs = [d for d in MISSIONS_DIR.iterdir() if d.is_dir() and not d.name.startswith("_")]
    if not dirs:
        console.print("[yellow]No case missions found.[/yellow]")
        return

    tbl = Table(title="Available Cases", box=box.ROUNDED, border_style="blue",
                header_style="bold cyan", title_style="bold white")
    tbl.add_column("Directory", style="bold yellow")
    tbl.add_column("Config", style="cyan")
    tbl.add_column("Aliases", style="dim")

    reverse_aliases: dict[str, list] = {}
    for alias, mission in CASE_ALIASES.items():
        reverse_aliases.setdefault(mission, []).append(alias)

    for d in sorted(dirs):
        has_cfg = "✓" if (d / "case_config.json").exists() else "✗"
        aliases = ", ".join(reverse_aliases.get(d.name, []))
        tbl.add_row(d.name, has_cfg, aliases or "—")

    console.print(tbl)
    console.print()


def cmd_output(console: Console, _args):
    if not OUTPUT_DIR.exists():
        console.print("[yellow]output/ directory is empty or does not exist.[/yellow]")
        return

    files = sorted(OUTPUT_DIR.iterdir(), key=lambda f: f.stat().st_mtime, reverse=True)
    if not files:
        console.print("[yellow]No files in output/[/yellow]")
        return

    tbl = Table(title="Output Files", box=box.ROUNDED, border_style="blue",
                header_style="bold cyan", title_style="bold white")
    tbl.add_column("File", style="bold white")
    tbl.add_column("Size", style="cyan", justify="right")
    tbl.add_column("Modified", style="dim")

    import datetime
    for f in files:
        if f.is_file():
            size = f.stat().st_size
            size_str = f"{size / 1024:.1f} KB" if size > 1024 else f"{size} B"
            mtime = datetime.datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            tbl.add_row(f.name, size_str, mtime)

    console.print(tbl)
    console.print()


def cmd_open(console: Console, args: list):
    if not args:
        console.print("[yellow]Usage: open <filename>[/yellow]")
        return

    target = OUTPUT_DIR / args[0]
    if not target.exists():
        # Try partial match
        matches = list(OUTPUT_DIR.glob(f"*{args[0]}*"))
        if not matches:
            console.print(f"[red]File not found: {args[0]}[/red]")
            return
        target = matches[0]

    console.print(f"[dim]Opening {target}...[/dim]")
    try:
        if sys.platform == "darwin":
            subprocess.Popen(["open", str(target)])
        elif sys.platform == "win32":
            os.startfile(str(target))
        else:
            subprocess.Popen(["xdg-open", str(target)])
    except Exception as e:
        console.print(f"[red]Could not open file: {e}[/red]")


def cmd_dashboard(console: Console, _args):
    dashboard = REPO_ROOT / "legal-dashboard.html"
    if not dashboard.exists():
        console.print("[red]legal-dashboard.html not found[/red]")
        return

    console.print(f"[dim]Opening dashboard: {dashboard}[/dim]")
    try:
        if sys.platform == "darwin":
            subprocess.Popen(["open", str(dashboard)])
        elif sys.platform == "win32":
            os.startfile(str(dashboard))
        else:
            subprocess.Popen(["xdg-open", str(dashboard)])
        console.print("[green]✓ Dashboard opened in browser[/green]")
    except Exception as e:
        console.print(f"[red]Could not open dashboard: {e}[/red]")


def _show_output_files(console: Console, filenames: list):
    for name in filenames:
        path = OUTPUT_DIR / name
        if path.exists():
            size_kb = path.stat().st_size / 1024
            console.print(f"  [green]✓[/green]  [bold]{name}[/bold]  [dim]({size_kb:.1f} KB)[/dim]")

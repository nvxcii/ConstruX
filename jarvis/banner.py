"""Jarvis banner and splash screen"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box

BANNER_ART = r"""
   ██████╗ ██████╗ ███╗   ██╗███████╗████████╗██████╗ ██╗   ██╗██╗  ██╗
  ██╔════╝██╔═══██╗████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║   ██║╚██╗██╔╝
  ██║     ██║   ██║██╔██╗ ██║███████╗   ██║   ██████╔╝██║   ██║ ╚███╔╝
  ██║     ██║   ██║██║╚██╗██║╚════██║   ██║   ██╔══██╗██║   ██║ ██╔██╗
  ╚██████╗╚██████╔╝██║ ╚████║███████║   ██║   ██║  ██║╚██████╔╝██╔╝ ██╗
   ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝
"""

JARVIS_ART = r"""
     ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗
     ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝
     ██║███████║██████╔╝██║   ██║██║███████╗
██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║
╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║
 ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝
"""


def print_splash(console: Console, version: str = "1.0.0"):
    console.print()

    title = Text(JARVIS_ART, style="bold blue")
    console.print(Align.center(title))

    subtitle = Text("Multi-AI Justice League Framework  ·  Command Interface", style="dim cyan")
    console.print(Align.center(subtitle))
    console.print(Align.center(Text(f"v{version}  ·  Justice Engine", style="dim")))
    console.print()

    panel = Panel(
        Align.center(
            Text(
                "⚡  Dispatch  ·  PDF Reports  ·  Case Intelligence  ·  Settlement Strategy",
                style="bold white"
            )
        ),
        border_style="blue",
        box=box.ROUNDED,
    )
    console.print(panel)
    console.print()


def print_help(console: Console):
    from rich.table import Table

    table = Table(
        title="Available Commands",
        box=box.ROUNDED,
        border_style="blue",
        show_header=True,
        header_style="bold cyan",
        title_style="bold white",
    )
    table.add_column("Command", style="bold yellow", width=22)
    table.add_column("Description", style="white")
    table.add_column("Example", style="dim")

    commands = [
        ("dispatch [case]",    "Generate CoworkDispatch handoff document",   "dispatch kyle"),
        ("report [case]",      "Generate PDF case status report",            "report kyle"),
        ("status [case]",      "Show case summary in terminal",              "status kyle"),
        ("cases",              "List all available case configs",            "cases"),
        ("output",             "List files in the output directory",         "output"),
        ("open [file]",        "Open output file with system viewer",        "open report.pdf"),
        ("dashboard",          "Open legal dashboard in browser",            "dashboard"),
        ("help",               "Show this help screen",                      "help"),
        ("clear",              "Clear the terminal",                         "clear"),
        ("exit / quit",        "Exit Jarvis",                                "exit"),
    ]

    for cmd, desc, ex in commands:
        table.add_row(cmd, desc, ex)

    console.print(table)
    console.print()

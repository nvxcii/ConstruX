"""
Jarvis interactive REPL shell
"""

import os
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.styles import Style

from .banner import print_splash, print_help
from .commands import (
    cmd_dispatch,
    cmd_report,
    cmd_status,
    cmd_cases,
    cmd_output,
    cmd_open,
    cmd_dashboard,
)
from . import __version__

PROMPT_STYLE = Style.from_dict({
    "prompt": "bold ansicyan",
})

DISPATCH_MAP = {
    "dispatch":  cmd_dispatch,
    "report":    cmd_report,
    "status":    cmd_status,
    "cases":     cmd_cases,
    "output":    cmd_output,
    "open":      cmd_open,
    "dashboard": cmd_dashboard,
}


def run_shell(console: Console):
    print_splash(console, __version__)
    console.print("[dim]Type [bold]help[/bold] for commands, [bold]exit[/bold] to quit.[/dim]")
    console.print()

    session: PromptSession = PromptSession(
        history=InMemoryHistory(),
        auto_suggest=AutoSuggestFromHistory(),
        style=PROMPT_STYLE,
    )

    while True:
        try:
            raw = session.prompt(
                [("class:prompt", "jarvis ❯ ")],
            ).strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Exiting Jarvis.[/dim]")
            break

        if not raw:
            continue

        parts = raw.split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd in ("exit", "quit", "q"):
            console.print("[dim]Goodbye.[/dim]")
            break

        elif cmd == "help":
            print_help(console)

        elif cmd == "clear":
            os.system("clear")
            print_splash(console, __version__)

        elif cmd in DISPATCH_MAP:
            DISPATCH_MAP[cmd](console, args)

        else:
            console.print(
                f"[yellow]Unknown command:[/yellow] [bold]{cmd}[/bold]  "
                f"[dim](type [bold]help[/bold] for a list)[/dim]"
            )

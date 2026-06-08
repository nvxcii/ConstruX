"""
python -m jarvis  — entry point
"""

import argparse
import sys
from rich.console import Console

from . import __version__
from .shell import run_shell
from .commands import cmd_dispatch, cmd_report, cmd_status, cmd_cases, cmd_output


def main():
    parser = argparse.ArgumentParser(
        prog="jarvis",
        description="Jarvis — ConstruX Command Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m jarvis                     # start interactive REPL
  python -m jarvis --dispatch kyle     # generate dispatch document
  python -m jarvis --report kyle       # generate PDF report
  python -m jarvis --status kyle       # show case status
  python -m jarvis --cases             # list all cases
        """,
    )
    parser.add_argument("--version", action="version", version=f"Jarvis v{__version__}")
    parser.add_argument("--dispatch", metavar="CASE", help="generate CoworkDispatch for a case")
    parser.add_argument("--report",   metavar="CASE", help="generate PDF report for a case")
    parser.add_argument("--status",   metavar="CASE", help="print case status summary")
    parser.add_argument("--cases",    action="store_true", help="list available case missions")
    parser.add_argument("--output",   action="store_true", help="list output files")

    args = parser.parse_args()
    console = Console()

    # Non-interactive one-shot commands
    if args.dispatch:
        cmd_dispatch(console, [args.dispatch])
        sys.exit(0)
    if args.report:
        cmd_report(console, [args.report])
        sys.exit(0)
    if args.status:
        cmd_status(console, [args.status])
        sys.exit(0)
    if args.cases:
        cmd_cases(console, [])
        sys.exit(0)
    if args.output:
        cmd_output(console, [])
        sys.exit(0)

    # Default: interactive REPL
    run_shell(console)


if __name__ == "__main__":
    main()

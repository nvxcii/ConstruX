"""
Jarvis CLI Entry Point
Run with: python -m jarvis
"""

import argparse
import sys

from jarvis.core.orchestrator import Orchestrator
from jarvis.config.settings import JarvisSettings


def create_orchestrator(settings: JarvisSettings) -> Orchestrator:
    """Build the orchestrator with all enabled tools registered."""
    # Initialize persistent memory and auto-tuner
    from jarvis.memory.persistent_memory import PersistentMemory
    from jarvis.memory.auto_tuner import AutoTuner
    from jarvis.scheduler.task_scheduler import TaskScheduler

    memory = PersistentMemory()
    auto_tuner = AutoTuner(memory)
    scheduler = TaskScheduler()

    orchestrator = Orchestrator(
        api_key=settings.anthropic_api_key,
        model=settings.model,
        max_tokens=settings.max_tokens,
        memory=memory,
        auto_tuner=auto_tuner,
        scheduler=scheduler,
    )

    tools = []

    # Memory tool (always enabled - persistent cross-session memory)
    from jarvis.memory.memory_tool import MemoryTool
    tools.append(MemoryTool(memory=memory))

    # Scheduler tool (always enabled - deferred and recurring tasks)
    from jarvis.scheduler.scheduler_tool import SchedulerTool
    tools.append(SchedulerTool(scheduler=scheduler))

    # macOS tools
    if settings.get("tools", "macos_enabled", True):
        from jarvis.tools.macos.apple_notes import AppleNotesTool
        from jarvis.tools.macos.apple_reminders import AppleRemindersTool
        from jarvis.tools.macos.apple_calendar import AppleCalendarTool
        from jarvis.tools.macos.system_control import SystemControlTool
        from jarvis.tools.macos.finder import FinderTool
        from jarvis.tools.macos.browser import BrowserTool
        tools.extend([
            AppleNotesTool(),
            AppleRemindersTool(),
            AppleCalendarTool(),
            SystemControlTool(),
            FinderTool(),
            BrowserTool(),
        ])

    # Web tools
    if settings.get("tools", "web_enabled", True):
        from jarvis.tools.web.web_search import WebSearchTool
        from jarvis.tools.web.web_fetch import WebFetchTool
        tools.extend([
            WebSearchTool(settings=settings),
            WebFetchTool(),
        ])

    # Code tools
    if settings.get("tools", "code_enabled", True):
        from jarvis.tools.code.codebase_search import CodebaseSearchTool
        tools.append(CodebaseSearchTool())

    # Hivemind (multi-AI)
    if settings.get("tools", "hivemind_enabled", False):
        from jarvis.tools.hivemind.multi_agent import HivemindTool
        tools.append(HivemindTool(settings=settings))

    # Smart home
    if settings.get("tools", "smart_home_enabled", False):
        from jarvis.tools.smart_home.homekit import SmartHomeTool
        tools.append(SmartHomeTool(settings=settings))

    orchestrator.register_tools(tools)
    return orchestrator


def run_text_mode(orchestrator: Orchestrator, name: str) -> None:
    """Run Jarvis in interactive text mode (REPL)."""
    print(f"\n{'='*60}")
    print(f"  {name} - AI Assistant")
    print(f"  Type 'quit' to exit | 'reset' to clear conversation")
    print(f"  Tools loaded: {orchestrator.registry.tool_count}")
    print(f"{'='*60}\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n\nGoodbye, sir.")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "bye"):
            print(f"\n{name}: Goodbye, sir.")
            break
        if user_input.lower() == "reset":
            orchestrator.reset_conversation()
            print(f"{name}: Conversation cleared.\n")
            continue

        try:
            response = orchestrator.process(user_input)
            print(f"\n{name}: {response}\n")
        except Exception as e:
            print(f"\n{name}: I encountered an error: {e}\n")


def run_voice_mode(orchestrator: Orchestrator, settings: JarvisSettings) -> None:
    """Run Jarvis with voice input/output."""
    from jarvis.voice.voice_engine import VoiceEngine

    name = settings.assistant_name
    engine = VoiceEngine(settings=settings)

    print(f"\n{'='*60}")
    print(f"  {name} - Voice Mode")
    print(f"  Wake word: '{settings.get('assistant', 'wake_word', 'hey jarvis')}'")
    print(f"  Tools loaded: {orchestrator.registry.tool_count}")
    print(f"{'='*60}\n")

    engine.run(orchestrator)


def main():
    parser = argparse.ArgumentParser(description="Jarvis - macOS AI Assistant")
    parser.add_argument("--voice", action="store_true", help="Start in voice mode")
    parser.add_argument("--config", default=None, help="Path to config file")
    parser.add_argument("--model", default=None, help="Override Claude model")
    parser.add_argument("--list-tools", action="store_true", help="List available tools")
    args = parser.parse_args()

    settings = JarvisSettings(config_path=args.config)
    if args.model:
        settings.set("assistant", "model", args.model)

    orchestrator = create_orchestrator(settings)

    if args.list_tools:
        print("Available tools:")
        for name in orchestrator.registry.tool_names:
            print(f"  - {name}")
        return

    # Start the background scheduler (executes deferred/recurring tasks)
    def _scheduler_handler(action, arguments):
        """Handle scheduled task execution via the orchestrator."""
        if action == "notify":
            msg = arguments.get("message", "Scheduled task triggered.")
            print(f"\n[Scheduled] {msg}")
            return msg
        return orchestrator.registry.execute(action, **arguments)

    if orchestrator.scheduler:
        orchestrator.scheduler.start(_scheduler_handler)

    try:
        if args.voice:
            run_voice_mode(orchestrator, settings)
        else:
            run_text_mode(orchestrator, settings.assistant_name)
    finally:
        if orchestrator.scheduler:
            orchestrator.scheduler.stop()
        if orchestrator.memory:
            orchestrator.memory.close()


if __name__ == "__main__":
    main()

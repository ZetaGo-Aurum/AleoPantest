"""Modern TUI for AloPantest V3.0 using Textual"""
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Button, ListItem, ListView, Label, Input, DataTable
from textual.screen import Screen
from textual.binding import Binding
from textual import on

import time
import threading
from datetime import timedelta
from typing import Dict, Any, List, Optional

from .core.platform import PlatformDetector
from .core.session import SessionManager
from .core.automation import AutomationEngine, ContextDetector
from .cli import TOOLS_BY_CATEGORY, TOOLS_REGISTRY

class ToolExecutionScreen(Screen):
    """Screen for tool execution and results"""
    
    def __init__(self, tool_id: str):
        super().__init__()
        self.tool_id = tool_id
        self.tool_instance = TOOLS_REGISTRY[tool_id]()
        self.automation_engine = AutomationEngine()
        
    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="execution-container"):
            yield Label(f"[bold cyan]Tool:[/bold cyan] {self.tool_instance.metadata.name}", id="tool-title")
            yield Label(f"[dim]{self.tool_instance.metadata.description}[/dim]", id="tool-desc")
            
            with Container(id="input-area"):
                yield Label("Target (URL/IP/Domain):", id="input-label")
                yield Input(placeholder="e.g., example.com or 8.8.8.8", id="target-input")
                yield Button("Launch Automatically", variant="primary", id="launch-btn")
            
            yield Static("Results will appear below...", id="results-display")
        yield Footer()

    @on(Button.Pressed, "#launch-btn")
    def handle_launch(self) -> None:
        target = self.query_one("#target-input", Input).value
        if not target:
            self.query_one("#results-display", Static).update("[red]Please enter a target![/red]")
            return
            
        params = self.automation_engine.auto_fill_params(self.tool_id, target)
        self.query_one("#results-display", Static).update(f"[yellow]Launching {self.tool_id} against {target}...[/yellow]\n[dim]Params: {params}[/dim]")
        
        # Run tool in background
        def run_tool():
            try:
                result = self.tool_instance.run(**params)
                self.app.call_from_thread(self.update_results, result)
            except Exception as e:
                self.app.call_from_thread(self.update_results, {"error": str(e)})

        threading.Thread(target=run_tool, daemon=True).start()

    def update_results(self, result: Any) -> None:
        import json
        formatted = json.dumps(result, indent=2) if isinstance(result, (dict, list)) else str(result)
        self.query_one("#results-display", Static).update(f"[green]✓ Execution Complete[/green]\n\n{formatted}")

class Dashboard(Screen):
    """Main Dashboard with animations and navigation"""
    
    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Label("[bold]Categories[/bold]", id="sidebar-title")
                with ListView(id="category-list"):
                    for category in TOOLS_BY_CATEGORY.keys():
                        yield ListItem(Label(category), id=f"cat-{category.lower()}")
            
            with Vertical(id="main-content"):
                yield Label("[bold cyan]Welcome to AloPantest V3.0[/bold cyan]", id="welcome-msg")
                yield Label(f"Platform: [green]{PlatformDetector.get_platform_name()}[/green]", id="platform-info")
                yield Label("Select a category to view tools", id="instruction")
                with ListView(id="tool-list"):
                    yield ListItem(Label("Select a category first..."))
                    
        yield Static(id="status-bar")
        yield Footer()

    def on_mount(self) -> None:
        self.update_status()
        self.set_interval(1.0, self.update_status)

    def update_status(self) -> None:
        session = self.app.session_manager.get_status()
        color = "green" if session['is_active'] else "red"
        status_text = (
            f"Session: {session['session_id']} | "
            f"Elapsed: {session['elapsed_formatted']} | "
            f"[{color}]Remaining: {session['remaining_formatted']}[/{color}]"
        )
        self.query_one("#status-bar", Static).update(status_text)
        
        if not session['is_active']:
            self.app.notify("Session quota reached! Please restart.", severity="error")

    @on(ListView.Selected, "#category-list")
    def change_category(self, event: ListView.Selected) -> None:
        cat_id = event.item.id.replace("cat-", "").capitalize()
        tools = TOOLS_BY_CATEGORY.get(cat_id, [])
        
        tool_list = self.query_one("#tool-list", ListView)
        tool_list.clear()
        for tool_id in tools:
            tool_list.append(ListItem(Label(tool_id), id=f"tool-{tool_id}"))
        
        self.query_one("#instruction", Label).update(f"Tools in [cyan]{cat_id}[/cyan]:")

    @on(ListView.Selected, "#tool-list")
    def select_tool(self, event: ListView.Selected) -> None:
        tool_id = event.item.id.replace("tool-", "")
        self.app.push_screen(ToolExecutionScreen(tool_id))

class AloPantestTUI(App):
    """Main Textual Application for AloPantest V3.0"""
    
    CSS = """
    Screen {
        background: #121212;
    }
    #sidebar {
        width: 25%;
        border-right: solid $accent;
        padding: 1;
    }
    #sidebar-title {
        text-align: center;
        padding: 1;
        background: $accent;
        color: white;
    }
    #main-content {
        width: 75%;
        padding: 2;
    }
    #welcome-msg {
        text-style: bold;
        margin-bottom: 1;
    }
    #status-bar {
        dock: bottom;
        height: 1;
        background: $surface;
        color: $text;
        text-align: center;
    }
    #execution-container {
        padding: 2;
    }
    #tool-title {
        text-style: bold;
        color: $accent;
    }
    #input-area {
        margin: 2 0;
        border: tall $accent;
        padding: 1;
        height: auto;
    }
    #results-display {
        background: #000;
        color: #0f0;
        padding: 1;
        border: solid #333;
        height: 1fr;
        overflow-y: scroll;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("escape", "back", "Back"),
        Binding("d", "toggle_dark", "Toggle Dark Mode"),
    ]

    def __init__(self):
        super().__init__()
        self.session_manager = SessionManager()
        
    def on_mount(self) -> None:
        self.push_screen(Dashboard())

    def action_back(self) -> None:
        if len(self.screen_stack) > 1:
            self.pop_screen()

if __name__ == "__main__":
    app = AloPantestTUI()
    app.run()

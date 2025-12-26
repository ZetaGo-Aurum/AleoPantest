"""Modern TUI for AleoPantest V3.0 using Textual"""
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
                yield Label("[bold cyan]Welcome to AleoPantest V3.0[/bold cyan]", id="welcome-msg")
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
        
        new_items = [ListItem(Label(tool_id), id=f"tool-{tool_id}") for tool_id in tools]
        if new_items:
            tool_list.mount(*new_items)
        
        self.query_one("#instruction", Label).update(f"Tools in [cyan]{cat_id}[/cyan]:")

    @on(ListView.Selected, "#tool-list")
    def select_tool(self, event: ListView.Selected) -> None:
        tool_id = event.item.id.replace("tool-", "")
        self.app.push_screen(ToolExecutionScreen(tool_id))

class AleoPantestTUI(App):
    """Main Textual Application for AleoPantest V3.0"""
    
    CSS = """
    Screen {
        background: #0a0a0a;
        color: #e0e0e0;
    }

    Header {
        background: #1a1a1a;
        color: #00ffff;
        text-style: bold;
        border-bottom: double #00ffff;
    }

    Footer {
        background: #1a1a1a;
        color: #888888;
    }

    #sidebar {
        width: 30;
        background: #121212;
        border-right: solid #333;
        margin: 1 0;
    }

    #sidebar-title {
        text-align: center;
        padding: 1;
        background: #1a1a1a;
        color: #00ffff;
        text-style: bold;
        border-bottom: solid #333;
    }

    ListView {
        background: transparent;
        border: none;
    }

    ListItem {
        padding: 0 1;
        color: #aaaaaa;
    }

    ListItem:hover {
        background: #1e1e1e;
        color: #00ffff;
    }

    ListItem.--highlight {
        background: #00ffff 20%;
        color: #00ffff;
        text-style: bold;
    }

    #main-content {
        width: 1fr;
        padding: 1 2;
    }

    #welcome-msg {
        text-style: bold;
        color: #00ffff;
        margin-bottom: 1;
        content-align: center middle;
    }

    #platform-info {
        background: #1a1a1a;
        padding: 0 1;
        border: solid #333;
        margin-bottom: 1;
    }

    #instruction {
        color: #888;
        margin-bottom: 1;
    }

    #tool-list {
        border: tall #333;
        height: 1fr;
    }

    #status-bar {
        dock: bottom;
        height: 1;
        background: #1a1a1a;
        color: #00ffff;
        text-align: center;
        border-top: solid #333;
    }

    /* Tool Execution Screen */
    #execution-container {
        padding: 1 2;
    }

    #tool-title {
        text-style: bold;
        color: #00ffff;
        border-bottom: solid #00ffff;
        margin-bottom: 1;
    }

    #input-area {
        margin: 1 0;
        border: tall #333;
        padding: 1;
        height: auto;
        background: #121212;
    }

    Input {
        background: #0a0a0a;
        border: solid #333;
        color: #00ffff;
        margin-top: 1;
    }

    Input:focus {
        border: solid #00ffff;
    }

    #launch-btn {
        margin-top: 1;
        width: 100%;
        background: #00ffff 20%;
        color: #00ffff;
        border: tall #00ffff;
    }

    #launch-btn:hover {
        background: #00ffff 40%;
    }

    #results-display {
        background: #050505;
        color: #00ff00;
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
    app = AleoPantestTUI()
    app.run()

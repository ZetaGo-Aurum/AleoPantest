"""Modern TUI for Aleopantest V3.0.0 - by Aleocrophic using Textual"""
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
from .core.base_tool import BaseTool
from .cli import TOOLS_BY_CATEGORY, TOOLS_REGISTRY

class ToolExecutionScreen(Screen):
    """Screen for tool execution and results"""
    
    def __init__(self, tool_id: str):
        super().__init__()
        self.tool_id = tool_id
        if tool_id in TOOLS_REGISTRY:
            self.tool_instance = TOOLS_REGISTRY[tool_id]()
        else:
            raise ValueError(f"Unknown tool ID: {tool_id}")
        self.automation_engine = AutomationEngine()
        
    def compose(self) -> ComposeResult:
        try:
            admin = BaseTool.get_admin_info()
        except:
            admin = {"username": "admin", "hostname": "localhost", "os": "unknown"}
            
        yield Header()
        with Horizontal():
            with Vertical(id="execution-container"):
                yield Label(f"[bold cyan]Tool:[/bold cyan] {self.tool_instance.metadata.name}", id="tool-title")
                yield Label(f"[dim]{self.tool_instance.metadata.description}[/dim]", id="tool-desc")
                yield Label(f"[bold green]Admin:[/bold green] {admin['username']}@{admin['hostname']} ([dim]{admin['os']}[/dim])", id="admin-info-label")
                
                with Container(id="input-area"):
                    yield Label("Target (URL/IP/Domain/Text):", id="input-label")
                    yield Input(placeholder="e.g., example.com, 8.8.8.8, or payload text", id="target-input")
                    with Horizontal(id="action-buttons"):
                        yield Button("Launch Auto", variant="primary", id="launch-btn")
                        yield Button("Clear Results", variant="error", id="clear-btn")
                
                yield Static("Results will appear below...", id="results-display")
            
            with Vertical(id="tool-info-panel"):
                yield Label("[bold cyan]Tool Information[/bold cyan]", id="info-title")
                
                yield Label("[yellow]Description:[/yellow]")
                yield Label(f"{self.tool_instance.metadata.description}", id="tool-desc-full")
                
                yield Label("\n[yellow]Usage Guide:[/yellow]")
                yield Label(f"{self.tool_instance.metadata.usage}", id="usage-info")
                
                if self.tool_instance.metadata.example:
                    yield Label("\n[yellow]Example:[/yellow]")
                    yield Label(f"{self.tool_instance.metadata.example}", id="example-info")
                
                if self.tool_instance.metadata.parameters:
                    yield Label("\n[yellow]Available Parameters:[/yellow]")
                    params_text = ""
                    for k, v in self.tool_instance.metadata.parameters.items():
                        params_text += f"• [b]{k}[/b]: {v}\n"
                    yield Label(params_text.strip(), id="params-info")
                
                yield Label(f"\n[yellow]Risk Level:[/yellow] {self.tool_instance.metadata.risk_level}")
                yield Label(f"[yellow]Category:[/yellow] {self.tool_instance.metadata.category.value}")
                yield Label(f"[yellow]Author:[/yellow] {self.tool_instance.metadata.author}")
        yield Footer()

    @on(Button.Pressed, "#launch-btn")
    def handle_launch(self) -> None:
        target = self.query_one("#target-input", Input).value
        if not target:
            self.query_one("#results-display", Static).update("[bold red]Error: Please enter a target![/bold red]")
            return
            
        params = self.automation_engine.auto_fill_params(self.tool_id, target)
        self.query_one("#results-display", Static).update(f"[bold yellow]🚀 Launching {self.tool_id}...[/bold yellow]\n[dim]Target: {target}[/dim]\n[dim]Detected Params: {params}[/dim]\n\n[cyan]Executing tool logic...[/cyan]")
        
        # Disable button during execution
        btn = self.query_one("#launch-btn", Button)
        btn.disabled = True
        btn.label = "Running..."
        
        # Run tool in background
        def run_tool():
            try:
                result = self.tool_instance.run(**params)
                self.app.call_from_thread(self.update_results, result)
            except Exception as e:
                self.app.call_from_thread(self.update_results, {"error": str(e)})

        threading.Thread(target=run_tool, daemon=True).start()

    @on(Button.Pressed, "#clear-btn")
    def handle_clear(self) -> None:
        self.query_one("#results-display", Static).update("Results will appear below...")
        self.query_one("#target-input", Input).value = ""

    def update_results(self, result: Any) -> None:
        from rich.markup import escape
        import json
        
        # Re-enable button
        try:
            btn = self.query_one("#launch-btn", Button)
            btn.disabled = False
            btn.label = "Launch Auto"
        except:
            pass
        
        if result is None:
            formatted = "No results returned from tool."
        elif isinstance(result, (dict, list)):
            try:
                formatted = json.dumps(result, indent=2)
            except:
                formatted = str(result)
        else:
            formatted = str(result)
            
        # Escape the output to prevent markup parsing errors
        try:
            display = self.query_one("#results-display", Static)
            display.update(f"[bold green]✓ Execution Complete[/bold green]\n\n{escape(formatted)}")
        except:
            pass

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
                yield Label("[bold cyan]Welcome to Aleopantest V3.3.5[/bold cyan]", id="welcome-msg")
                yield Label("[#666666]by Aleocrophic[/#666666]", id="welcome-subtitle")
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
        try:
            # Match category name case-insensitively
            if not event.item or not event.item.id:
                return
                
            cat_id_raw = event.item.id.replace("cat-", "")
            cat_id = next((k for k in TOOLS_BY_CATEGORY.keys() if k.lower() == cat_id_raw), cat_id_raw)
            
            tools = TOOLS_BY_CATEGORY.get(cat_id, [])
            
            tool_list = self.query_one("#tool-list", ListView)
            tool_list.clear()
            
            new_items = []
            for tool_id in tools:
                if tool_id in TOOLS_REGISTRY:
                    try:
                        instance = TOOLS_REGISTRY[tool_id]()
                        name = instance.metadata.name
                        new_items.append(ListItem(Label(f"{name} ({tool_id})"), id=f"tool-{tool_id}"))
                    except Exception as e:
                        # Log or handle broken tool initialization
                        new_items.append(ListItem(Label(f"Error: {tool_id}"), id=f"tool-{tool_id}"))
            
            if new_items:
                tool_list.mount(*new_items)
            else:
                tool_list.mount(ListItem(Label("[yellow]No tools found in this category[/yellow]")))
            
            self.query_one("#instruction", Label).update(f"Tools in [cyan]{cat_id}[/cyan]:")
        except Exception as e:
            self.app.notify(f"Error changing category: {str(e)}", severity="error")

    @on(ListView.Selected, "#tool-list")
    def select_tool(self, event: ListView.Selected) -> None:
        tool_id = event.item.id.replace("tool-", "")
        self.app.push_screen(ToolExecutionScreen(tool_id))

class AleopantestTUI(App):
    """Main Textual Application for Aleopantest V3.3.5"""
    TITLE = "Aleopantest v3.3.5 PRO"
    SUB_TITLE = "by Aleocrophic - Advanced Cyber Security Tool Suite"
    
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
        width: 65%;
        padding: 1 2;
    }

    #tool-info-panel {
        width: 35%;
        background: #121212;
        border-left: solid #333;
        padding: 1 2;
    }

    #info-title {
        color: #00ffff;
        margin-bottom: 1;
        border-bottom: solid #333;
    }

    #usage-info, #example-info, #params-info {
        background: #0a0a0a;
        padding: 1;
        border: solid #333;
        margin-bottom: 1;
        color: #ccc;
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

    #action-buttons {
        height: auto;
        margin-top: 1;
    }

    #launch-btn {
        width: 1fr;
        background: #00ffff 20%;
        color: #00ffff;
        border: tall #00ffff;
    }

    #clear-btn {
        width: 1fr;
        margin-left: 1;
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
    app = AleopantestTUI()
    app.run()

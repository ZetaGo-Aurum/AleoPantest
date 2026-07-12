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
import re

from .core.platform_detector import PlatformDetector
from .core.session import SessionManager
from .core.automation import AutomationEngine, ContextDetector
from .core.base_tool import BaseTool
from .core.tool_helper import get_safe_attr
from .cli import TOOLS_BY_CATEGORY, TOOLS_REGISTRY


def _safe_id(value: str) -> str:
    """Sanitize a string into a valid Textual/CSS identifier.

    Identifiers must contain only letters, numbers, underscores or hyphens and
    must not begin with a number.
    """
    cleaned = re.sub(r"[^a-zA-Z0-9_-]", "-", str(value).lower())
    cleaned = re.sub(r"-+", "-", cleaned).strip("-")
    if not cleaned:
        cleaned = "id"
    if cleaned[0].isdigit():
        cleaned = "_" + cleaned
    return cleaned


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
                tool_name = get_safe_attr(self.tool_instance, "metadata.name", self.tool_id)
                tool_desc = get_safe_attr(self.tool_instance, "metadata.description", "No description available")
                
                yield Label(f"[bold cyan]Tool:[/bold cyan] {tool_name}", id="tool-title")
                yield Label(f"[dim]{tool_desc}[/dim]", id="tool-desc")
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
                yield Label(f"{tool_desc}", id="tool-desc-full")
                
                usage = get_safe_attr(self.tool_instance, "metadata.usage", "No usage guide available")
                yield Label("\n[yellow]Usage Guide:[/yellow]")
                yield Label(f"{usage}", id="usage-info")
                
                example = get_safe_attr(self.tool_instance, "metadata.example", "")
                if example:
                    yield Label("\n[yellow]Example:[/yellow]")
                    yield Label(f"{example}", id="example-info")
                
                parameters = get_safe_attr(self.tool_instance, "metadata.parameters", {})
                if parameters:
                    yield Label("\n[yellow]Available Parameters:[/yellow]")
                    params_text = ""
                    for k, v in parameters.items():
                        params_text += f"• [b]{k}[/b]: {v}\n"
                    yield Label(params_text.strip(), id="params-info")
                
                risk_level = get_safe_attr(self.tool_instance, "metadata.risk_level", "LOW")
                category = get_safe_attr(self.tool_instance, "metadata.category.value", "Unknown")
                author = get_safe_attr(self.tool_instance, "metadata.author", "Unknown")
                
                yield Label(f"\n[yellow]Risk Level:[/yellow] {risk_level}")
                yield Label(f"[yellow]Category:[/yellow] {category}")
                yield Label(f"[yellow]Author:[/yellow] {author}")
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
                call = self.tool_instance.resolve_call_kwargs(params)
                result = self.tool_instance.run(**call)
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
        except Exception:
            pass

        if isinstance(result, dict) and result.get("error"):
            formatted = f"[bold red]✗ Error[/bold red]\n\n{escape(str(result['error']))}"
        elif result is None:
            formatted = "[yellow]No results returned from tool.[/yellow]"
        elif isinstance(result, (dict, list)):
            try:
                formatted = escape(json.dumps(result, indent=2, default=str))
            except Exception:
                formatted = escape(str(result))
        else:
            formatted = escape(str(result))

        try:
            display = self.query_one("#results-display", Static)
            display.update(f"[bold green]✓ Execution Complete[/bold green]\n\n{formatted}")
        except Exception:
            pass

# Emoji/icons for categories to give the TUI a modern look.
_CATEGORY_ICONS = {
    "Network": "🌐", "Web": "🕸️", "OSINT": "🔍", "Utilities": "🛠️",
    "Phishing": "🎣", "Security": "🛡️", "Clickjacking": "🖱️", "Crypto": "🔐",
    "Wireless": "📡", "Database": "🗄️", "Reporting": "📊", "Exploit": "💥",
    "Forensics": "🔬", "Malware": "🦠", "Mobile Security": "📱", "Cloud Security": "☁️",
    "IoT Security": "📶", "Post-Exploitation": "🚩", "Social Engineering": "👥",
    "Active Directory": "🪪", "Api Security": "🔌", "Container": "📦",
    "Cloud": "☁️", "Web Advanced": "🕸️", "Network Advanced": "🌐",
    "Wireless Advanced": "📡", "Binary": "⚙️", "Osint": "🔎", "Password": "🔑",
    "Social": "👥", "Mobile": "📱", "Automation": "🤖", "Misc": "✨",
}


class Dashboard(Screen):
    """Main Dashboard with a modern 3-pane layout and live stats."""
    
    def compose(self) -> ComposeResult:
        self._cat_ids: Dict[str, str] = {}
        self._tool_ids: Dict[str, str] = {}
        self._tools_by_cat: Dict[str, list] = {}
        yield Header()
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Label("🛡  CATEGORIES", id="sidebar-title")
                with ListView(id="category-list"):
                    seen: set = set()
                    for category in TOOLS_BY_CATEGORY.keys():
                        sid = _safe_id(category)
                        base = sid
                        i = 2
                        while sid in seen:
                            sid = f"{base}-{i}"
                            i += 1
                        seen.add(sid)
                        self._cat_ids[sid] = category
                        self._tools_by_cat[sid] = TOOLS_BY_CATEGORY.get(category, [])
                        icon = _CATEGORY_ICONS.get(category, "•")
                        yield ListItem(Label(f"{icon}  {category}  [dim]({len(self._tools_by_cat[sid])})[/dim]"), id=f"cat-{sid}")
            
            with Vertical(id="main-content"):
                with Horizontal(id="stat-bar"):
                    yield Static(f"🧰 [b]{len(TOOLS_REGISTRY)}[/b] Tools", id="stat-tools")
                    yield Static(f"📂 [b]{len(TOOLS_BY_CATEGORY)}[/b] Categories", id="stat-cats")
                    yield Static(f"💻 {PlatformDetector.get_platform_name()}", id="stat-platform")
                yield Label("Select a category to begin →", id="instruction")
                with ListView(id="tool-list"):
                    yield ListItem(Label("Select a category first..."))
            
            with Vertical(id="detail-panel"):
                yield Label("🔎 TOOL DETAIL", id="detail-title")
                yield Static("Hover or select a tool on the left to see its description and risk level here.", id="detail-body")
        
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
        try:
            self.query_one("#status-bar", Static).update(status_text)
        except Exception:
            pass
        
        if not session['is_active']:
            self.app.notify("Session quota reached! Please restart.", severity="error")

    @on(ListView.Selected, "#category-list")
    def change_category(self, event: ListView.Selected) -> None:
        try:
            if not event.item or not event.item.id:
                return
                
            cat_id_raw = event.item.id.replace("cat-", "")
            cat_id = self._cat_ids.get(cat_id_raw, cat_id_raw)
            tools = TOOLS_BY_CATEGORY.get(cat_id, [])
            
            tool_list = self.query_one("#tool-list", ListView)
            tool_list.clear()
            
            new_items = []
            seen_tools: set = set()
            for tool_id in tools:
                if tool_id in TOOLS_REGISTRY:
                    try:
                        instance = TOOLS_REGISTRY[tool_id]()
                        name = instance.metadata.name
                        sid = _safe_id(tool_id)
                        base = sid
                        i = 2
                        while sid in seen_tools:
                            sid = f"{base}-{i}"
                            i += 1
                        seen_tools.add(sid)
                        self._tool_ids[sid] = tool_id
                        new_items.append(ListItem(Label(f"{name}  [dim]({tool_id})[/dim]"), id=f"tool-{sid}"))
                    except Exception as e:
                        new_items.append(ListItem(Label(f"Error: {tool_id}"), id=f"tool-{_safe_id(tool_id)}"))
            
            if new_items:
                tool_list.mount(*new_items)
            else:
                tool_list.mount(ListItem(Label("[yellow]No tools found in this category[/yellow]")))
            
            self.query_one("#instruction", Label).update(f"Tools in [cyan]{cat_id}[/cyan]:")
            self._show_category_detail(cat_id, len(tools))
        except Exception as e:
            self.app.notify(f"Error changing category: {str(e)}", severity="error")

    @on(ListView.Selected, "#tool-list")
    def select_tool(self, event: ListView.Selected) -> None:
        tool_id_raw = event.item.id.replace("tool-", "")
        tool_id = self._tool_ids.get(tool_id_raw, tool_id_raw)
        self._show_tool_detail(tool_id)
        self.app.push_screen(ToolExecutionScreen(tool_id))

    def _show_category_detail(self, cat_id: str, count: int) -> None:
        try:
            self.query_one("#detail-body", Static).update(
                f"[bold cyan]{cat_id}[/bold cyan]\n\n"
                f"Contains [b]{count}[/b] tools.\n\n"
                f"Select a tool from the middle panel to view its details, then press [b]Enter[/b] to launch it."
            )
        except Exception:
            pass

    def _show_tool_detail(self, tool_id: str) -> None:
        try:
            inst = TOOLS_REGISTRY.get(tool_id)
            if not inst:
                return
            instance = inst()
            name = getattr(getattr(instance, "metadata", None), "name", tool_id)
            desc = getattr(getattr(instance, "metadata", None), "description", "No description")
            risk = getattr(getattr(instance, "metadata", None), "risk_level", "LOW")
            risk_color = {"LOW": "green", "MEDIUM": "yellow", "HIGH": "red", "CRITICAL": "red"}.get(str(risk).upper(), "white")
            self.query_one("#detail-body", Static).update(
                f"[bold cyan]{name}[/bold cyan]  [dim]({tool_id})[/dim]\n\n"
                f"{desc}\n\n"
                f"Risk: [{risk_color}]{risk}[/{risk_color}]"
            )
        except Exception:
            pass

class AleopantestTUI(App):
    """Main Textual Application for Aleopantest"""
    TITLE = "Aleopantest v4.0.5 PRO"
    SUB_TITLE = "by Aleocrophic - Advanced Cyber Security Tool Suite"
    
    CSS = """
    Screen {
        background: #0b0e14;
        color: #c8d0da;
    }

    Header {
        background: #11161f;
        color: #38e1c6;
        text-style: bold;
        border-bottom: solid #1f6feb;
        height: 1;
    }

    Footer {
        background: #11161f;
        color: #7d8aa0;
        border-top: solid #1f6feb;
    }

    #sidebar {
        width: 34;
        background: #0e131c;
        border-right: solid #1c2530;
        margin: 1 0;
    }

    #sidebar-title {
        text-align: center;
        padding: 1;
        background: #11161f;
        color: #38e1c6;
        text-style: bold;
        border-bottom: solid #1c2530;
    }

    ListView {
        background: transparent;
        border: none;
    }

    ListItem {
        padding: 0 1;
        color: #9fb0c3;
    }

    ListItem:hover {
        background: #16202e;
        color: #38e1c6;
    }

    ListItem.--highlight {
        background: #1f6feb 25%;
        color: #ffffff;
        text-style: bold;
    }

    #main-content {
        width: 1fr;
        padding: 1 2;
    }

    #stat-bar {
        height: 3;
        margin-bottom: 1;
    }

    #stat-bar > Static {
        width: 1fr;
        background: #11161f;
        color: #38e1c6;
        border: solid #1c2530;
        border-title-align: center;
        padding: 0 1;
        text-align: center;
        content-align: center middle;
    }

    #instruction {
        color: #7d8aa0;
        margin-bottom: 1;
    }

    #tool-list {
        border: tall #1c2530;
        height: 1fr;
    }

    #detail-panel {
        width: 38;
        background: #0e131c;
        border-left: solid #1c2530;
        padding: 1 2;
    }

    #detail-title {
        color: #38e1c6;
        text-style: bold;
        border-bottom: solid #1c2530;
        margin-bottom: 1;
    }

    #detail-body {
        color: #c8d0da;
        padding: 1;
    }

    #status-bar {
        dock: bottom;
        height: 1;
        background: #11161f;
        color: #38e1c6;
        text-align: center;
        border-top: solid #1c2530;
    }

    /* Tool Execution Screen */
    #execution-container {
        width: 65%;
        padding: 1 2;
    }

    #tool-info-panel {
        width: 35%;
        background: #0e131c;
        border-left: solid #1c2530;
        padding: 1 2;
    }

    #info-title {
        color: #38e1c6;
        margin-bottom: 1;
        border-bottom: solid #1c2530;
    }

    #usage-info, #example-info, #params-info {
        background: #0b0e14;
        padding: 1;
        border: solid #1c2530;
        margin-bottom: 1;
        color: #cdd6e3;
    }

    #tool-title {
        text-style: bold;
        color: #38e1c6;
        border-bottom: solid #1f6feb;
        margin-bottom: 1;
    }

    #input-area {
        margin: 1 0;
        border: tall #1c2530;
        padding: 1;
        height: auto;
        background: #0e131c;
    }

    Input {
        background: #0b0e14;
        border: solid #1c2530;
        color: #38e1c6;
        margin-top: 1;
    }

    Input:focus {
        border: solid #1f6feb;
    }

    #action-buttons {
        height: auto;
        margin-top: 1;
    }

    #launch-btn {
        width: 1fr;
        background: #1f6feb 25%;
        color: #ffffff;
        border: tall #1f6feb;
    }

    #clear-btn {
        width: 1fr;
        margin-left: 1;
    }

    #launch-btn:hover {
        background: #1f6feb 45%;
    }

    #results-display {
        background: #05070a;
        color: #79e87a;
        padding: 1;
        border: solid #1c2530;
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

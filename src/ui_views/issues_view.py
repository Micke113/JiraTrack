from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Header, Input, Label, ListItem, ListView

from src.jira_track import TICKET_HEADERS


class IssuesScreen(Screen):
    """Screen displaying Jira tickets in a scrollable data table."""

    BINDINGS = [
        Binding("escape", "go_back", "Retour"),
        Binding("q", "go_back", "Retour"),
    ]

    def __init__(self, issues: list[dict]) -> None:
        super().__init__()
        self.issues = issues

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield DataTable(id="issues-table", cursor_type="row")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("#", *TICKET_HEADERS)
        for i, issue in enumerate(self.issues, start=1):
            table.add_row(str(i), *(str(issue.get(h, "")) for h in TICKET_HEADERS))
        table.focus()

    def action_go_back(self) -> None:
        self.app.pop_screen()

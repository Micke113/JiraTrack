from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Header, Input, Label, ListItem, ListView


class ExcelExportScreen(Screen):
    """Screen prompting user how to export issues to Excel."""

    BINDINGS = [
        Binding("escape", "go_back", "Annuler"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="excel-container"):
            yield Label("Méthode d'export", id="menu-title")
            yield ListView(
                ListItem(
                    Button("Exporter vers Excel", id="export-excel", variant="primary"),
                    Button("Exporter vers Excel (Template)", id="export-excel-template", variant="primary")
                ),
                id="main-menu",
            )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "export-excel":
            self.app._export_issues()
        elif event.button.id == "export-excel-template":
            self.app._export_issues(template=True)

    def action_go_back(self) -> None:
        self.app.pop_screen()

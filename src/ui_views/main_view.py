from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Header, Input, Label, ListItem, ListView

from src.jira_track import TICKET_HEADERS
from src.model import MenuModel


class MainMenuScreen(Screen):
    """Main menu screen with navigable options."""

    BINDINGS = [
        Binding("q", "app.quit", "Quitter"),
    ]

    def __init__(self, model: MenuModel) -> None:
        super().__init__()
        self.mod = model

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="menu-container"):
            yield Label("JIRA TRACK", id="menu-title")
            yield ListView(
                *(ListItem(Label(option), id=f"menu-item-{i}")
                  for i, option in enumerate(self.mod.options)),
                id="main-menu",
            )
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        index = int(event.item.id.split("-")[-1])
        self.app.handle_menu_select(index)

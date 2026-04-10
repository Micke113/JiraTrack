from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Header, Input, Label, ListItem, ListView


class UserDataScreen(Screen):
    """Screen prompting user to input data."""

    """Screen prompting the user to paste their Jira session cookie."""

    BINDINGS = [
        Binding("escape", "go_back", "Annuler"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="data-container"):
            with Vertical(id="data-form"):
                yield Label("Veuillez saisir vos données :")
                yield Input(
                    placeholder="Lien Jira",
                    id="jira-link",
                )
                yield Input(
                    placeholder="Mail utilisateur",
                    id="jira-user",
                )
                yield Button("Valider", id="submit-data", variant="primary")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit-data":
            self._submit()

    def on_input_submitted(self, _: Input.Submitted) -> None:
        self._submit()

    def _submit(self) -> None:
        data = {
            "jira_link": self.query_one("#jira-link", Input).value.strip(),
            "jira_user": self.query_one("#jira-user", Input).value.strip(),
        }
        if data["jira_link"] and data["jira_user"]:
            self.app.handle_data_saved(data)

    def action_go_back(self) -> None:
        self.app.pop_screen()
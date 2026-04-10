from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Header, Input, Label, ListItem, ListView


class CookieInputScreen(Screen):
    """Screen prompting the user to paste their Jira session cookie."""

    BINDINGS = [
        Binding("escape", "go_back", "Annuler"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="cookie-container"):
            with Vertical(id="cookie-form"):
                yield Label("Cookie Jira introuvable. Collez votre cookie JSESSIONID :")
                yield Input(
                    placeholder="Votre cookie de session Jira...",
                    id="cookie-input",
                    password=True,
                )
                yield Button("Valider", id="submit-cookie", variant="primary")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit-cookie":
            self._submit()

    def on_input_submitted(self, _: Input.Submitted) -> None:
        self._submit()

    def _submit(self) -> None:
        cookie = self.query_one("#cookie-input", Input).value.strip()
        if cookie:
            self.app.handle_cookie_saved(cookie)

    def action_go_back(self) -> None:
        self.app.pop_screen()
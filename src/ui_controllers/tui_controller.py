from textual import work
from textual.app import App

from src.jira_track import (
    export_to_excel,
    format_issues_to_headers,
    get_jira_issues,
    load_cookie,
    save_cookie,
)
from src.model import MenuModel
from src.ui_views.main_view import MainMenuScreen
from src.ui_views.cookie_view import CookieInputScreen
from src.ui_views.issues_view import IssuesScreen
from src.ui_views.userdata_view import UserDataScreen


class JiraTrackApp(App[None]):
    """Textual TUI application for JiraTrack."""

    CSS = """
    #menu-container {
        align: center middle;
        height: 1fr;
    }

    #menu-title {
        text-align: center;
        color: cyan;
        text-style: bold;
        margin-bottom: 1;
    }

    #main-menu {
        width: 40;
        border: solid cyan;
    }

    #cookie-container {
        align: center middle;
        height: 1fr;
    }

    #cookie-form {
        width: 60;
        border: solid cyan;
        padding: 1 2;
    }

    #cookie-form Label {
        margin-bottom: 1;
    }

    #cookie-form Input {
        margin-bottom: 1;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self.model = MenuModel()
        self.model.cookie = load_cookie()

    def on_mount(self) -> None:
        self.push_screen(MainMenuScreen(self.model))

    # --- Menu actions ---

    def handle_menu_select(self, index: int) -> None:
        choice = self.model.options[index]
        match choice:
            case "Voir mes données utilisateur":
                self.push_screen(UserDataScreen())
            case "Voir les tickets":
                if not self.model.cookie:
                    self.push_screen(CookieInputScreen())
                else:
                    self._fetch_issues()
            case "Exporter vers Excel":
                if not self.model.issues:
                    self.notify(
                        "Aucun ticket à exporter. Chargez d'abord les tickets.",
                        severity="warning",
                    )
                else:
                    self._export_issues()
            case "Quitter":
                self.exit()

    # --- Workers (non-blocking network / IO calls) ---

    @work(thread=True, exclusive=True)
    def _fetch_issues(self) -> None:
        issues = get_jira_issues(self.model.cookie)
        if not issues:
            self.call_from_thread(
                self.notify,
                "Impossible de récupérer les tickets. Vérifiez votre cookie.",
                severity="error",
            )
            self.call_from_thread(self.push_screen, CookieInputScreen())
            return
        formatted = format_issues_to_headers(issues)
        self.model.issues = formatted
        self.call_from_thread(self.push_screen, IssuesScreen(formatted))

    @work(thread=True)
    def _export_issues(self) -> None:
        export_to_excel(self.model.issues)
        self.call_from_thread(self.notify, "Export Excel terminé !", severity="information")

    # --- Cookie handling ---

    def handle_cookie_saved(self, cookie: str) -> None:
        save_cookie(cookie)
        self.model.cookie = cookie
        self.pop_screen()
        self._fetch_issues()


def run():
    JiraTrackApp().run()
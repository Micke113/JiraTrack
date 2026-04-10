
class MenuModel:
    def __init__(self):
        self.options = ["Voir mes données utilisateur", "Voir les tickets", "Exporter vers Excel", "Quitter"]
        self.selected_index = 0
        self.issues = []
        self.cookie = None

    def move_up(self):
        self.selected_index = (self.selected_index - 1) % len(self.options)

    def move_down(self):
        self.selected_index = (self.selected_index + 1) % len(self.options)

    def get_selected(self):
        return self.options[self.selected_index]

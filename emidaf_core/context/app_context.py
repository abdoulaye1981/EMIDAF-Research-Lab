class AppContext:

    def __init__(self):

        self.reset()

    # =====================================================
    # Réinitialisation
    # =====================================================

    def reset(self):

        self.current_project = None

        self.current_dataset = None

        self.current_model = None

        self.current_page = "Accueil"

        self.current_user = None

        self.current_theme = "EMIDAF"

        self.current_language = "fr"

        self.current_workspace = None

    # =====================================================
    # Projet
    # =====================================================

    def set_project(self, project):

        self.current_project = project

    def get_project(self):

        return self.current_project

    # =====================================================
    # Dataset
    # =====================================================

    def set_dataset(self, dataset):

        self.current_dataset = dataset

    def get_dataset(self):

        return self.current_dataset

    # =====================================================
    # Modèle
    # =====================================================

    def set_model(self, model):

        self.current_model = model

    def get_model(self):

        return self.current_model

    # =====================================================
    # Page
    # =====================================================

    def set_page(self, page):

        self.current_page = page

    def get_page(self):

        return self.current_page

    # =====================================================
    # Utilisateur
    # =====================================================

    def set_user(self, user):

        self.current_user = user

    def get_user(self):

        return self.current_user

    # =====================================================
    # Thème
    # =====================================================

    def set_theme(self, theme):

        self.current_theme = theme

    def get_theme(self):

        return self.current_theme

    # =====================================================
    # Langue
    # =====================================================

    def set_language(self, language):

        self.current_language = language

    def get_language(self):

        return self.current_language

    # =====================================================
    # Workspace
    # =====================================================

    def set_workspace(self, workspace):

        self.current_workspace = workspace

    def get_workspace(self):

        return self.current_workspace
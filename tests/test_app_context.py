from emidaf_core.context.app_context import AppContext


def main():

    context = AppContext()

    print()

    print("=" * 60)

    print("TEST APP CONTEXT")

    print("=" * 60)

    print()

    context.set_project("Doctorat")

    context.set_dataset("students.csv")

    context.set_model("Random Forest")

    context.set_page("Inspection")

    context.set_user("Pr. Abdoulaye Wakhab DIOP")

    context.set_theme("Dark")

    context.set_language("fr")

    context.set_workspace("workspace/projects")

    print("Projet      :", context.get_project())

    print("Dataset     :", context.get_dataset())

    print("Modèle      :", context.get_model())

    print("Page        :", context.get_page())

    print("Utilisateur :", context.get_user())

    print("Thème       :", context.get_theme())

    print("Langue      :", context.get_language())

    print("Workspace   :", context.get_workspace())

    print()

    print("AppContext OK")


if __name__ == "__main__":

    main()
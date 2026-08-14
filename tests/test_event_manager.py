from emidaf_core.managers.event_manager import EventManager


def on_project_created(project_name):

    print(f"Projet créé : {project_name}")


def on_dataset_imported(dataset):

    print(f"Dataset importé : {dataset}")


def main():

    manager = EventManager()

    manager.subscribe(

        "PROJECT_CREATED",

        on_project_created

    )

    manager.subscribe(

        "DATASET_IMPORTED",

        on_dataset_imported

    )

    print()

    print("=" * 60)

    print("TEST EVENT MANAGER")

    print("=" * 60)

    print()

    print("Evénements enregistrés")

    print(manager.list())

    print()

    print("Publication")

    print("---------------------")

    manager.publish(

        "PROJECT_CREATED",

        "Doctorat"

    )

    manager.publish(

        "DATASET_IMPORTED",

        "students.csv"

    )

    print()

    print("Subscribers")

    print("---------------------")

    print(

        "PROJECT_CREATED :",

        manager.subscribers(

            "PROJECT_CREATED"

        )

    )

    print(

        "DATASET_IMPORTED :",

        manager.subscribers(

            "DATASET_IMPORTED"

        )

    )

    print()

    print("EventManager OK")


if __name__ == "__main__":

    main()
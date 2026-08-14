from emidaf_core.bootstrap import Bootstrap


def main():

    bootstrap = Bootstrap()

    registry = bootstrap.initialize()

    print()

    print("Composants enregistrés")

    print("----------------------")

    for component in registry.list():

        print(component)


if __name__ == "__main__":

    main()
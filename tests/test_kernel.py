from emidaf_core.kernel import Kernel


def main():

    print()

    print("=" * 60)

    print("TEST KERNEL")

    print("=" * 60)

    print()

    kernel = Kernel()

    registry = kernel.start()

    print("Registry créé :", registry is not None)

    print()

    composants = registry.list()

    print("Composants enregistrés")

    print("----------------------")

    for composant in composants:

        print(composant)

    print()

    print("Nombre de composants :", len(composants))

    print()

    print("Kernel OK")


if __name__ == "__main__":

    main()
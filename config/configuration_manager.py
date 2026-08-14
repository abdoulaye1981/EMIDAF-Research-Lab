import json
from pathlib import Path


class ConfigurationManager:

    def __init__(self):

        self._config = {}

        self._config_file = Path(__file__).parent / "settings.json"

        self.initialize()

    # ==========================================================
    # Initialisation
    # ==========================================================

    def initialize(self):

        self.load()

    # ==========================================================
    # Chargement
    # ==========================================================

    def load(self):

        if not self._config_file.exists():

            raise FileNotFoundError(

                f"Fichier de configuration introuvable : {self._config_file}"

            )

        with open(

            self._config_file,

            "r",

            encoding="utf-8"

        ) as file:

            self._config = json.load(file)

    # ==========================================================
    # Rechargement
    # ==========================================================

    def reload(self):

        self.load()

    # ==========================================================
    # Accès générique
    # ==========================================================

    def get(self, key, default=None):

        return self._config.get(key, default)

    def has(self, key):

        return key in self._config

    def keys(self):

        return list(self._config.keys())

    def values(self):

        return list(self._config.values())

    def items(self):

        return list(self._config.items())

    def count(self):

        return len(self._config)

    # ==========================================================
    # Modification
    # ==========================================================

    def set(self, key, value):

        self._config[key] = value

    def remove(self, key):

        if key in self._config:

            del self._config[key]

    def clear(self):

        self._config.clear()

    # ==========================================================
    # Sauvegarde
    # ==========================================================

    def save(self):

        with open(

            self._config_file,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                self._config,

                file,

                indent=4,

                ensure_ascii=False

            )

    # ==========================================================
    # Propriétés
    # ==========================================================

    @property
    def application(self):

        return self._config.get("application")

    @property
    def version(self):

        return self._config.get("version")

    @property
    def theme(self):

        return self._config.get("theme")

    @property
    def language(self):

        return self._config.get("language")

    @property
    def workspace(self):

        return self._config.get("workspace")

    @property
    def database(self):

        return self._config.get("database")

    @property
    def debug(self):

        return self._config.get("debug")

    @property
    def autosave(self):

        return self._config.get("autosave")

    @property
    def log_level(self):

        return self._config.get("log_level")
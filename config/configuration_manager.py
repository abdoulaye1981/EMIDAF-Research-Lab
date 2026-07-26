import json
from pathlib import Path


class ConfigurationManager:

    def __init__(self):

        self.settings = {}

        self.settings_file = Path("config/settings.json")

    def load(self):

        if self.settings_file.exists():

            with open(

                self.settings_file,

                encoding="utf-8"

            ) as file:

                self.settings = json.load(file)

        else:

            self.settings = {}

    def get(self, key, default=None):

        return self.settings.get(key, default)

    def set(self, key, value):

        self.settings[key] = value

    def save(self):

        with open(

            self.settings_file,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                self.settings,

                file,

                indent=4,

                ensure_ascii=False

            )
from config.configuration_manager import ConfigurationManager

config = ConfigurationManager()

settings = config.load()

print(settings)
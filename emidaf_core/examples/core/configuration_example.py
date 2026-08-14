from emidaf_core.core.configuration import Configuration

config = Configuration()

config.analysis.enable_parallel = True

config.analysis.max_workers = 8

config.reporting.export_pdf = True

print(config)
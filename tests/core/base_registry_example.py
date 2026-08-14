from emidaf_core.core.base_registry import BaseRegistry

registry = BaseRegistry()

registry.register(

    "Analyzer1",

    object()

)

registry.register(

    "Analyzer2",

    object()

)

print(

    registry.names

)

for analyzer in registry:

    print(analyzer)
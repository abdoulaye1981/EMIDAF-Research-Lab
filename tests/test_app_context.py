from emidaf_core.context.app_context import AppContext

context = AppContext()

print(context.current_project)
print(context.current_dataset)
print(context.current_user)
print(context.current_experiment)
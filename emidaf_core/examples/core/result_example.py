from emidaf_core.core.base_result import BaseResult

result = BaseResult()

result.score = 98.4

result.execution_time = 0.21

result.add_warning("Quelques valeurs manquantes.")

result.add_recommendation("Effectuer une imputation.")

result.put("rows", 5000)

print(result.to_dict())
from emidaf_core.core.analyzer_result import AnalyzerResult

result = AnalyzerResult("StructureAnalyzer")

result.description = "Analyse de la structure"

result.score = 97.5

result.execution_time = 0.15

result.put("rows", 1000)

result.set_statistic("columns", 12)

result.add_recommendation("Aucune action nécessaire.")

result.finalize()

print(result.to_dict())
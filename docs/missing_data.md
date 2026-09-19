# EMIDAF — Missing Data Module

## 1. Overview

The EMIDAF missing-data subsystem provides a complete workflow for:

- detecting missing values;
- analyzing missingness patterns;
- assessing evidence related to MCAR, MAR and MNAR;
- recommending imputation strategies;
- constructing an auditable imputation plan;
- applying simple or multivariate imputation methods;
- identifying variables requiring manual review;
- generating technical and scientific reports.

The high-level public API is exposed through:

```python
from emidaf_core.missing import (
    MissingPipeline,
    MissingReporter,
)

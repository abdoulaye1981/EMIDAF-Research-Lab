from database.database import Base
from database.database import engine

import database.models

Base.metadata.create_all(bind=engine)

print("Base EMIDAF créée avec succès.")
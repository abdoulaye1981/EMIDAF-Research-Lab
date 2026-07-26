from database.database_manager import DatabaseManager

db = DatabaseManager()

print(db)

print(db.get_session())

db.close()

print("DatabaseManager OK")
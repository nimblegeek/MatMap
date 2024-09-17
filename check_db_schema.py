from main import app, db
from sqlalchemy import inspect

def check_db_schema():
    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print("Tables in the database:", tables)
        
        for table in tables:
            columns = inspector.get_columns(table)
            print(f"\nColumns in {table} table:")
            for column in columns:
                print(f"- {column['name']} ({column['type']})")

if __name__ == '__main__':
    check_db_schema()

import sqlite3
from pathlib import Path


def main():
    project_folder = Path(__file__).parent
    database_path = project_folder / "instance" / "applications.db"
    schema_path = project_folder / "schema.sql"

    database_path.parent.mkdir(exist_ok=True)

    connection = sqlite3.connect(database_path)

    with schema_path.open(encoding="utf-8") as schema_file:
        connection.executescript(schema_file.read())

    connection.commit()
    connection.close()

    print("Database initialized.")


if __name__ == "__main__":
    main()
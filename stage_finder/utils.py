from sqlalchemy import create_engine, inspect
from stage_finder.settings import DATABASE_URL


def return_string_from_table(table_name: str) -> str:
    engine = create_engine(DATABASE_URL)

    inspector = inspect(engine)

    all_columns = inspector.get_columns(table_name)

    ddl_statement = f"CREATE TABLE {table_name} ("

    for col in all_columns:
        col_name = col["name"]
        col_type = col["type"]
        nullable = not col["nullable"]

        col_def = f"{col_name} {col_type} {'NOT NULL' if nullable else ''}"

        ddl_statement += f"{col_def}, "

    ddl_statement = ddl_statement[:-2]

    # pk_constraint = inspector.get_primary_keys(table_name)
    # if pk_constraint:
    #     pk_cols = ", ".join(col["name"] for col in pk_constraint)
    #     ddl_statement += f", PRIMARY KEY ({pk_cols})"

    ddl_statement += ")"

    return ddl_statement

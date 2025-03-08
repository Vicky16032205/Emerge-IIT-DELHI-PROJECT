import psycopg2
from typing import List, Dict

class PGManager:
    def __init__(self, dbname: str, user: str, password: str, host: str):
        """
        Manages PostgreSQL database connections and operations.
        """
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
        )

    def get_schema(self) -> str:
        """
        Extracts the database schema for use in prompts.
        """
        schema_query = """
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
        """
        schema_data = self.execute_query(schema_query)
        schema_str = "\n".join(
            f"Table: {row['table_name']}, Column: {row['column_name']}, Type: {row['data_type']}"
            for row in schema_data
        )
        return schema_str

    def execute_query(self, query: str) -> List[Dict]:
        """
        Executes a SQL query and returns the results as a list of dictionaries.
        """
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(query)
                if cursor.description:
                    columns = [desc[0] for desc in cursor.description]
                    return [dict(zip(columns, row)) for row in cursor.fetchall()]
                return []
            except Exception as e:
                print(f"Query execution failed: {e}")
                return []
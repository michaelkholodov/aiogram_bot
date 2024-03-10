import sqlite3


class SimpleORM:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        columns_definition = ', '.join(columns)
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition})"
        self.execute_query(query)

    def insert(self, table_name, data):
        columns = ', '.join(data.keys())
        values = ', '.join([f"'{value}'" for value in data.values()])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        self.execute_query(query)

    def select(self, table_name, filters=None):
        query = f"SELECT * FROM {table_name}"
        if filters:
            where_clause = self._build_where_clause(filters)
            query += f" WHERE {where_clause}"
        return self.execute_query(query)

    def update(self, table_name, data, filters=None):
        set_clause = ', '.join([f"{key}='{value}'" for key, value in data.items()])
        query = f"UPDATE {table_name} SET {set_clause}"
        if filters:
            where_clause = self._build_where_clause(filters)
            query += f" WHERE {where_clause}"
        self.execute_query(query)

    def delete(self, table_name, filters=None):
        query = f"DELETE FROM {table_name}"
        if filters:
            where_clause = self._build_where_clause(filters)
            query += f" WHERE {where_clause}"
        self.execute_query(query)

    def _build_where_clause(self, filters):
        conditions = [f"{key}='{value}'" for key, value in filters.items()]
        return ' AND '.join(conditions)

    def execute_query(self, query):
        self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()


"""# Example usage:
orm = SimpleORM('database.db')

# Create a table
orm.create_table('users', ['id INTEGER PRIMARY KEY', 'name TEXT', 'age INTEGER'])
orm.create_table('posts', ['id INTEGER PRIMARY KEY', 'name TEXT', 'description TEXT'])
# Insert data
orm.insert('users', {'name': 'John Doe', 'age': 25})
orm.insert('users', {'name': 'Jane Doe', 'age': 30})

# Select data
result = orm.select('users', filters={'name': 'John Doe'})

print(result)

# Update data
orm.update('users', {'age': 26}, filters={'name': 'John Doe'})
print(orm.select('users'))
# Delete data

"""
'''
@Author: Sanjay Kumar V
@Date: 2024-08-23
@Last Modified by:Sanjay Kumar
@Last Modified: 2024-08-23
@Title : CRUD operation to create table in SQL server using python.

'''

import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

class SQLServerCRUD:
    def __init__(self):
        self.driver = os.getenv("Driver")
        self.server = os.getenv("Server")
        self.database = os.getenv("Database")
        self.trusted_connection = os.getenv("Trusted_Connection")

        self.connection_string = (
            f"Driver={{{self.driver}}};"
            f"Server={self.server};"
            f"Database={self.database};"
            f"Trusted_Connection={self.trusted_connection};"
        )

        self.sqlDbConn = pyodbc.connect(self.connection_string)

    def create_database(self, database_name):
        
        '''Function Takes the datbase name and create one database on that name

        parameters-str-Database name

        returns-None
        '''
        print(f"Creating database: {database_name}")
        create_db_conn_string = (
            f"Driver={{{self.driver}}};"
            f"Server={self.server};"
            f"Trusted_Connection={self.trusted_connection};"
        )
        try:
            with pyodbc.connect(create_db_conn_string, autocommit=True) as conn:
                cursor = conn.cursor()
                cursor.execute(f"""
                    IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = ?)
                    BEGIN
                        CREATE DATABASE {database_name}
                    END
                """, database_name)
                print(f"Database '{database_name}' has been created.")
        except pyodbc.Error as e:
            print(f"An error occurred: {e}")

        self.database = database_name
        self.connection_string = (
            f"Driver={{{self.driver}}};"
            f"Server={self.server};"
            f"Database={self.database};"
            f"Trusted_Connection={self.trusted_connection};"
        )
        self.sqlDbConn.close()
        self.sqlDbConn = pyodbc.connect(self.connection_string)

    def show_databases(self):
        
        '''Function print the all database
        
        parameters-str-none

        returns-None
        '''
        print("Showing all databases:")
        show_db_conn_string = (
            f"Driver={{{self.driver}}};"
            f"Server={self.server};"
            f"Trusted_Connection={self.trusted_connection};"
        )
        try:
            with pyodbc.connect(show_db_conn_string) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sys.databases")
                databases = cursor.fetchall()
                for db in databases:
                    print(db.name)
                return databases
        except pyodbc.Error as e:
            print(f"An error occurred: {e}")

    def create_table(self, table_name, columns, database_name=None):
        
        '''Function take the table name and table calomus and name create the table
        
        parameters-str-table_name,columns,database_name

        returns-None
        '''
        if database_name:
            print(f"Switching to database: {database_name}")
            self.database = database_name
            self.connection_string = (
                f"Driver={{{self.driver}}};"
                f"Server={self.server};"
                f"Database={self.database};"
                f"Trusted_Connection={self.trusted_connection};"
            )
            self.sqlDbConn.close()
            self.sqlDbConn = pyodbc.connect(self.connection_string)

        print(f"Creating table: {table_name} in database: {self.database}")
        cursor = self.sqlDbConn.cursor()
        
        columns_with_types = ", ".join([f"{col_name} {col_type}" for col_name, col_type in columns.items()])
        cursor.execute(f"""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{table_name}' AND xtype='U')
            CREATE TABLE {table_name} (
                {columns_with_types}
            )
        """)
        self.sqlDbConn.commit()

    def get_data(self, table_name):
        
        '''Function take table name print data in the table
        
        parameters-table_name-table_name

        returns-None
        '''
        print('Read')
        cursor = self.sqlDbConn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        return rows

    def insert_data(self, table_name, data):
        
        '''Function take table name print data in the table.
        
        parameters-table_name-table_name,date.

        returns-None
        '''
        print("Insert")
        cursor = self.sqlDbConn.cursor()
        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' * len(data))
        cursor.execute(
            f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})',
            tuple(data.values())
        )
        self.sqlDbConn.commit()

    def update_data(self, table_name, updates, condition):
        
        '''Function take table name print data in the table
        
        parameters-table_name-table_name,date,uadates,condition.

        returns-None
        '''
        print('Update')
        cursor = self.sqlDbConn.cursor()
        set_clause = ', '.join([f"{key} = ?" for key in updates])
        condition_clause = ' AND '.join([f"{key} = ?" for key in condition])
        values = tuple(updates.values()) + tuple(condition.values())
        cursor.execute(
            f'UPDATE {table_name} SET {set_clause} WHERE {condition_clause}',
            values
        )
        self.sqlDbConn.commit()

    def delete_data(self, table_name, condition):
        
        '''Function take table name delete values in the table
        
        parameters-table_name-table_name,condition.

        returns-None
        '''
        print('Delete')
        cursor = self.sqlDbConn.cursor()
        condition_clause = ' AND '.join([f"{key} = ?" for key in condition])
        cursor.execute(
            f'DELETE FROM {table_name} WHERE {condition_clause}',
            tuple(condition.values())
        )
        self.sqlDbConn.commit()

    def reset_identity(self, table_name):
        
        '''Function take table name delete values in the table
        
        parameters-table_name-table_name,condition.

        returns-None
        '''
        print('Reset Identity')
        cursor = self.sqlDbConn.cursor()
        cursor.execute(f"DBCC CHECKIDENT ('{table_name}', RESEED, 0)")
        self.sqlDbConn.commit()

    def show_tables(self):
        
        '''Function print the all table in database.
        
        parameters- None

        returns-None
        '''
        print("Showing all tables:")
        cursor = self.sqlDbConn.cursor()
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_type = 'BASE TABLE'
            AND table_catalog = ?
        """, self.database)
        tables = cursor.fetchall()
        for table in tables:
            print(table.table_name)
        return tables
    
    def delete_table(self, table_name):
        
        '''Function print the delete table in database.
        
        parameters- Table_name

        returns-None
        '''
        print(f"Deleting table: {table_name}")
        cursor = self.sqlDbConn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.sqlDbConn.commit()
        print(f"Table '{table_name}' has been deleted.")
    
    def show_columns(self, table_name):
        
        '''Function print the show all the columns  table in database.
        
        parameters- Table_name

        returns-None
        '''
        print(f"Showing columns for table: {table_name}")
        cursor = self.sqlDbConn.cursor()
        cursor.execute(f"""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = ?
        """, table_name)
        columns = cursor.fetchall()
        for column in columns:
            print(f"Column Name: {column.COLUMN_NAME}, Data Type: {column.DATA_TYPE}, Nullable: {column.IS_NULLABLE}")
        return columns

    def close_connection(self):
        '''Function close the connection to the database
        
        parameters- None

        returns-None
        '''
        self.sqlDbConn.close()

def menu():
    print("\nMenu:")
    print("1. Create a new database")
    print("2. Create a new table")
    print("3. Insert data into the table")
    print("4. Read data from the table")
    print("5. Update data in the table")
    print("6. Delete data from the table")
    print("7. Reset identity column")
    print("8. Show all tables")
    print("9. Delete specified table")
    print("10. Show the specified table columns")
    print("11. Show all databases")
    print("12. Exit")
    
    try:
        return int(input("Select an option: "))
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 12.")
        return None

def get_table_fields():
    fields = {}
    while True:
        field_name = input("Enter field name (or press Enter to finish): ")
        if not field_name:
            break
        field_value = input(f"Enter value for {field_name}: ")
        fields[field_name] = field_value
    return fields

def get_table_columns():
    columns = {}
    print("Define the columns for your table:")
    while True:
        col_name = input("Enter column name (or press Enter to finish): ")
        if not col_name:
            break
        col_type = input(f"Enter data type for column '{col_name}' (e.g., INT, NVARCHAR(50), BIGINT): ")
        columns[col_name] = col_type
    return columns

if __name__ == "__main__":
    crud = SQLServerCRUD()

    while True:
        choice = menu()

        if choice is None:
            continue

        if choice == 1:
            database_name = input("Enter the database name to create: ")
            crud.create_database(database_name)

        elif choice == 2:
            database_name = input("Enter the database name where the table will be created (leave empty for current database): ")
            table_name = input("Enter the table name to create: ")
            columns = get_table_columns()
            crud.create_table(table_name, columns, database_name if database_name else None)

        elif choice == 3:
            table_name = input("Enter the table name: ")
            data = get_table_fields()
            crud.insert_data(table_name, data)

        elif choice == 4:
            table_name = input("Enter the table name: ")
            crud.get_data(table_name)

        elif choice == 5:
            table_name = input("Enter the table name: ")
            condition = get_table_fields()
            updates = get_table_fields()
            crud.update_data(table_name, updates, condition)

        elif choice == 6:
            table_name = input("Enter the table name: ")
            condition = get_table_fields()
            crud.delete_data(table_name, condition)

        elif choice == 7:
            table_name = input("Enter the table name: ")
            reset = input("Are you sure you want to reset the identity column? (yes/no): ")
            if reset.lower() == 'yes':
                crud.reset_identity(table_name)

        elif choice == 8:
            crud.show_tables()
        
        elif choice == 9:
            table_name = input("Enter the table name to delete: ")
            confirmation = input(f"Are you sure you want to delete the table '{table_name}'? This action cannot be undone. (yes/no): ")
            if confirmation.lower() == 'yes':
                crud.delete_table(table_name)
        
        elif choice == 10:
            table_name = input("Enter the table name to show columns: ")
            crud.show_columns(table_name)

        elif choice == 11:
            crud.show_databases()

        elif choice == 12:
            crud.close_connection()
            print("Connection closed. Exiting...")
            break

        else:
            print("Invalid choice. Please select a valid option.")

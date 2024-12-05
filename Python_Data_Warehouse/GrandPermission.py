import pyodbc

# Connection parameters
server = 'localhost'
port = '1433'
database = 'Mark_Db'  # Connect to 'master' initially
username = 'WM6'
password = 'WM6'

# Create the connection string
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server},{port};DATABASE={database};UID={username};PWD={password}'

try:
    # Establish the connection
    conn = pyodbc.connect(conn_str)
    
    # Create a cursor
    cursor = conn.cursor()
    
    print("Successfully connected to the database!")
    
    # SQL commands to create user and grant permissions
    user_creation_commands = [
        "USE [Mark_Db];",
        "IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = 'WM6') BEGIN CREATE USER [WM6] FOR LOGIN [WM6]; END",
        "ALTER ROLE [db_datareader] ADD MEMBER [WM6];",
        "ALTER ROLE [db_datawriter] ADD MEMBER [WM6];"
    ]

    # user_delete_commands = [
    #     "USE [Mark_Db];",
    #     "IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = 'WM6') BEGIN CREATE USER [WM6] FOR LOGIN [WM6]; END",
    #     "ALTER ROLE [db_datareader] DROP MEMBER [WM6];",
    #     "ALTER ROLE [db_datawriter] DROP MEMBER [WM6];"
    # ]
    
    # Execute user creation commands
    for command in user_creation_commands:
        cursor.execute(command)
        conn.commit()

    # for command in user_delete_commands:
    #     cursor.execute(command)
    #     conn.commit()
    
    # print("User created and permissions granted successfully.")

    print("User drop and permissions granted successfully.")
    
    # Switch to Mark_Db
    cursor.execute("USE [Mark_Db];")
    
    # Get and print server information
    cursor.execute("SELECT @@VERSION")
    row = cursor.fetchone()
    print(f"\nSQL Server version:\n{row[0]}")
    
    # Get and print database names
    print("\nDatabases in this SQL Server:")
    cursor.execute("SELECT name FROM sys.databases")
    for row in cursor.fetchall():
        print(row.name)
    
    # Example query - replace with a query suitable for your Mark_Db schema
    cursor.execute("SELECT TOP 10 * FROM INFORMATION_SCHEMA.TABLES")
    
    # Fetch all rows
    rows = cursor.fetchall()
    
    # Get column names
    columns = [column[0] for column in cursor.description]
    
    # Print column names
    print("\nColumns:")
    print(" | ".join(columns))
    print("-" * (sum(len(col) for col in columns) + 3 * (len(columns) - 1)))
    
    # Print rows
    print("\nData:")
    for row in rows:
        print(" | ".join(str(value) for value in row))
    
    # Print total number of rows
    print(f"\nTotal rows: {len(rows)}")

except pyodbc.Error as e:
    print(f"Error connecting to the database: {e}")

finally:
    # Close the connection
    if 'conn' in locals():
        conn.close()
        print("\nDatabase connection closed.")
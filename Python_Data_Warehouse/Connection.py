import pyodbc

# Connection parameters
server = 'localhost'
port = '1433'
database = 'COOLBLUE_DB'  # You can change this to your specific database name
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
    
    # Get and print server information
    cursor.execute("SELECT @@VERSION")
    row = cursor.fetchone()
    print(f"\nSQL Server version:\n{row[0]}")
    
    # Get and print database names
    print("\nDatabases in this SQL Server:")
    cursor.execute("SELECT name FROM sys.databases")
    for row in cursor.fetchall():
        print(row.name)

    

       # Fetch all rows
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
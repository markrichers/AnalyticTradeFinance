import pyodbc

# Connection parameters
server = 'localhost'
port = '1433'
database = 'Mark_Db'
username = 'WM6'
password = 'WM6'

# Create the connection string
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server},{port};DATABASE={database};UID={username};PWD={password}'

try:
    # Establish the connection
    conn = pyodbc.connect(conn_str)
    
    # Create a cursor
    cursor = conn.cursor()
    
    print("Successfully connected to Mark_Db!")

    # Create tables
    cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Customer')
    CREATE TABLE Customer (
        CustomerID INT PRIMARY KEY,
        Name NVARCHAR(100),
        Address NVARCHAR(200),
        ContactNumber NVARCHAR(20),
        Email NVARCHAR(100)
    )
    ''')

    cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Product')
    CREATE TABLE Product (
        ProductID INT PRIMARY KEY,
        Name NVARCHAR(100),
        Description NVARCHAR(MAX),
        QuantityAvailable INT,
        UnitPrice DECIMAL(10, 2)
    )
    ''')

    cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Vehicle')
    CREATE TABLE Vehicle (
        VehicleID INT PRIMARY KEY,
        Type NVARCHAR(50),
        Capacity DECIMAL(10, 2),
        AvailabilityStatus NVARCHAR(20)
    )
    ''')

    cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Route')
    CREATE TABLE Route (
        RouteID INT PRIMARY KEY,
        Origin NVARCHAR(100),
        Destination NVARCHAR(100),
        Distance DECIMAL(10, 2),
        EstimatedTravelTime TIME
    )
    ''')

    cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Order')
    CREATE TABLE [Order] (
        OrderID INT PRIMARY KEY,
        CustomerID INT,
        OrderDate DATE,
        Status NVARCHAR(20),
        FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
    )
    ''')

    cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'OrderProduct')
    CREATE TABLE OrderProduct (
        OrderID INT,
        ProductID INT,
        Quantity INT,
        PRIMARY KEY (OrderID, ProductID),
        FOREIGN KEY (OrderID) REFERENCES [Order](OrderID),
        FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
    )
    ''')

    cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Shipment')
    CREATE TABLE Shipment (
        ShipmentID INT PRIMARY KEY,
        OrderID INT,
        VehicleID INT,
        RouteID INT,
        ShipmentDate DATE,
        EstimatedDeliveryDate DATE,
        ActualDeliveryDate DATE,
        Status NVARCHAR(20),
        FOREIGN KEY (OrderID) REFERENCES [Order](OrderID),
        FOREIGN KEY (VehicleID) REFERENCES Vehicle(VehicleID),
        FOREIGN KEY (RouteID) REFERENCES Route(RouteID)
    )
    ''')

    conn.commit()
    print("Logistics tables created successfully in Mark_Db!")

    # Get and print table names
    print("\nTables in Mark_Db:")
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE'")
    for row in cursor.fetchall():
        print(row.table_name)

except pyodbc.Error as e:
    print(f"Error connecting to the database: {e}")

finally:
    # Close the connection
    if 'conn' in locals():
        conn.close()
        print("\nDatabase connection closed.")
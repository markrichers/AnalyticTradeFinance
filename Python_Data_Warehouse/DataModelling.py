from sqlalchemy import create_engine, inspect, Column, Integer, String, ForeignKey, DECIMAL, Date, Time
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# Use declarative_base from sqlalchemy.orm (SQLAlchemy 2.0+)
Base = declarative_base()

# Customer table
class Customer(Base):
    __tablename__ = 'Customer'
    CustomerID = Column(Integer, primary_key=True)
    Name = Column(String(100))
    Address = Column(String(200))
    ContactNumber = Column(String(20))
    Email = Column(String(100))

    orders = relationship("Order", back_populates="customer")

# Product table
class Product(Base):
    __tablename__ = 'Product'
    ProductID = Column(Integer, primary_key=True)
    Name = Column(String(100))
    Description = Column(String)  # NVARCHAR(MAX) maps to String
    QuantityAvailable = Column(Integer)
    UnitPrice = Column(DECIMAL(10, 2))

# Vehicle table
class Vehicle(Base):
    __tablename__ = 'Vehicle'
    VehicleID = Column(Integer, primary_key=True)
    Type = Column(String(50))
    Capacity = Column(DECIMAL(10, 2))
    AvailabilityStatus = Column(String(20))

# Route table
class Route(Base):
    __tablename__ = 'Route'
    RouteID = Column(Integer, primary_key=True)
    Origin = Column(String(100))
    Destination = Column(String(100))
    Distance = Column(DECIMAL(10, 2))
    EstimatedTravelTime = Column(Time)

# Order table
class Order(Base):
    __tablename__ = 'Order'
    OrderID = Column(Integer, primary_key=True)
    CustomerID = Column(Integer, ForeignKey('Customer.CustomerID'))
    OrderDate = Column(Date)
    Status = Column(String(20))

    customer = relationship("Customer", back_populates="orders")
    order_products = relationship("OrderProduct", back_populates="order")
    shipments = relationship("Shipment", back_populates="order")

# OrderProduct (junction table between Order and Product)
class OrderProduct(Base):
    __tablename__ = 'OrderProduct'
    OrderID = Column(Integer, ForeignKey('Order.OrderID'), primary_key=True)
    ProductID = Column(Integer, ForeignKey('Product.ProductID'), primary_key=True)
    Quantity = Column(Integer)

    order = relationship("Order", back_populates="order_products")
    product = relationship("Product")

# Shipment table
class Shipment(Base):
    __tablename__ = 'Shipment'
    ShipmentID = Column(Integer, primary_key=True)
    OrderID = Column(Integer, ForeignKey('Order.OrderID'))
    VehicleID = Column(Integer, ForeignKey('Vehicle.VehicleID'))
    RouteID = Column(Integer, ForeignKey('Route.RouteID'))
    ShipmentDate = Column(Date)
    EstimatedDeliveryDate = Column(Date)
    ActualDeliveryDate = Column(Date)
    Status = Column(String(20))

    order = relationship("Order", back_populates="shipments")
    vehicle = relationship("Vehicle")
    route = relationship("Route")


# Connection parameters
server = 'localhost'
port = '1433'
database = 'Mark_Db'
username = 'WM6'
password = 'WM6'

# Create an engine to connect to your database
connection_string = f'mssql+pyodbc://{username}:{password}@{server}:{port}/{database}?driver=ODBC+Driver+17+for+SQL+Server'
engine = create_engine(connection_string)

# Inspect the database to check if tables already exist
inspector = inspect(engine)

def check_and_create_tables():
    tables_needed = ['Customer', 'Product', 'Vehicle', 'Route', 'Order', 'OrderProduct', 'Shipment']
    existing_tables = inspector.get_table_names()

    # Check which tables do not exist
    missing_tables = [table for table in tables_needed if table not in existing_tables]

    if missing_tables:
        print(f"Tables missing: {', '.join(missing_tables)}. Creating tables...")
        Base.metadata.create_all(engine)
    else:
        print("All tables already exist, no need to create them.")

# Call the function to check and create tables
check_and_create_tables()

# Create a session for interacting with the database
Session = sessionmaker(bind=engine)
session = Session()

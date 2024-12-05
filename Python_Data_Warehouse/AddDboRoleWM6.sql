SELECT SCHEMA_NAME() AS DefaultSchema; 

SELECT HAS_PERMS_BY_NAME('dbo','SCHEMA','SELECT') AS HasSelectPermOnDBO;

GRANT SELECT ON SCHEMA::dbo TO [WM6];

EXEC sp_addrolemember 'db_datareader','WM6';

SELECT SUSER_SNAME(owner_sid) AS DatabaseOwner 
FROM sys.databases 
WHERE name = 'Mark_Db';

-- Grant DBo
USE master;
GO
GRANT VIEW ANY DEFINITION TO [WM6];
GRANT VIEW SERVER STATE TO [WM6];
USE [Mark_Db];

-- Check if the user exists and remove from roles if it does
IF EXISTS (SELECT * FROM sys.database_principals WHERE name = 'WM6')
BEGIN
    -- Remove WM6 from db_datareader role
    ALTER ROLE [db_datareader] DROP MEMBER [WM6];

    -- Remove WM6 from db_datawriter role
    ALTER ROLE [db_datawriter] DROP MEMBER [WM6];

    -- Drop the user WM6 from the database
    DROP USER [WM6];

    PRINT 'User WM6 has been removed from roles and dropped from the database.';
END
ELSE
END
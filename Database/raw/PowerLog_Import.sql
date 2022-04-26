ALTER PROC [raw].Powerlog_Import(@Name VARCHAR(255))
AS
BEGIN

	-- TO DO: Logging
	
	DECLARE @File VARCHAR(1024);
	DECLARE @SQL VARCHAR(MAX);
	DECLARE @TableName2Part VARCHAR(MAX);

	SET @File = 'C:\repo\PiExperiments\esp32\PowerLogger\DataFiles\' + @Name + '.txt';
	SET @TableName2Part = '[raw].' + @Name

	-- Check if table exists before dropping
	SET @SQL = 'DROP TABLE ' + @TableName2Part;  EXEC(@SQL);

	SET @SQL = 'CREATE TABLE ' + @TableName2Part + ' (
		  DateTimeStamp VARCHAR(50) NOT NULL
		, RawValue VARCHAR(50) NOT NULL
	)';
	EXEC(@SQL);


	SET @SQL = 'BULK INSERT ' + @TableName2Part + '
	   FROM ''' + @File + '''
	   WITH (
			  FIRSTROW = 2
			, FIELDTERMINATOR = '',''
			, ROWTERMINATOR = ''' + CHAR(10) + '''
			);'
	EXEC(@SQL);

	-- SET @SQL = 'SELECT * FROM ' + @TableName2Part; EXEC(@SQL);

END;

-- EXEC [raw].Powerlog_Import 'powerlog_20220404213256'
-- EXEC [raw].Powerlog_Import 'powerlog_20220405184536'
-- EXEC [raw].Powerlog_Import 'powerlog_20220407212748'
-- EXEC [raw].Powerlog_Import 'powerlog_20220422173254'

-- SELECT * FROM raw.powerlog_20220404213256
-- SELECT * FROM raw.powerlog_20220405184536
-- SELECT * FROM raw.powerlog_20220407212748
-- SELECT * FROM raw.powerlog_20220422173254
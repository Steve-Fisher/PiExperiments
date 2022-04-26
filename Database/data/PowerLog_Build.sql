ALTER PROCEDURE [data].PowerLog_Build
AS
BEGIN

	DROP TABLE [data].PowerLog;
	
	CREATE TABLE [data].PowerLog (
		  DateTimeStamp DATETIME2(0) NOT NULL
		, [Value] NUMERIC(8,2)
	);

	INSERT INTO [data].PowerLog SELECT DateTimeStamp, RawValue FROM [raw].powerlog_20220404213256;
	INSERT INTO [data].PowerLog SELECT DateTimeStamp, RawValue FROM [raw].powerlog_20220405184536;
	INSERT INTO [data].PowerLog SELECT DateTimeStamp, RawValue FROM [raw].powerlog_20220407212748;
	INSERT INTO [data].PowerLog SELECT DateTimeStamp, RawValue FROM [raw].powerlog_20220422173254;

	CREATE UNIQUE CLUSTERED INDEX uci ON [data].PowerLog(DateTimeStamp) WITH(DATA_COMPRESSION=PAGE);

END

-- EXEC [data].PowerLog_Build
-- SELECT * FROM [data].PowerLog
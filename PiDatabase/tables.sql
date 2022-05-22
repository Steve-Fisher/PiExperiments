CREATE TABLE logheader (
    logID INT NOT NULL,
    [Desc] VARCHAR(50) NOT NULL,
    API_URL VARCHAR(50) NULL,
    interval_secs INT NULL
);

CREATE TABLE log(
    DateTimeStamp DATETIME NOT NULL,
    LogID INT NOT NULL,
    [Value] NUMERIC (14,6) NULL
);
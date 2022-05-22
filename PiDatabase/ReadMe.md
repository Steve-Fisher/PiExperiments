# Making and using a Raspberry Pi database server

Decided to use [SQLite](https://sqlite.org/index.html).  Confirmation this as a sensible choice in [this article](https://chipwired.com/databases-for-raspberry-pi/).

# Setup
```sudo apt update```

```sudo apt install sqlite3```

```sqlite3``` to confirm installation.  Get:
```SQLite version 3.27.2 2019-02-15 16:06:06
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen a persistent database.
sqlite> ▯
```

(```.exit``` to leave the sqlite prompt)

Create a persistent database called logger: ```sqlite3 logger.db```

```
CREATE TABLE test(Message VARCHAR(1024));
INSERT INTO test VALUES('Hello from SQLite');
SELECT * FROM test;
```

SQLite is a local database.  Meaning you cannot connect to it directly over a network.  However, we can use the python library sqlite-web to run a local webserver which can act as a browser based window in to the local database.  Based on [this stackoverflow question](https://stackoverflow.com/questions/8357496/access-sqlite-from-a-remote-server)

```pip install sqlite-web```

```PATH=$PATH:/home/pi/.local/bin```

```sqlite_web --host 192.168.0.165 logger.db```

This is then accessible over the (home) network via http://192.168.0.165:8080

## Logging tables ##
Going to put the code for this is a separate .sql file in this repo








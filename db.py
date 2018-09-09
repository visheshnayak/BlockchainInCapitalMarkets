import sqlite3
conn = sqlite3.connect('test.db')
print("Opened database successfully")

# conn.execute('''CREATE TABLE USER_NAME
#          (USER_ID INTEGER PRIMARY KEY    AUTOINCREMENT,
#          UNAME           CHAR(64)    NOT NULL, 
#          PASSWORD            CHAR(128)    NOT NULL,
#          TYPE_OF_USER        CHAR(10) NOT NULL);''')

conn.execute('''DROP TABLE POOL_OF_AWESOMENESS''')  

conn.execute('''CREATE TABLE POOL_OF_AWESOMENESS
         (ORDER_ID INTEGER PRIMARY KEY AUTOINCREMENT,
         FLAG           CHAR(1)    NOT NULL, 
         BUYER_ID      INTEGER ,
         SELLER_ID     INTEGER ,
         QUANTITY          INTEGER    NOT NULL,
         PRICE          REAL NOT NULL, 
         STATUS         CHAR(1) NOT NULL,
         MOD_DATE_TIME        TEXT)''')  

print("Table created successfully")
conn.close()
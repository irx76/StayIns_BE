import pymysql

conn=pymysql.connect(
                            host="127.0.0.1",
                            database= "stayins",
                            user= "root",
                            password= "",
                            port=8889,
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor
                            ) #if not there, it will be created

cursor=conn.cursor()

# create_Locations_table_query="""CREATE TABLE Location(
# LOCATION VARCHAR(255) PRIMARY KEY
# )"""

# cursor.execute(create_Locations_table_query)




conn.close()
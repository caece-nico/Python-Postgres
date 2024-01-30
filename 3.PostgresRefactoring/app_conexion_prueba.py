import psycopg2 
import os
from dotenv import load_dotenv

load_dotenv()

try:
    connection = psycopg2.connect(host = 'localhost', 
                                database=os.environ.get('USER_DB'),
                                user=os.environ.get('USER_NAME'),
                                password=os.environ.get('USER_PASS'),
                                port=5432
                                )

    cur = connection.cursor()


    cur.execute("select version();")

    print(cur.fetchone())

    connection.close()
except Exception as error:
    print(error)



import pymysql, os, sys
from dotenv import load_dotenv

load_dotenv()
host = os.getenv('DB_HOST', '127.0.0.1')
user = os.getenv('DB_USER', 'root')
password = os.getenv('DB_PASSWORD', 'password')
db = os.getenv('DB_NAME', 'saveabite')

try:
    conn = pymysql.connect(host=host, user=user, password=password, db=db, connect_timeout=3)
    conn.close()
    print('OK')
    sys.exit(0)
except Exception as e:
    print('FAIL', e)
    sys.exit(1)

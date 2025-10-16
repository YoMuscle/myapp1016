import psycopg2
import sys

DB_URL = "postgresql://myapp1016_user:MlSmsd0ZiVrZagCJj7ZNuJi6yY4e3NbB@dpg-d3o9o7t6ubrc73a919bg-a.oregon-postgres.render.com/myapp1016"

try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    result = cur.fetchone()
    print("資料庫連線成功，查詢結果：", result)
    cur.close()
    conn.close()
except Exception as e:
    print("資料庫連線失敗：", e)
    sys.exit(1)

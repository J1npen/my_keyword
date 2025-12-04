import pymysql

def connect_database():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='keyword',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except pymysql.MySQLError as e:
        print(f"Database connection failed: {e}")
        return None

def main():
    conn = connect_database()
    if not conn:
        return
    try:
        with conn.cursor() as cursor:
            cursor.execute('SHOW DATABASES')
            feedback = cursor.fetchall()
            for db in feedback:
                print(db)
    except pymysql.MySQLError as e:
        print(f"Query failed: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    main()
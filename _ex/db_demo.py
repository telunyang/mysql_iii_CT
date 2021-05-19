import pymysql

# 資料庫連線
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='my_db',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

# 取得 cursor 物件，進行 CRUD
cursor = connection.cursor()

try:
    # 寫入資料
    # sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
    # cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    # 查詢資料
    sql = "SELECT * FROM `categories`"
    cursor.execute(sql)

    # 查詢結果列數大於0 ，代表有資料
    if cursor.rowcount > 0:
        # 將查詢結果轉成 list 型態 (list 裡頭元素都是 dict)
        results = cursor.fetchall()
        # 迭代取得資料 (dict 型態)
        for result in results:
            print(result)
    else:
        print("rowcount: 0")

    # 提交 SQL 執行結果
    connection.commit()
except Exception as e:
    # 回滾
    connection.rollback()
    print("SQL 執行失敗")
    print(e)

# 釋放 cursor
cursor.close()

# 關閉資料庫連線
connection.close()
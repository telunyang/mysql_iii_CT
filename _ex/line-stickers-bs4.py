import requests, pprint, os, json, pprint
from bs4 import BeautifulSoup
import pymysql

    
#放貼圖資訊用
listLineStickers = []

# 自訂標頭
my_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
}

# 官方 LINE 貼圖的網址
url = 'https://store.line.me/stickershop/product/17555/zh-Hant'

# 將自訂標頭加入 GET 請求中
response = requests.get(url, headers = my_headers)

# 建立 soup 物件
soup = BeautifulSoup(response.text, 'lxml')

'''
備註:
1. soup.select()：回傳的結果是元素集合（list 型態，BeautifulSoup ResultSet）
2. soup.select_one()：回傳的結果是單一元素（BeautifulSoup Result）
'''
# 取得放置貼圖的 li 元素 (list 型態)
li_elements = soup.select("ul.mdCMN09Ul.FnStickerList > li.mdCMN09Li.FnStickerPreviewItem")

# 逐一取得 li 元素中的 data-preview 資訊
for li in li_elements:
    # 取得 data-preview 屬性的值(字串)
    strJson = li['data-preview'] # 另一種寫法：li.get("data-preview")
    
    #把屬性的值(字串)轉成物件 
    obj = json.loads(strJson)
    
    # 將重要資訊放置在 list 當中，幫助我們稍候進行資料下載與儲存
    listLineStickers.append({
        "id": obj['id'],
        "link": obj['staticUrl']
    })

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
    # 建立儲存圖片的資料夾，不存在就新增
    folderPath = 'line_stickers'
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

    # 定義 SQL 語法
    sql = "INSERT INTO `line-stickers` (`id`, `ext`, `category`, `link`) VALUES (%s, %s, %s, %s)"
    
    # 迭代走訪 list 當中的 dict
    for obj in listLineStickers: 
        # 執行 SQL 語法
        cursor.execute( sql, (obj['id'], 'png', 'stickershop', obj['link']) )

        # 下載
        os.system(f"curl {obj['link']} -o {folderPath}/{obj['id']}.png")
        print(f"貼圖ID: {obj['id']}, 下載連結: {obj['link']}")

    # 提交 SQL 執行結果
    connection.commit()
except Exception as e:
    # 回滾
    connection.rollback()
    print("SQL 執行失敗")
    print(e)

# 關閉 cursor
cursor.close()

# 關閉 資料庫連線
connection.close()
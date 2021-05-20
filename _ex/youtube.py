'''
匯入套件
'''
# 操作 browser 的 API
from selenium import webdriver

# 處理逾時例外的工具
from selenium.common.exceptions import TimeoutException

# 面對動態網頁，等待某個元素出現的工具，通常與 exptected_conditions 搭配
from selenium.webdriver.support.ui import WebDriverWait

# 搭配 WebDriverWait 使用，對元素狀態的一種期待條件，若條件發生，則等待結束，往下一行執行
from selenium.webdriver.support import expected_conditions as EC

# 期待元素出現要透過什麼方式指定，通常與 EC、WebDriverWait 一起使用
from selenium.webdriver.common.by import By

# 強制等待 (執行期間休息一下)
from time import sleep

# 整理 json 使用的工具
import json

# 執行 command 的時候用的
import os

# 資料庫 CRUD 工具
import pymysql

'''
Selenium with Python 中文翻譯文檔
參考網頁：https://selenium-python-zh.readthedocs.io/en/latest/index.html
selenium 啓動 Chrome 的進階配置參數
參考網址：https://stackoverflow.max-everyday.com/2019/12/selenium-chrome-options/
Mouse Hover Action in Selenium
參考網址：https://www.toolsqa.com/selenium-webdriver/mouse-hover-action/
'''
# 啟動瀏覽器工具的選項
options = webdriver.ChromeOptions()
# options.add_argument("--headless")                #不開啟實體瀏覽器背景執行
options.add_argument("--start-maximized")         #最大化視窗
options.add_argument("--incognito")               #開啟無痕模式
options.add_argument("--disable-popup-blocking ") #禁用彈出攔截

# 使用 Chrome 的 WebDriver (含 options)
driver = webdriver.Chrome( options = options )

# driver.set_window_size(1200, 960) #視窗大小設定 (寬，高)
# driver.maximize_window() #視窗最大化
# driver.minimize_window() #視窗最小化

# 資料庫連線
connection = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'my_db',
    charset = 'utf8mb4',
    cursorclass = pymysql.cursors.DictCursor
)

# 取得 cursor 物件，進行 CRUD
cursor = connection.cursor()

# 放置爬取的資料
listData = []

# 準備在 YouTube 搜尋的關鍵字
keyword = "蕭敬騰"

'''
以 function 名稱，作為爬蟲流程
'''

# 走訪頁面
def visit():
    driver.get('https://www.youtube.com/');

# 輸入關鍵字
def search():
    # 輸入名稱
    txtInput = driver.find_element(By.CSS_SELECTOR, "input#search")
    txtInput.send_keys(keyword)
    
    #按下送出
    btnInput = driver.find_element(By.CSS_SELECTOR, "button#search-icon-legacy")
    btnInput.click()

    # 等待一下
    sleep(2)
    
# 篩選 (選項)
def filterFunc():
    try:
        # 等待篩選元素出現
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located( 
                (
                    By.CSS_SELECTOR, 
                    "yt-formatted-string#text.style-scope.ytd-toggle-button-renderer.style-text"
                ) 
            )
        )

        #按下篩選元素，使項目浮現
        driver.find_element(
            By.CSS_SELECTOR, 
            "yt-formatted-string#text.style-scope.ytd-toggle-button-renderer.style-text"
        ).click()

        # 等待一下
        sleep(2)

        # 按下選擇的項目
        driver.find_elements(
            By.CSS_SELECTOR, 
            "yt-formatted-string.style-scope.ytd-search-filter-renderer"
        )[10].click()

        # 等待一下
        sleep(2)
        
    except TimeoutException:
        print("等待逾時，即將關閉瀏覽器…")
        sleep(3)
        driver.quit()
        
# 滾動頁面
def scroll():
    # 瀏覽器內部的高度
    innerHeightOfWindow = 0
    
    # 當前捲動的量(高度)
    totalOffset = 0
    
    # 在捲動到沒有元素動態產生前，持續捲動
    while totalOffset <= innerHeightOfWindow:
        # 每次移動高度
        totalOffset += 500
        
        # 捲動的 js code
        js_scroll = '''(
            function (){{
                window.scrollTo({{
                    top:{}, 
                    behavior: 'smooth' 
                }});
            }})();'''.format(totalOffset)
        
        # 執行 js code
        driver.execute_script(js_scroll)
        
        # 透過執行 js 語法來取得捲動後的當前總高度
        innerHeightOfWindow = driver.execute_script(
            'return window.document.documentElement.scrollHeight;'
        )
        
        # 印出捲動距離
        print("innerHeightOfWindow: {}, totalOffset: {}".format(innerHeightOfWindow, totalOffset))

        # 強制等待
        sleep(2)
        
        # 為了實驗功能，捲動超過一定的距離，就結束程式
        # if totalOffset >= 1800:
        #     break

# 分析頁面元素資訊
def parse():
    # 取得主要元素的集合
    ytd_video_renderers = driver.find_elements(
        By.CSS_SELECTOR, 
        'ytd-video-renderer.style-scope.ytd-item-section-renderer')
    
    # 逐一檢視元素
    for element in ytd_video_renderers:
        # 印出分隔文字
        print("=" * 30)
        
        # 取得圖片連結
        img = element.find_element(
            By.CSS_SELECTOR, 
            "ytd-thumbnail.style-scope.ytd-video-renderer img#img")
        imgSrc = img.get_attribute('src')
        print(imgSrc)
        
        # 取得資料名稱
        a = element.find_element(By.CSS_SELECTOR, "a#video-title")
        aTitle = a.text
        print(aTitle)
        
        # 取得 YouTube 連結
        aLink = a.get_attribute('href')
        print(aLink)

        # 取得 影音 ID
        youtube_id = aLink.split("v=")[1]
        
        # 放資料到 list 中
        listData.append({
            "youtube_id": youtube_id,
            "title": aTitle,
            "link": aLink,
            "img": imgSrc
        })

# 將 list 存成 json
def saveJson():
    fp = open("youtube.json", "w", encoding='utf-8')
    fp.write( json.dumps(listData, ensure_ascii=False) )
    fp.close()

# 將取得資料寫入資料庫
def saveDB():
    try:
        # 開啟 json 檔案
        fp = open("youtube.json", "r", encoding='utf-8')
        
        #取得 json 字串
        strJson = fp.read()
        
        # 關閉檔案
        fp.close()
        
        # 將 json 轉成 list (裡面是 dict 集合)
        listResult = json.loads(strJson)

        # 決定資料寫入的語法
        sql = "INSERT INTO `youtube` (`youtube_id`, `keyword`, `title`, `link`, `img`) VALUES (%s, %s, %s, %s, %s)"
        
        # ??????
        for index, obj in enumerate(listResult):
            cursor.execute( 
                sql, 
                (
                    obj['youtube_id'], keyword, obj['title'], obj['link'], obj['img']
                ) 
            )
            
        # 提交 SQL 執行結果
        connection.commit()
    except Exception as e:
        # 回滾
        connection.rollback()
        print("SQL 執行失敗")
        print(e)

# 關閉瀏覽器、資料庫等資源
def close():
    driver.quit()
    cursor.close()
    connection.close()

# 主程式
if __name__ == '__main__':
    visit()
    search()
    filterFunc()
    scroll()
    parse()
    saveJson()
    saveDB()
    close()
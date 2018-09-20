# 專案名稱

中山大學網路選課系統

## 目的

取代原本學校極為老舊的選課系統，利用爬蟲的方式，重建一個較接近現代的網頁，並增加便利的功能優化與加速選課流程。

## 開始

1. 自備一個伺服器環境，內含 Python 3.6、MySQL 資料庫，以下以 Ubuntu、MySQL 為例。

2. 在您的資料庫中，建立一個新的資料庫。

3. 將專案中的 tables.sql 放入新建立的資料庫中執行。

4. 修改 ClassesDB.py 中，連接資料庫的名字帳號與密碼。

5. 安裝此專案所需的 Python 套件。

    ```
    opencc-python
    pymysql-python
    BeautifulSoup4
    flask
    ```

6. 執行以下去學校網站抓去所有課程，需要花費數十分鐘。

    ```
    clear && python crawl.py
    ```

    執行中必須確保資料庫能連線，才能將抓取的課程直接塞入資料庫。

7. 執行以下開啟整體的爬蟲伺服器，開始遠離破舊的中山大學網路選課系統。

    ```
    clear && python Web.py
    ```

## 範例

http://selcrs.ga

## 版本

Version 2.0

## 作者

Hua777

## License

MIT

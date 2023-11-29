import json
import os
import sqlite3
from typing import List, Tuple

def read_json(df: str) -> dict:
    """
    從文件中讀取 JSON 數據。

    參數:
    - df (str): JSON 文件的文件路徑。

    返回:
    dict: JSON 文件的內容。
    """
    with open(df, 'r', encoding="utf-8") as f:
        file_content = json.load(f)
        return file_content
        
def save_AP(file: List[dict]) -> Tuple[List[str], List[str]]:
    """
    從使用者數據列表中提取帳號和密碼。

    參數:
    - file (List[dict]): 包含使用者數據的字典列表。

    返回:
    Tuple[List[str], List[str]]: 包含帳號和密碼的列表的元組。
    """
    accounts = []
    passwords = []

    for user_data in file:
        accounts.append(user_data["帳號"])
        passwords.append(user_data["密碼"])

    return accounts, passwords

def signIn(account: List[str], password: List[str]) -> None:
    """
    使用給定的帳號和密碼登入。

    參數:
    - account (List[str]): 有效帳號名稱的列表。
    - password (List[str]): 相應密碼的列表。

    返回:
    None
    """
    input_Account = input("請輸入帳號 : ")
    input_Password = input("請輸入密碼 : ")
    
    if (
        (input_Account == account[0] or input_Account == account[1]) and
        (input_Password == password[0] or input_Password == password[1])
    ):
        menu()
    else:
        print("=>帳密錯誤，程式結束")
        print()
        os._exit(0)

def menu() -> None:
    """
    顯示菜單選項。

    返回:
    None
    """
    print("""
---------- 選單 ----------
0 / Enter 離開
1 建立資料庫與資料表
2 匯入資料
3 顯示所有紀錄
4 新增記錄
5 修改記錄
6 查詢指定手機
7 刪除所有記錄
--------------------------
          """)

def create_SQL_database() -> sqlite3.Cursor:
    """
    建立 SQLite 資料庫連線並返回游標。

    返回:
    sqlite3.Cursor: SQLite 資料庫的游標。
    """
    database = sqlite3.connect('wanghong.db')
    cursorObj = database.cursor()
    return cursorObj

def open_txt() -> Tuple[List[str], List[str], List[str]]:
    """
    從文本文件中讀取數據。

    返回:
    Tuple[List[str], List[str], List[str]]: 姓名、性別和手機號碼的列表。
    """
    with open('members.txt', 'r', encoding="utf-8") as txt_read:
        name_list = []
        sex_list = []
        phone_list= []

        line = txt_read.readline().strip()  

        while line:
            items = line.split(",")

            name_list.append(items[0])
            sex_list.append(items[1])
            phone_list.append(items[2])
        
            line = txt_read.readline().strip()

        return name_list, sex_list, phone_list
    
def add_spaces_name(input_str: str) -> str:
    """
    為名稱添加空格，使其達到指定的長度。

    參數:
    - input_str (str): 要處理的輸入字串。

    返回:
    str: 處理後的字串。
    """
    spaces = 12 - len(input_str)*2
    input_str = input_str + (" "*spaces)
    return input_str

def add_spaces_sex(input_str: str) -> str:
    """
    為性別添加空格，使其達到指定的長度。

    參數:
    - input_str (str): 要處理的輸入字串。

    返回:
    str: 處理後的字串。
    """
    spaces = 6 - len(input_str)*2
    input_str = input_str + (" "*spaces)
    return input_str

def add_data_to_database(name: str, sex: str, phone: str) -> None:
    """
    向資料庫中添加新記錄。

    參數:
    - name (str): 姓名。
    - sex (str): 性別。
    - phone (str): 手機號碼。

    返回:
    None
    """
    cursorObj = create_SQL_database()
    cursorObj.execute("INSERT INTO members (mname, msex, mphone) VALUES (?, ?, ?)",
            (name, sex, phone))
    cursorObj.connection.commit()
    cursorObj.close()

def show_log() -> List[Tuple[str, str, str]]:
    """
    顯示資料庫中的所有記錄。

    返回:
    List[Tuple[str, str, str]]: 包含所有記錄的元組列表。
    """
    cursorObj = create_SQL_database()
    cursor = cursorObj.execute("SELECT * from members")
    result_all = cursor.fetchall()
    cursorObj.close()

    if not result_all:
        print("=>查無資料")
        return []  # 如果沒有資料，返回一個空列表
    else:
        print("""
姓名       性別  手機
-----------------------------1
        """)
        for item in result_all:
            print(f'{add_spaces_name(item[0])}{add_spaces_sex(item[1])}{(item[2])}')
        return result_all
    
def modify_record() -> None:
    """
    修改資料庫中的記錄。

    返回:
    None
    """
    cursorObj = create_SQL_database()  
    input_set_logName = input("請輸入想修改記錄的姓名: ")
    result = show_log()
    found_record = None

    for item in result:
        if input_set_logName == item[0]:
            found_record = item
            break

    if found_record:
        input_set_logSex = input("請輸入想修改記錄的性別: ")
        input_set_logPhone = input("請輸入要改變的手機: ")

        # 顯示更改前的資料
        print("\n原資料: ")
        print(f'姓名:{found_record[0]}，性別:{found_record[1]}，電話:{found_record[2]}')
        print("=>異動 1 筆記錄")
        cursorObj.execute('UPDATE members SET msex = ?, mphone = ? WHERE mname = ?', (input_set_logSex, input_set_logPhone, input_set_logName))
        print("\n修改後資料: ")
        print(f'姓名:{input_set_logName}，性別:{input_set_logSex}，電話:{input_set_logPhone}')
        cursorObj.connection.commit()
        cursorObj.close()
        menu()
    else:
        print("=>未找到指定姓名的記錄")

    cursorObj.close()  # 在這裡關閉連接
            
def found_recode() -> None:
    """
    查找資料庫中的記錄。

    返回:
    None
    """
    cursorObj = create_SQL_database()  
    result = show_log()
    input_set_logPhone = input("請輸入想修改記錄的手機: ")
    found_record = None
    for item in result:
        if input_set_logPhone == item[2]:
            found_record = item
            break

    if found_record:
        # 顯示更改前的資料
        print("""
姓名       性別  手機
-----------------------------2
    """)
        print(f'{add_spaces_name(item[0])}{add_spaces_sex(item[1])}{(item[2])}')
    else:
        print("查無此電話!請重新輸入")
        
def delete_database() -> None:
    """
    刪除資料庫中的所有記錄。

    返回:
    None
    """
    cursorObj = create_SQL_database()  
    result = show_log()

    if result:
        deleted_records = len(result)  # 記錄要刪除的記錄數
        cursorObj.execute('DELETE FROM members')
        print(f"=>異動 {deleted_records} 筆記錄")
    else:
        print("=>查無資料")

    cursorObj.connection.commit()
    cursorObj.close()

def switch(choice: str) -> None:
    """
    根據用戶的選擇執行相應的操作。

    參數:
    - choice (str): 用戶的選擇。

    返回:
    None
    """
    if choice == "0": #Exit
        print()
        os._exit(0)
        
    elif choice == "1": #create_SQL_database
        cursorObj = create_SQL_database()
        print("=>資料庫已建立")
        menu()
        return cursorObj
    
    elif choice == "2":
        cursorObj = create_SQL_database()
        name_list, sex_list, phone_list = open_txt()
       
        cursorObj.execute("DROP TABLE IF EXISTS members")
        cursorObj.execute("CREATE TABLE IF NOT EXISTS members (mname TEXT, msex TEXT, mphone TEXT)")

        for i in range(len(name_list)):
            cursorObj.execute("INSERT INTO members (mname, msex, mphone) VALUES (?, ?, ?)",
                            (name_list[i], sex_list[i], phone_list[i]))
        print(f'=>異動 {len(name_list)} 筆記錄')

        # 將數據提交到數據庫
        cursorObj.connection.commit()
        cursorObj.close()
        menu()

    elif choice == "3":
        show_log()
        menu()

    elif choice == "4":

        name = input("請輸入姓名: ")
        sex = input("請輸入性別: ")
        phone = input("請輸入手機: ")
        add_data_to_database(name,sex,phone)
        print("=>異動 1 筆紀錄")
        menu()

    elif choice == "5":
        modify_record()

    elif choice == "6":
        found_recode()
        menu()

    elif choice == "7":
        delete_database()
        menu()

    else:
        print("=>無效的選擇")

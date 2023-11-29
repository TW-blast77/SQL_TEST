from modu import lib

def main():
    df = "./pass.json"
    json_df = lib.read_json(df)
    account, password = lib.save_AP(json_df)
    lib.signIn(account,password)

    while(True):
        choice = input("請輸入您的選擇 [0-7]: ")
        lib.switch(choice)
        lib.menu()
main()
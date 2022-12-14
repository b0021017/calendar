# YIC 情報ビジネス専門学校
#  情報工学科 2年
#     南野 凌志 (B0021017@ib.yic.ac.jp)
#

import pymysql
import tkinter
from YicDiary import YicDiary

WEEK = ['日', '月', '火', '水', '木', '金', '土']
WEEK_COLOUR = ['red', 'black', 'black', 'black','black', 'black', 'blue']
actions = ('学校','試験', '課題', '行事', '就活', 'アルバイト','旅行')

class Login():
    '''ログインを制御するクラス'''

    def __init__(self, master, main):
        '''コンストラクタ
            master:ログイン画面を配置するウィジェット
            body:アプリ本体のクラスのインスタンス
        '''

        self.master = master

        # アプリ本体のクラスのインスタンスをセット
        self.main = main

        # ログイン関連のウィジェットを管理するリスト
        self.widgets = []

        # ログイン画面のウィジェット作成
        self.create_widgets()


    def create_widgets(self):
        '''ウィジェットを作成・配置する'''

        # ユーザー名入力用のウィジェット
        self.name_label = tkinter.Label(
            self.master,
            text="ユーザー名"
        )
        self.name_label.grid(
            row=0,
            column=0
        )
        self.widgets.append(self.name_label)

        self.name_entry = tkinter.Entry(self.master)
        self.name_entry.grid(
            row=0,
            column=1
        )
        self.widgets.append(self.name_entry)

        # パスワード入力用のウィジェット
        self.pass_label = tkinter.Label(
            self.master,
            text="パスワード"
        )
        self.pass_label.grid(
            row=1,
            column=0
        )
        self.widgets.append(self.pass_label)

        self.pass_entry = tkinter.Entry(
            self.master,
            show="*"
        )
        self.pass_entry.grid(
            row=1,
            column=1
        )
        self.widgets.append(self.pass_entry)

        # ログインボタン
        self.login_button = tkinter.Button(
            self.master,
            text="ログイン",
            command=self.login
        )
        self.login_button.grid(
            row=2,
            column=0,
            columnspan=2,
        )
        self.widgets.append(self.login_button)

        # 登録ボタン
        self.register_button = tkinter.Button(
            self.master,
            text="登録",
            command=self.register
        )
        self.register_button.grid(
            row=3,
            column=0,
            columnspan=2,
        )
        self.widgets.append(self.register_button)

        # ウィジェット全てを中央寄せ
        self.master.grid_anchor(tkinter.CENTER)

    def login(self):
        '''ログインを実行する'''

        # 入力された情報をEntryウィジェットから取得
        username = self.name_entry.get()
        password = self.pass_entry.get()

        if self.check(username, password):
            # ログインユーザー名を設定
            self.login_name = username

            self.success()
        else:
            self.fail()

    def check(self, username, password):
        '''
            入力されたユーザー情報が登録済みか確認する
            username:ユーザー名
            password:パスワード
            返却値:True(登録済み),False（未登録）
        '''
        print(password)
        # DB接続
        connection = pymysql.connect(host= '127.0.0.1',
                                     user='root',
                                     password='',
                                     db='april01',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            # トランザクション開始
            connection.begin()
    
            with connection.cursor() as cursor:
                
                cursor = connection.cursor()
        
                sql = "SELECT * FROM user WHERE user_name='{}' and user_password='{}';".format(username,password)
                print(sql)
                cursor.execute(sql)

                results = cursor.fetchone()
                print(results)
                self.login_id = results["user_ID"]
                #for i, row in enumerate(results):
                 #   print(i, row)
                  #  X = row['contents']
    
                   # lbl = tk.Label(self.r2_frame, text=X, font=('', 12))
                    #lbl.grid(row = i, column = 0)
                       #                lbl.place(x = 280, y = 100 + i * 30)
                        # ユーザー情報の有無をチェック
                if results:
                    ret = True
                else:
                    ret = False
                    
                return ret
            connection.commit()
    
    
    
        except Exception as e:
            print('error:', e)
            connection.rollback()
        finally:
            connection.close()

    def save(self, username, password):
        '''
            入力されたユーザー情報を登録する
            username:ユーザー名
            password:パスワード
        '''

        # DB接続
        self.connection = sqlite3.connect(DB_NAME)
        self.cursor = self.connection.cursor()

        # まだDBにテーブルがなければ作成
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS user_info (username text, password text)"
        )

        # 取得した情報をDBに追記
        self.cursor.execute("INSERT INTO user_info VALUES (?,?)", [username, password])

        # DBを保存
        self.connection.commit()

        # DB接続をクローズ
        self.connection.close()


    def register(self):
        '''ユーザー名とパスワードを登録する'''

        # 入力された情報をEntryウィジェットから取得
        username = self.name_entry.get()
        password = self.pass_entry.get()

        self.save(username, password)

    def fail(self):
        '''ログイン失敗時の処理を行う'''

        # 表示中のウィジェットを一旦削除
        for widget in self.widgets:
            widget.destroy()

        # "ログインに失敗しました"メッセージを表示
        self.message = tkinter.Label(
            self.master,
            text="ログインできませんでした",
            font=("",40)
        )
        self.message.place(
            x=self.master.winfo_width() // 2,
            y=self.master.winfo_height() // 2,
            anchor=tkinter.CENTER
        )

        # 少しディレイを入れてredisplayを実行
        self.master.after(1000, self.redisplay)

    def redisplay(self):
        '''ログイン画面を再表示する'''

        # "ログインできませんでした"メッセージを削除
        self.message.destroy()

        # ウィジェットを再度作成・配置
        self.create_widgets()

    def success(self):
        '''ログイン成功時の処理を実行する'''

        # 表示中のウィジェットを一旦削除
        for widget in self.widgets:
            widget.destroy()

        # "ログインに成功しました"メッセージを表示
        self.message = tkinter.Label(
            self.master,
            text="ログインに成功しました",
            font=("",40)
        )
        self.message.place(
            x=self.master.winfo_width() // 2,
            y=self.master.winfo_height() // 2,
            anchor=tkinter.CENTER
        )

        # 少しディレイを入れてredisplayを実行
        self.master.after(1000, self.main_start(self.login_name, self.login_id))

    def main_start(self, login_name, login_id):
        '''アプリ本体を起動する'''
        print(login_id)
        # "ログインに成功しました"メッセージを削除
        self.message.destroy()

        # アプリ本体を起動
        self.main.start(login_name)
        self.master.destroy()
        root = tkinter.Tk()
        YicDiary(root, login_name, login_id)
        root.mainloop()

class MainAppli():
    '''アプリ本体'''

    def __init__(self, master):
        '''コンストラクタ
            master:ログイン画面を配置するウィジェット
        '''

        self.master = master

        # ログイン完了していないのでウィジェットは作成しない

    def start(self, login_name):
        '''アプリを起動する'''

        # ログインユーザー名を表示する
        self.message = tkinter.Label(
            self.master,
            font=("",40),
            text=login_name + "でログイン中"
        )
        self.message.pack()

        # 必要に応じてウィジェット作成やイベントの設定なども行う

def Main():
    app = tkinter.Tk()
    
    # メインウィンドウのサイズ設定
    app.geometry("600x400")

    #タイトル
    app.title("ログイン画面")

    # アプリ本体のインスタンス生成
    main = MainAppli(app)
    
    # ログイン管理クラスのインスタンス生成
    login = Login(app, main)
    
    app.mainloop()


if __name__ == '__main__':
    Main()

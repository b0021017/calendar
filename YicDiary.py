# YIC 情報ビジネス専門学校
#  情報工学科 2年
#     南野 凌志 (B0021017@ib.yic.ac.jp)
#




import tkinter as tk
import tkinter.ttk as ttk
import datetime as da
import calendar as ca
import pymysql.cursors


WEEK = ['日', '月', '火', '水', '木', '金', '土']
WEEK_COLOUR = ['red', 'black', 'black', 'black','black', 'black', 'blue']
actions = ('学校','試験', '課題', '行事', '就活', 'アルバイト','旅行')

class YicDiary:
  def __init__(self, root, login_name, login_id):
    root.title('予定管理アプリ')
    root.geometry('520x280')
    root.resizable(0, 0)
    root.grid_columnconfigure((0, 1), weight=1)
    self.sub_win = None

    self.year  = da.date.today().year
    self.mon = da.date.today().month
    self.today = da.date.today().day

    self.title = None

    self.login_name = login_name
    self.login_id = login_id
    self.distinction_id = login_id

    # 左側のカレンダー部分
    leftFrame = tk.Frame(root)
    leftFrame.grid(row=0, column=0)
    self.leftBuild(leftFrame)

    # 右側の予定管理部分
    rightFrame = tk.Frame(root)
    rightFrame.grid(row=0, column=1)
    self.rightBuild(rightFrame)


  #-----------------------------------------------------------------
  # アプリの左側の領域を作成する
  #
  # leftFrame: 左側のフレーム
  def leftBuild(self, leftFrame):
    self.viewLabel = tk.Label(leftFrame, font=('', 10))
    beforButton = tk.Button(leftFrame, text='＜', font=('', 10), command=lambda:self.disp(-1))
    nextButton = tk.Button(leftFrame, text='＞', font=('', 10), command=lambda:self.disp(1))

    self.viewLabel.grid(row=0, column=1, pady=10, padx=10)
    beforButton.grid(row=0, column=0, pady=10, padx=10)
    nextButton.grid(row=0, column=2, pady=10, padx=10)

    self.calendar = tk.Frame(leftFrame)
    self.calendar.grid(row=1, column=0, columnspan=3)
    self.disp(0)


  #-----------------------------------------------------------------
  # アプリの右側の領域を作成する
  #
  # rightFrame: 右側のフレーム
  def rightBuild(self, rightFrame):

    #self.max_user = self.max_user()
    temp2 = self.login_name         #self.user(0)
    #print(temp)
    self.viewLabel2 = tk.Label(rightFrame,text=temp2, font=('', 10))
    beforButton = tk.Button(rightFrame, text='＜', font=('', 10))
    nextButton = tk.Button(rightFrame, text='＞', font=('', 10))

    self.viewLabel2.grid(row=70, column=1, pady=10, padx=10)
    beforButton.grid(row=70, column=0, pady=50, padx=10)
    nextButton.grid(row=70, column=2, pady=10, padx=10)  
    r1_frame = tk.Frame(rightFrame)
    r1_frame.grid(row=0, column=0, pady=10)

    temp = '{}年{}月{}日の予定'.format(self.year, self.mon, self.today)
    self.title = tk.Label(r1_frame, text=temp, font=('', 12))
    self.title.grid(row=0, column=0, padx=20)

    button = tk.Button(rightFrame, text='追加', command=lambda:self.add())
    button.grid(row=0, column=1)

    self.r2_frame = tk.Frame(rightFrame)
    self.r2_frame.grid(row=1, column=0)

    self.schedule()


  #-----------------------------------------------------------------
  # アプリの右側の領域に予定を表示する
  #
  def schedule(self):
    # ウィジットを廃棄
    for widget in self.r2_frame.winfo_children():
      widget.destroy()

    # データベースに予定の問い合わせを行う
    # データベースに接続
    host = '127.0.0.1'
    user = 'root'
    password = ''
    db = 'april01'
    charset = 'utf8mb4'
    connection = pymysql.connect(host=host,
                                 user=user,
                                 password=password,
                                 db=db,
                                 charset=charset,
                                 cursorclass=pymysql.cursors.DictCursor)


    try:
        # トランザクション開始
        connection.begin()

        with connection.cursor() as cursor:
            
            cursor = connection.cursor()
    
            sql = "select contents from schedule inner JOIN calendar on calendar.date_ID = schedule.date_ID where date = '{}-{}-{}' and user_id = {};".format(self.year, self.mon, self.today, self.login_id)
            cursor.execute(sql)
            results = cursor.fetchall()
            for i, row in enumerate(results):
                print(i, row)
                X = row['contents']

                lbl = tk.Label(self.r2_frame, text=X, font=('', 12))
                lbl.grid(row = i, column = 0)
#                lbl.place(x = 280, y = 100 + i * 30)
               
                

        connection.commit()
#            sql = "select * from schedule where date_ID = sql"
#            sql = "select * from schedule where date_ID = {}".format(s)




#            sql = "select max(id) from schedule"
#            cursor.execute(sql)

#            results = cursor.fetchone()
#            idx = results['max(id)']
#            print(idx)








    except Exception as e:
        print('error:', e)
        connection.rollback()
    finally:
        connection.close()



  #-----------------------------------------------------------------
  # カレンダーを表示する
  #
  # argv: -1 = 前月
  #        0 = 今月（起動時のみ）
  #        1 = 次月
  def disp(self, argv):
    self.mon = self.mon + argv
    if self.mon < 1:
      self.mon, self.year = 12, self.year - 1
    elif self.mon > 12:
      self.mon, self.year = 1, self.year + 1

    self.viewLabel['text'] = '{}年{}月'.format(self.year, self.mon)

    cal = ca.Calendar(firstweekday=6)
    cal = cal.monthdayscalendar(self.year, self.mon)

    # ウィジットを廃棄
    for widget in self.calendar.winfo_children():
      widget.destroy()

    # 見出し行
    r = 0
    for i, x in enumerate(WEEK):
      label_day = tk.Label(self.calendar, text=x, font=('', 10), width=3, fg=WEEK_COLOUR[i])
      label_day.grid(row=r, column=i, pady=1)

    # カレンダー本体
    r = 1
    for week in cal:
      for i, day in enumerate(week):
        if day == 0: day = ' ' 
        label_day = tk.Label(self.calendar, text=day, font=('', 10), fg=WEEK_COLOUR[i], borderwidth=1)
        if (da.date.today().year, da.date.today().month, da.date.today().day) == (self.year, self.mon, day):
          label_day['relief'] = 'solid'
        label_day.bind('<Button-1>', self.click)
        label_day.grid(row=r, column=i, padx=2, pady=1)
      r = r + 1

    # 画面右側の表示を変更
    if self.title is not None:
      self.today = 1
      self.title['text'] = '{}年{}月{}日の予定'.format(self.year, self.mon, self.today)


  #-----------------------------------------------------------------
  # 予定を追加したときに呼び出されるメソッド
  #
  def add(self):
    if self.sub_win == None or not self.sub_win.winfo_exists():
      self.sub_win = tk.Toplevel()
      self.sub_win.geometry("300x300")
      self.sub_win.resizable(0, 0)

      # ラベル
      sb1_frame = tk.Frame(self.sub_win)
      sb1_frame.grid(row=0, column=0)
      temp = '{}年{}月{}日　追加する予定'.format(self.year, self.mon, self.today)
      title = tk.Label(sb1_frame, text=temp, font=('', 12))
      title.grid(row=0, column=0)

      # 予定種別（コンボボックス）
      sb2_frame = tk.Frame(self.sub_win)
      sb2_frame.grid(row=1, column=0)
      label_1 = tk.Label(sb2_frame, text='種別 : 　', font=('', 10))
      label_1.grid(row=0, column=0, sticky=tk.W)
      self.combo = ttk.Combobox(sb2_frame, state='readonly', values=actions)
      self.combo.current(0)
      self.combo.grid(row=0, column=1)

      # テキストエリア（垂直スクロール付）
      sb3_frame = tk.Frame(self.sub_win)
      sb3_frame.grid(row=2, column=0)
      self.text = tk.Text(sb3_frame, width=40, height=15)
      self.text.grid(row=0, column=0)
      scroll_v = tk.Scrollbar(sb3_frame, orient=tk.VERTICAL, command=self.text.yview)
      scroll_v.grid(row=0, column=1, sticky=tk.N+tk.S)
      self.text["yscrollcommand"] = scroll_v.set

      # 保存ボタン
      sb4_frame = tk.Frame(self.sub_win)
      sb4_frame.grid(row=3, column=0, sticky=tk.NE)
      button = tk.Button(sb4_frame, text='保存', command=lambda:self.done())
      button.pack(padx=10, pady=10)
    elif self.sub_win != None and self.sub_win.winfo_exists():
      self.sub_win.lift()


  #-----------------------------------------------------------------
  # 予定追加ウィンドウで「保存」を押したときに呼び出されるメソッド
  #
  def done(self):
    # 日付
    date = '{}-{}-{}'.format(self.year, self.mon, self.today)
    print(date)

    # 種別
    kinds = self.combo.get()
    print(kinds)

    # 予定の内容
    contents = self.text.get('1.0', 'end')  #1.0は最初から(?) endは終わりまで(?)
    print(contents)


    # データベースに接続
    host = '127.0.0.1'
    user = 'root'
    password = ''
    db = 'april01'
    charset = 'utf8mb4'
    connection = pymysql.connect(host=host,
                                 user=user,
                                 password=password,
                                 db=db,
                                 charset=charset,
                                 cursorclass=pymysql.cursors.DictCursor)


    try:
        # トランザクション開始
        connection.begin()

        with connection.cursor() as cursor:
            
            cursor = connection.cursor()
    
            sql = "select * from schedule"
#            sql = "select max(id) from schedule"
            cursor.execute(sql)

#            results = cursor.fetchone()
#            idx = results['max(id)']
#            print(idx)

            results = cursor.fetchall()
            for i, row in enumerate(results):
                print(i, row)

            #sql = "insert into calendar(date) values('{}')".format(date)
#            print(sql)

            #cursor.execute(sql)

            #sql = "SELECT max(date_ID) FROM calendar"
#            cursor.execute(sql)
#            result = cursor.fetchone()


            d = ("'{}-{}-{}'".format(self.year, self.mon, self.today))
            d2 = "select * from calendar where date = {}".format(d)
            #print(cursor.execute(d2))
            #print(d)

            result = cursor.fetchone()
            #print(result)
            if  cursor.execute(d2) == 0:
                sql = "insert into calendar(date) values('{}')".format(date)
                cursor.execute(sql)

                #print(cursor.execute(d2))
                sql = "SELECT max(date_ID) FROM calendar"
                cursor.execute(sql)

                result = cursor.fetchone()

                foreignKey = result['max(date_ID)']
                #print(foreignKey)

            else:
                sql = "select date_ID from calendar where date = {}".format(d)
                cursor.execute(sql)
                result = cursor.fetchone()
                #print(sql)
                foreignKey = result['date_ID']
                #print(foreignKey)

            sql = "insert into schedule(date_ID, kinds, contents, user_ID) values('{}', '{}', '{}' ,'{}')".format(foreignKey, kinds, contents, self.login_id)
#            print(sql)

            cursor.execute(sql)

        connection.commit()


    except Exception as e:
        print('error:', e)
        connection.rollback()
    finally:
        connection.close()
    # この行に制御が移った時点で、DBとの接続は切れている

    self.sub_win.destroy()


  #-----------------------------------------------------------------
  # 日付をクリックした際に呼びだされるメソッド（コールバック関数）
  #
  # event: 左クリックイベント <Button-1>
  def click(self, event):
    day = event.widget['text']
    if day != ' ':
      self.title['text'] = '{}年{}月{}日の予定'.format(self.year, self.mon, day)
      self.today = day


    self.schedule()





def Main():
  root = tk.Tk()
  YicDiary(root)
  root.mainloop()

if __name__ == '__main__':
  Main()

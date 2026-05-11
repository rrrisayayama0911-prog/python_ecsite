from fastapi import FastAPI, Request,Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse
import os
import psycopg2

app = FastAPI()

# テンプレートの設定
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# メイン画面（ここからが②接続確認のメイン！）
@app.get("/")
def show_main(request: Request):
    # 1.データベースに接続する
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    #2.SQLを実行して、productsテーブルから全件取ってくる
    cur.execute("SELECT id,name,price FROM products;")
    products = cur.fetchall()#バケツ「products」に全部入れる
    
    #3.
    print("---DBから取得したデータの中身---")
    print(products)
    print(f"取得した件数：{len(products)}件")
    print("------------------------------")
    
    #4.接続を閉じる
    cur.close()
    conn.close()
    
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"items":products}#バケツの中身を「items」という名前でhtmlに渡す、受付窓口（TemplateResponse）を通る時に、公式な「荷札（items）」に貼り替えられるから
    )
    

#登録画面
@app.get("/register")
def register_page(request:Request,error:str = None):#error: str = None の = None は、「もしURLに error が入ってなくても怒らないでね（空っぽでもいいよ）」という意味
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={"error":error} #HTMLにエラー内容を渡す
    )

#メールアドレスを受け取る
@app.post("/register") #データの送信(POST)を受け取る設定
def register_user(request:Request,email:str = Form(...)):
    #届いたメールアドレスを表示して、登録完了画面を出す
    print(f"届いたメールアドレス：{email}")#ターミナルに表示(テスト用)
    
    #データベースに保存する処理を追加
    try:
        #DBに保存する
        conn =psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        #SQlに実行する(usersテーブルのemail列に届いたアドレスを入れる)
        cur.execute("INSERT INTO users (email) VALUES(%s)",(email,))
        
        #重要：ハンコを押して確定させる
        conn.commit()
        
        #お片付け
        cur.close()
        conn.close()
        
        return RedirectResponse(url=f"/login",status_code=303)
       
    
    
    except Exception as e:
        #もしエラーが起きたら内容を表示する
        print(f"エラーが発生しました：{e}")
        print("登録に失敗しました")
        error_msg="すでに登録されているか、接続エラーです"
        return RedirectResponse(url=f"/register?error={error_msg}",status_code=303)
    """
    {e} の中身（システムの生のエラーメッセージ）をそのままユーザーに見せるのは、実はセキュリティリスクになる。
    「どのテーブルでエラーが出たか」などの内部構造が筒抜けになってしまうから。
    代わりに考えられる原因を伝えとく。
    """
    
    
#PostgreSQLに接続するための設定情報
DB_CONFIG = {
    "dbname":"postgres", #pgAdminで「Databases」 を開いた後に検索した名前
    "user":"postgres",#インストールした時のデフォルトユーザー名
    "password":"sql", #PostgreSQL 18インストール時に自分で決めたパスワード
    "host":"localhost", #自分のPC内で動いているためlocalhost
    "port":"5432" #PostgreSQLの標準的なポート番号(PostgreSQLをインストールにデフォルトででてきたポート番号になるが、もし数字変えた場合はその数字で設定しないとつながらない)
}

# /loginというURLにアクセス（GET）が来たら実行される窓口
@app.get("/login")
def show_login(request:Request,error:str = None):
    #templatesフォルダにあるlogin.htmlをブラウザに返してあげる
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error":error}
    )
#ログインボタン(POST)が押された時に動く窓口
@app.post("/login")
def login_check(request:Request,email:str = Form(...),password:str = Form(...)):
    print(f"ログインを試みているアドレス：{email}")
    
    #ここに「DBから探す処理」を書く
    #DBに保存する
    try:
        #データベースに繋ぐ
        conn =psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        #ログインは「探す(SELECT)」のが仕事！
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s",(email,password))
        
        #sqlに登録したメールアドレスをuserに代入
        user =cur.fetchone() # ← ここで「中身があるか None か」が決まる！
        
        #お片付け
        cur.close()
        conn.close()
        
        #判断結果によって表示するメッセージを変える
        if user:
            #ログイン成功
            msg_ok = f"[成功]{email}さん、ようこそ"
            return RedirectResponse(url=f"/?ok={msg_ok}",status_code=303)
        else:
            #メールアドレスかパスワードが違う場合(ログイン失敗)
            error_msg = "[エラー]メールアドレスかパスワードが間違っています。登録されてない場合は、会員登録お願いします。メールアドレスまたはパスワードをお忘れの場合はXXX-XXXX-XXXXまでご連絡お願いします。"
            return RedirectResponse(url=f"/login?error={error_msg}",status_code=303)
    except Exception as e:
        print(f"エラー発生：{e}")
        return {"message": "接続エラーが発生しました。"}
    
    


# テスト用API
@app.get("/test")
def show_test():
    return {"message": "これはテスト用のAPI窓口です！"}
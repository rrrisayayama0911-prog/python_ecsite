from fastapi import FastAPI, Request,Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os
import psycopg2

app = FastAPI()

# テンプレートの設定
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# メイン画面（ここからが②接続確認のメイン！）
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    # 1.ここにHTMLに送るための「データの箱」を作る
    
    items = [
        {"name":"チョコレート","price":300}, # 辞書形式
        {"name":"バニラ","price":250},
        {"name":"ストロベリー","price":320},
        {"name":"抹茶","price":280}
    ]
    # 2. テンプレートエンジン(Jinja2)にデータを渡して出荷
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"items":items} #ここでデータをHTMLに流す。
    )

#登録画面
@app.get("/register")
def registar_page(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html"
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
        
        return {"message":f"{email}をデータベースに登録しました！"}
    
    except Exception as e:
        #もしエラーが起きたら内容を表示する
        print(f"エラーが発生しました：{e}")
        return {"message":"登録に失敗しました"}
    
#PostgreSQLに接続するための設定情報
DB_CONFIG = {
    "dbname":"postgres", #pgAdminで「Databases」 を開いた後に検索した名前
    "user":"postgres",#インストールした時のデフォルトユーザー名
    "password":"sql", #PostgreSQL 18インストール時に自分で決めたパスワード
    "host":"localhost", #自分のPC内で動いているためlocalhost
    "port":"5432" #PostgreSQLの標準的なポート番号(PostgreSQLをインストールにデフォルトででてきたポート番号になるが、もし数字変えた場合はその数字で設定しないとつながらない)
}

# テスト用API
@app.get("/test")
def show_test():
    return {"message": "これはテスト用のAPI窓口です！"}
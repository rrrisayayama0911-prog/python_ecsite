from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

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
# テスト用API
@app.get("/test")
def show_test():
    return {"message": "これはテスト用のAPI窓口です！"}
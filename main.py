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
    # ここに商品データを書いていく
    return templates.TemplateResponse(request=request, name="index.html")

# テスト用API
@app.get("/test")
def show_test():
    return {"message": "これはテスト用のAPI窓口です！"}
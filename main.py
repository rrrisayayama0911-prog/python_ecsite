

"""
FastAPI使うと以下でアプリ起動することになる
uvicorn main:app --reload
意味：uvicornエンジンに自分が作ったappをセットして起動する
appはwebサーバとしての能力が入ってる箱(実物/オブジェクト)。
uvicornはブラウザからリクエストを受けてappにレスポンスよろしくと投げる外箱(エンジン)。

main → main.py ファイル
app → その中の app オブジェクト
--reload → ファイル変更時に自動再起動（開発時のみ使用）

"""


#fastapi定義
from fastapi import FastAPI
"""
Q:fastapiインストールしたけどインポートいるのなんで？
A:
インストール (pip install fastapi):
あなたのPC（図書館）の中に、FastAPIという便利な道具一式をダウンロードして保存した状態。
でも、この段階ではまだ「いつでも使えるように保管されている」だけ。
もしインポートしなくても全部が最初から読み込まれていたら、プログラムを動かすたびに全ての道具を準備することになり、
メモリを大量に消費して動きがめちゃくちゃ重くなってしまうので、
必要なときに、必要な道具だけを呼び出す（importする）のがプログラミングの鉄則

インポート (from fastapi import FastAPI):
from fastapi:
たくさんある道具箱（ライブラリ）の中から、fastapi という名前の箱を選ぶ

import FastAPI:
その箱の中には色々な部品が入っているけど、今回はWebアプリの心臓部である FastAPI という部品だけを使う。
"""

#Jinja2を使って、用意したHTMLファイルの中身表示に必要なものをインポート
from fastapi import Request #def index(request: Request): の中で Request という「型（ルール）」 を使うためにインポート
from fastapi.templating import Jinja2Templates #templates = Jinja2Templates(directory="templates")で使うためにインポート
from fastapi.responses import HTMLResponse #FastAPIの自動ドキュメント生成（Swagger UI）で、このエンドポイントがHTMLを返すことを明示するためにインポート
import os #"templates"で今実行している場所からの位置を教えるためにインポート

app= FastAPI()  
"""
Q:app = FastAPI()の意味は？
A:app = FastAPI() というのは、FastAPIという設計図から、実際にWebアプリとして動く機能を持った 『実体（オブジェクト）』 を作り出しているコード。
この app オブジェクトには、URLの受け取りやエラー処理などの機能がすでにパッケージ化されている。
これを uvicorn main:app --reloadでuvicorn という実行エンジンに渡すことで、
ブラウザからのリクエストを app が処理できるようになり、通信が可能になる。
上記の記載で実行し、ブラウザを確認(アドレスバーに http://127.0.0.1:8000 と入力してエンター。)
でサーバーが反応していること({"detail":"Not Found"}が表示される)が分かる。
"""

"""
htmi返すindex関数と同じパスになるためコメントアウト

@app.get("/")
#read_root関数定義
def read_root():
    return{"Hello world:webサーバとフロントエンドの通信に成功"}
"""


"""
Q:@app.get("/")の意味は？
A:@ から始まる記述をプログラミング用語は「デコレータ」
app オブジェクト（Webアプリ本体）に対して、「トップページ（/：ルートパス）という『住所』宛てに、
『データをちょうだい（GET）』という方式で連絡が来たら、すぐ下のread_root関数を実行してね！」と予約をしている状態
@app.get はGET（ちょうだい）という種類のリクエストだけを受け付ける窓口。ブラウザで普通にページを開くときはこれ。
"/" (ルートパス)はサイトのトップページのこと（http://127.0.0.1:8000/）。
"/items": http://127.0.0.1:8000/items にアクセスしたときに反応する。
"""


#Jinja2を使って、用意したHTMLファイルの中身表示
"""
Windows環境だと、たまにこの "templates" という書き方だけでは、うまく場所を特定できないことがあります。
これを、「今実行している場所からの相対位置」としてはっきり教えてあげる書き方に修正しましょう。
templates = Jinja2Templates(directory="templates")
"""
#絶対パスでtemplatesフォルダを指定(main.pyが置いてある場所を基準にして、すぐ隣にあるtemplatesフォルダを見てねという意味。これで階層エラーを防げる)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR,"templates"))

"""
※コメントの中のバックスラッシュをスラッシュに変えないと以下のエラーになった。

SyntaxError: (unicode error) 'unicodeescape' 
codec can't decode bytes in position 638-639
: truncated バックスラッシュUXXXXXXXX escape

1. os.path.abspath(__file__)
__file__: これはPythonが最初から持っている特別な変数で、「今動いているファイル（main.py）」の場所を指す。
os.path.abspath(...): そのファイルの「絶対パス（C:/Users/... から始まるフル住所）」を取得。
つまり： 「今実行中の main.py って、PCのどこの住所にいるの？」と突き止める作業。

2. os.path.dirname(...)
先ほど突き止めた main.py の住所から、「ファイル名」を削って「フォルダ（ディレクトリ）名」だけを取り出す。
つまり： C:/Users/.../main.py から main.py を除いた、C:/Users/.../python_ecsite（フォルダの場所） が BASE_DIR に入る。

3. os.path.join(BASE_DIR, "templates")
さっきのフォルダの場所に、"templates" という文字を安全にくっつける。
なぜ単に足し算（+）しないのかというと、Windowsは \（バックスラッシュ）、Macは /（スラッシュ）という風に、OSによってフォルダの区切り文字が違うから。
join を使うと、Pythonが勝手にそのPCに合わせて調節してくれる。
つまり： 「main.py があるフォルダのすぐ横にある templates フォルダ」の正確な住所が出来上がる。
"""




# 【重要！】HTMLを表示する窓口
@app.get("/",response_class=HTMLResponse)
def index(request:Request):
    return templates.TemplateResponse(request=request,name="index.html")


"""
response_class=HTMLResponse （返却物の種類）
意味: この関数が、最終的に「HTML形式のデータ」を返すことを明示。

なぜ書くのか？:
自動ドキュメントのため: FastAPIは http://127.0.0.1:8000/docs（Swagger UI）という説明書を自動生成しますが、ここに「この窓口はHTMLを返しますよ」
と正しく表示されるようになる。
ブラウザへの通知: ブラウザに対して「これから送るのはただの文字じゃなくて
HTMLだよ」と教えることで、ブラウザが正しくタグを解釈して表示してくれる。
"""


"""
request（小文字）: 
実際にブラウザから届いた「生のお手紙（データ）」を入れるための箱（変数名）。

: Request（大文字）: 
「この箱（request）の中には、FastAPIのルールに従った『Request形式』のデータが入りますよ」という型（注釈）であり、これをFastAPIに伝える

この階層（python_ecsite\python_ecsite）にいれば：
uvicorn main:app → すぐ横にある main.py を見つけられる。
Jinja2Templates(directory="templates") → すぐ横にある templates フォルダ を見つけられる。
"""


"""
Q:return templates.TemplateResponse("index.html",{"request":request})
だとブラウザでInternal Server Errorになるのはなんで？
A:
FastAPI（Starlette）のバージョンによっては、
「第1引数は request オブジェクトでなければならない」というルールに厳格な場合があり、今回該当した。
第2引数に辞書（{"request": request}）をそのまま渡すと、内部のキャッシュ処理で「辞書（dict）はハッシュ化できない（unhashable）！」というエラーが発生。
これがログにあった TypeError: unhashable type: 'dict' の正体
変数名=中身 の「名前付き引数」形式で書くといい

"""





# 【おまけ】テスト用の文字だけ返す窓口
@app.get("/test")# 「/test」という住所にアクセスが来たら...
def show_test():# この関数（プログラム）をその場で動かせ！
    # 必ず {"キー": "値"} の形式で返す
    return {"message": "これはテスト用のAPI窓口です！"}# その場で作った文字を返せ！

"""
Q:testファイルとかないのになんででるの?
A:
その場でプログラムが「返事（データ）」を作成している。だからファイルは存在しなくていい！
FastAPI（動的アプリ）: ファイルの有無ではなく、
「この住所（URL）に来たら、この関数を実行せよ」という「交通整理」のルールがある

ブラウザが /test という住所に「データをちょうだい（GET）」と注文を出す。
FastAPI（app）が「/test 宛ての注文だ！担当の show_test 関数、出番だぞ」と命令を出す。
show_test 関数が、その場で {"message": "..."} という文字データ を作ってブラウザに投げ返す。


"""

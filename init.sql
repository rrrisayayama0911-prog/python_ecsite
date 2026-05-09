-- ユーザー情報を管理する扉（テーブル）
-- 既にテーブルがある場合は作成しない（IF NOT EXISTS）
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,              -- 1, 2, 3...と自動で振られる背番号（鍵穴）
    email VARCHAR(255) UNIQUE NOT NULL, -- 重複を許さないメールアドレス（二重ロック）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- 登録日時（いつ作られたかの証跡）
);

-- コメント：
-- SERIAL は PostgreSQL 独自のデータ型で、自動で連番を振ってくれます。
-- UNIQUE をつけることで、同じメールアドレスでの二重登録（バグ）を防ぎます。


-- 商品情報を管理する扉（テーブル）
-- データはポスグレの場合シングルクォーテーションを使用
CREATE TABLE products(
	id SERIAL PRIMARY KEY,              -- 1, 2, 3...と自動で振られる背番号（鍵穴）
	name TEXT NOT NULL,                 -- 商品名（未入力はエラー、同じ名前はOK）
    price INTEGER NOT NULL              -- 価格（未入力はエラー、同じ価格はOK）
);

INSERT INTO products(name,price)VALUES ('バニラ',250);
INSERT INTO products(name,price)VALUES ('チョコレート',300);
INSERT INTO products(name,price)VALUES('ストロベリー',320);
INSERT INTO products(name,price)VALUES('抹茶',280);

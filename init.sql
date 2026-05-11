-- ユーザー情報を管理する扉（テーブル）
CREATE TABLE users (
    email TEXT PRIMARY KEY, -- メールアドレスをIDにする
	password TEXT NOT NULL,-- パスワード（今回は平文）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- 登録日時（いつ作られたかの証跡）
);

-- テスト用のデータを1つ入れておく
INSERT INTO users (email, password) VALUES ('test@example.com', 'pass123');



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

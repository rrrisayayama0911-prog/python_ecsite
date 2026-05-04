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
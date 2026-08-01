# WidMillClub-docs

人力飛行機 主翼設計解析プログラム（MATLAB→Excel VBA移植版）の学習ドキュメントを公開するための
MkDocsサイト一式です。

## 正本(ソース)について

このリポジトリの`docs/*.md`は、元のExcelプロジェクトフォルダ（OneDrive上の
`_VBA移植資料\学習ドキュメント\`）にある正本の**ミラー**です。**このリポジトリの
`docs/`を直接編集しないでください** — 次回`sync_docs.sh`実行時に上書きされます。

内容を更新する場合は、必ずOneDrive側の正本を編集したうえで、次を実行してから
コミット・デプロイしてください。

```bash
./sync_docs.sh
```

## ローカルでの確認

```bash
./venv/Scripts/python.exe -m mkdocs serve
```

`http://127.0.0.1:8000/` で確認できます。

## デプロイ

```bash
./venv/Scripts/python.exe -m mkdocs gh-deploy
```

`gh-pages`ブランチへビルド結果をpushし、GitHub Pagesで公開します。

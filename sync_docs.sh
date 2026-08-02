#!/bin/bash
# OneDrive上の正本(学習ドキュメント\*.md)を、このリポジトリのdocs/へコピーする。
# 正本はOneDrive側の "_VBA移植資料\学習ドキュメント\" のまま。
# ここにあるファイルは常にビルド用のミラーであり、直接編集しないこと。
set -e

SRC="/c/Users/fukam/OneDrive/cココナラ/202607-09/20260727 WidMillClub(人力飛行機設計プログラムの改良)/22.ワイヤー機vs片持ち機/22.ワイヤー機vs片持ち機/解析/_VBA移植資料/学習ドキュメント"
DST="$(dirname "$0")/docs"

for f in "$SRC"/*.md; do
    base="$(basename "$f")"
    case "$base" in
        _*) continue ;;   # "_"始まりは非公開の作業メモ(プロンプト集など)、サイトへは同期しない
    esac
    cp "$f" "$DST/"
done
# MkDocsはファイル名が index.md のものだけをサイトルート(/)に出力するため、
# 00_はじめに.md をルート表示用にもコピーする(内容は同一、二重管理ではなく毎回上書き)。
cp "$SRC/00_はじめに.md" "$DST/index.md"
if [ -f "$SRC/CNAME" ]; then
    cp "$SRC/CNAME" "$DST/"
fi
if [ -d "$SRC/figures" ]; then
    mkdir -p "$DST/figures"
    cp "$SRC"/figures/* "$DST/figures/" 2>/dev/null || true
fi
echo "synced: $SRC -> $DST"

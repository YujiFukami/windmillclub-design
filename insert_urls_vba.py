# -*- coding: utf-8 -*-
"""
既存の27箇所の '●学習資料:' アンカーコメントの直後に、公開サイト
(https://YujiFukami.github.io/windmillclub-design/) の該当ページ・見出しへの
安定URLを追記する。URLは heading_map.json(mkdocsビルド結果から見出しテキスト→
アンカーIDを実測して作った対応表)を使って機械的に生成するため、見出し文言の
今後の変更にも追従しやすい。

cp932ファイルはEdit toolで直接編集しない、という既存の安全ルールに従い、
バイト単位のread/writeのみで完結させる。
"""
import json
import os

VBA_DIR = (r'C:\Users\fukam\OneDrive\cココナラ\202607-09\20260727 '
           r'WidMillClub(人力飛行機設計プログラムの改良)\22.ワイヤー機vs片持ち機\22.'
           r'ワイヤー機vs片持ち機\解析\_VBA移植資料\VBAモジュール')
CRLF = '\r\n'
BASE_URL = 'https://YujiFukami.github.io/windmillclub-design'

with open('heading_map.json', encoding='utf-8') as f:
    HEADING_MAP = json.load(f)


def url_for(doc, heading=None):
    if heading is None:
        return f'{BASE_URL}/{doc}/'
    anchor = HEADING_MAP[doc][heading]
    return f'{BASE_URL}/{doc}/#{anchor}'


def read_lines(path):
    with open(path, 'rb') as f:
        text = f.read().decode('cp932')
    return text.split(CRLF)


def write_lines(path, lines):
    text = CRLF.join(lines)
    with open(path, 'wb') as f:
        f.write(text.encode('cp932'))


def indent_of(line):
    return line[:len(line) - len(line.lstrip(' '))]


def insert_after(lines, match_substring, comment_lines, occurrence=1):
    count = 0
    for idx, ln in enumerate(lines):
        if match_substring in ln:
            count += 1
            if count == occurrence:
                if idx + 1 < len(lines) and lines[idx + 1].strip().startswith("' URL:"):
                    return lines  # 冪等化: 既に挿入済みなら何もしない
                ind = indent_of(ln)
                new_lines = [ind + c for c in comment_lines]
                return lines[:idx + 1] + new_lines + lines[idx + 1:]
    raise AssertionError(f'not found: {match_substring!r} (occurrence {occurrence})')


def urls_block(refs):
    """refs: [(doc, heading_or_None), ...] -> コメント行のリスト"""
    urls = [url_for(doc, heading) for doc, heading in refs]
    if len(urls) == 1:
        return [f"' URL: {urls[0]}"]
    lines = [f"' URL: {urls[0]}"]
    for u in urls[1:]:
        lines.append(f"'      {u}")
    return lines


def process(fname, entries):
    path = os.path.join(VBA_DIR, fname)
    lines = read_lines(path)
    for anchor_last_line, refs, occurrence in entries:
        lines = insert_after(lines, anchor_last_line, urls_block(refs), occurrence)
    write_lines(path, lines)
    print(f'{fname}: {len(entries)} URLs inserted')


D02, D03, D04, D05 = '02_空力理論編', '03_空力実装編', '04_構造理論編', '05_構造実装編'
D01 = '01_全体アーキテクチャ'

# 各エントリ: (直前に挿入済みのアンカーコメント最終行を一意に特定する部分文字列, refs, occurrence)

process('clsWingGeometry.cls', [
    ("03_空力実装編.md「1. 翼形状の展開(コサイン分布グリッドの生成)」を参照",
     [(D02, "2. 循環のフーリエ級数展開とコサイン変数変換"),
      (D03, "1. 翼形状の展開(コサイン分布グリッドの生成)")], 1),
])

process('Mod03_分布補間.bas', [
    ("03_空力実装編.md「7. 補間ユーティリティ」を参照",
     [(D03, "7. 補間ユーティリティ")], 1),
])

process('Mod04_翼型データベース.bas', [
    ("03_空力実装編.md「4. プロファイル抗力・モーメント係数(翼型データベース参照)」を参照",
     [(D02, "6. プロファイル抗力・モーメント係数(2次元翼型データの利用)"),
      (D03, "4. プロファイル抗力・モーメント係数(翼型データベース参照)")], 1),
])

process('Mod05_空力ソルバー.bas', [
    ("'          03_空力実装編.md「2～6」に、この関数内の各ブロックとの対応を記載",
     [(D02, None)], 1),
    ("03_空力実装編.md「6. トリム速度の反復ループ」を参照",
     [(D02, "8. 飛行速度のつり合い(トリム)反復"),
      (D03, "6. トリム速度の反復ループ")], 1),
    ("03_空力実装編.md「2. フーリエ係数の連立方程式」を参照",
     [(D02, "3. モノプレーン方程式(フーリエ係数の連立方程式)"),
      (D03, "2. フーリエ係数の連立方程式")], 1),
    ("03_空力実装編.md「3. 誘導迎角の分布復元とCL・スパン効率」を参照",
     [(D02, "4. 揚力係数・誘導抗力・スパン効率"),
      (D03, "3. 誘導迎角の分布復元とCL・スパン効率")], 1),
    ("03_空力実装編.md「4. プロファイル抗力・モーメント係数(翼型データベース参照)」を参照",
     [(D02, "6. プロファイル抗力・モーメント係数(2次元翼型データの利用)"),
      (D03, "4. プロファイル抗力・モーメント係数(翼型データベース参照)")], 1),
    ("03_空力実装編.md「5. 空力中心・ピッチングモーメントの積分」を参照",
     [(D02, "7. 空力中心・区分重心とピッチングモーメント"),
      (D03, "5. 空力中心・ピッチングモーメントの積分")], 1),
])

process('Mod06_空力ソルバーテスト.bas', [
    ("03_空力実装編.md「9. 実行エントリポイントとテスト」を参照",
     [(D03, "9. 実行エントリポイントとテスト")], 1),
])

process('Mod07_空力結果出力.bas', [
    ("03_空力実装編.md「8. 結果の保持と出力」を参照",
     [(D03, "8. 結果の保持と出力")], 1),
])

process('Mod08_空力実行.bas', [
    ("03_空力実装編.md「9. 実行エントリポイントとテスト」を参照",
     [(D01, "エントリポイントは2つある"),
      (D03, "9. 実行エントリポイントとテスト")], 1),
])

process('Mod09_空力迎角スイープ.bas', [
    ("03_空力実装編.md「9. 実行エントリポイントとテスト」を参照",
     [(D03, "9. 実行エントリポイントとテスト")], 1),
])

process('Mod10_材料データベース.bas', [
    ("05_構造実装編.md「1. 材料データベース」を参照",
     [(D05, "1. 材料データベース")], 1),
])

process('Mod11_桁断面剛性.bas', [
    ("05_構造実装編.md「2. 積層構成のデータ表現とbreakpoint展開」を参照",
     [(D05, "2. 積層構成のデータ表現とbreakpoint展開")], 1),
    ("05_構造実装編.md「2. 積層構成のデータ表現とbreakpoint展開」を参照",
     [(D05, "2. 積層構成のデータ表現とbreakpoint展開")], 2),
    ("05_構造実装編.md「3. CLT計算の実装(Q行列～EIy～Q16)」を参照",
     [(D04, "2. 古典積層理論(CLT)の基礎 — 材料主軸のQ行列とその角度変換"),
      (D04, "3. 面内剛性(A行列)と等価Ex/Gxy"),
      (D05, "3. CLT計算の実装(Q行列〜EIy〜Q16)")], 1),
    ("05_構造実装編.md「4. UD補強断面二次モーメントの実装」を参照",
     [(D04, "5. UD補強の扇形断面二次モーメント"),
      (D05, "4. UD補強断面二次モーメントの実装")], 1),
])

process('Mod13_桁断面剛性実行.bas', [
    ("05_構造実装編.md「5. 断面剛性計算の実行エントリポイント」を参照",
     [(D05, "5. 断面剛性計算の実行エントリポイント")], 1),
])

process('Mod14_桁自重.bas', [
    ("05_構造実装編.md「6. 桁自重」を参照",
     [(D05, "6. 桁自重")], 1),
])

process('Mod15_桁荷重.bas', [
    ("05_構造実装編.md「7. 荷重ベクトルの組み立てとグリッド橋渡し」を参照",
     [(D01, "2つのグリッド(格子点)がある"),
      (D05, "7. 荷重ベクトルの組み立てとグリッド橋渡し")], 1),
    ("05_構造実装編.md「7. 荷重ベクトルの組み立てとグリッド橋渡し」を参照",
     [(D05, "7. 荷重ベクトルの組み立てとグリッド橋渡し")], 2),
])

process('Mod16_桁FEM.bas', [
    ("05_構造実装編.md「8. 3D梁FEMの組立・ブロックThomas法による求解」を参照",
     [(D04, "6. 3D梁要素の剛性行列(6自由度/節点)"),
      (D05, "8. 3D梁FEMの組立・ブロックThomas法による求解")], 1),
    ("05_構造実装編.md「8. 3D梁FEMの組立・ブロックThomas法による求解」を参照",
     [(D04, "7. ブロック三重対角のThomas法"),
      (D05, "8. 3D梁FEMの組立・ブロックThomas法による求解")], 2),
])

process('Mod17_桁強度座屈.bas', [
    ("05_構造実装編.md「9. 強度・座屈評価の実装」を参照",
     [(D04, "8. 断面内の応力分布とTsai-Wu複合則"),
      (D05, "9. 強度・座屈評価の実装")], 1),
    ("05_構造実装編.md「9. 強度・座屈評価の実装」を参照",
     [(D04, "8. 断面内の応力分布とTsai-Wu複合則"),
      (D04, "9. 座屈に対する安全率(4方式)"),
      (D05, "9. 強度・座屈評価の実装")], 2),
])

process('Mod18_桁構造解析実行.bas', [
    ("05_構造実装編.md「10. 構造解析パイプライン全体のエントリポイント」を参照",
     [(D01, "エントリポイントは2つある"),
      (D05, "10. 構造解析パイプライン全体のエントリポイント")], 1),
])

print('all done')

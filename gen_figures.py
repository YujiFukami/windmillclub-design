# -*- coding: utf-8 -*-
"""
学習ドキュメント用の図版を生成するスクリプト。
理論編(02_空力理論編.md / 04_構造理論編.md)・実装編(03/05)で使う精度重視の図を
matplotlibでSVG出力する。生成先はOneDrive上の正本フォルダ(学習ドキュメント\\figures\\)。
"""
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle, FancyArrowPatch
from matplotlib.path import Path
import matplotlib.patches as mpatches

matplotlib.rcParams['font.family'] = ['Yu Gothic', 'Noto Sans JP', 'sans-serif']
matplotlib.rcParams['svg.fonttype'] = 'path'   # フォント未インストール環境でも文字化けしないようパス化
matplotlib.rcParams['axes.unicode_minus'] = False

OUT_DIR = os.environ.get('FIG_OUT_DIR') or (
    r'C:\Users\fukam\OneDrive\cココナラ\202607-09\20260727 '
    r'WidMillClub(人力飛行機設計プログラムの改良)\22.ワイヤー機vs片持ち機\22.'
    r'ワイヤー機vs片持ち機\解析\_VBA移植資料\学習ドキュメント\figures')
FIG_FORMAT = os.environ.get('FIG_FORMAT', 'svg')
os.makedirs(OUT_DIR, exist_ok=True)


def save(fig, name):
    if FIG_FORMAT != 'svg':
        name = os.path.splitext(name)[0] + '.' + FIG_FORMAT
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, format=FIG_FORMAT, bbox_inches='tight')
    plt.close(fig)
    print('saved:', name)


# ============================================================
# 図1: コサイン分布グリッド vs 等間隔グリッド (02_空力理論編.md)
# ============================================================
def fig_cosine_grid():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), gridspec_kw={'width_ratios': [1, 1.3]})

    # --- 左: 半円周上の等間隔θ → x軸への投影(コサイン変換) ---
    n = 13
    thetas = np.linspace(0, np.pi, n)
    xs = -np.cos(thetas)
    ys = np.sin(thetas)

    ax1.plot(np.cos(np.linspace(0, np.pi, 200)) * -1, np.sin(np.linspace(0, np.pi, 200)),
              color='#888', lw=1)
    ax1.scatter(xs, ys, color='#1d6fa5', zorder=5, s=28)
    for x, y in zip(xs, ys):
        ax1.plot([x, x], [0, y], color='#1d6fa5', lw=0.6, ls=':', alpha=0.6)
    ax1.scatter(xs, np.zeros_like(xs), color='#ab4a3a', zorder=5, s=28)
    ax1.axhline(0, color='#333', lw=0.8)
    ax1.set_xlim(-1.25, 1.25)
    ax1.set_ylim(-0.25, 1.15)
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.set_title('θを等間隔に取ると\ny = −(b/2)cosθ は翼端側で密になる', fontsize=10)
    # θ=0→(-1,0)、θ=π/2→(0,1、射影先は(0,0))、θ=π→(1,0)
    ax1.text(-1.0, -0.18, '翼端\nθ=0', fontsize=8, ha='center', color='#ab4a3a')
    ax1.text(0.0, -0.18, '翼根 (y=0)\nθ=π/2', fontsize=8, ha='center', color='#ab4a3a')
    ax1.text(1.0, -0.18, '翼端\nθ=π', fontsize=8, ha='center', color='#ab4a3a')

    # --- 右: コサイン分布 vs 等間隔の点列比較 ---
    n2 = 21
    theta2 = np.linspace(0, np.pi, n2)
    y_cos = -np.cos(theta2)          # -1..1、コサイン分布
    y_uniform = np.linspace(-1, 1, n2)

    ax2.scatter(y_cos, np.ones_like(y_cos), color='#1d6fa5', s=22)
    ax2.scatter(y_uniform, np.zeros_like(y_uniform), color='#b3791f', s=22)
    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(['等間隔グリッド\n(構造側、Mod16_桁FEM)', 'コサイン分布グリッド\n(空力側、clsWingGeometry)'])
    ax2.set_xlim(-1.15, 1.15)
    ax2.set_ylim(-0.6, 1.6)
    ax2.set_xlabel('スパン方向位置 y (翼根=0が中央)')
    ax2.spines[['top', 'right', 'left']].set_visible(False)
    ax2.tick_params(left=False)
    ax2.set_title('同じ21点でも配置が異なる', fontsize=10)

    fig.tight_layout()
    save(fig, 'cosine_grid.svg')


# ============================================================
# 図2: フーリエ級数による循環分布Γ(θ)の合成イメージ (02_空力理論編.md)
# ============================================================
def fig_fourier_circulation():
    theta = np.linspace(0.001, np.pi - 0.001, 400)

    # 例示用の係数(理想楕円分布に近いA1に、高次項A3,A5を少し混ぜた図示例。実データではない)
    coeffs = {1: 1.0, 3: -0.12, 5: 0.05}

    fig, ax = plt.subplots(figsize=(7.5, 4.2))

    total = np.zeros_like(theta)
    colors = ['#b3791f', '#2f7d55', '#ab4a3a']
    for (n, a), c in zip(coeffs.items(), colors):
        term = a * np.sin(n * theta)
        total += term
        ax.plot(theta, term, lw=1.1, ls='--', color=c, alpha=0.8, label=f'A{n}·sin({n}θ)')

    ax.plot(theta, total, lw=2.4, color='#1d6fa5', label='Σ Aₙ·sin(nθ) (合成後)')
    ax.plot(theta, np.sin(theta), lw=1.4, color='#888', ls=':', label='理想楕円分布 (sinθ)')

    ax.axhline(0, color='#333', lw=0.6)
    ax.set_xticks([0, np.pi / 2, np.pi])
    ax.set_xticklabels(['0\n(翼端)', 'π/2\n(翼根)', 'π\n(翼端)'])
    ax.set_xlabel('θ')
    ax.set_ylabel('Γ(θ) / (2bV)  相当の値')
    ax.set_title('フーリエ級数による循環分布の合成(奇数次のみ、係数は説明用の例)', fontsize=10.5)
    ax.legend(fontsize=8.5, loc='lower center', ncol=2)
    fig.tight_layout()
    save(fig, 'fourier_circulation.svg')


# ============================================================
# 図3: Q̄ij(θ) の繊維角度依存性 (04_構造理論編.md)
# ============================================================
def fig_qbar_rotation():
    # 代表的なCFRP一方向材の物性(説明用の例。実データベースの値そのものではない)
    Ex, Ey, Gxy, nu_xy = 130e9, 9e9, 5e9, 0.30
    nu_yx = nu_xy * Ey / Ex
    R = 1 / (1 - nu_xy * nu_yx)
    Qxx, Qyy, Qxy, Qss = R * Ex, R * Ey, R * nu_yx * Ex, Gxy

    u1 = 0.125 * (3 * Qxx + 3 * Qyy + 2 * Qxy + 4 * Qss)
    u2 = 0.5 * (Qxx - Qyy)
    u3 = 0.125 * (Qxx + Qyy - 2 * Qxy - 4 * Qss)
    u4 = 0.125 * (Qxx + Qyy + 6 * Qxy - 4 * Qss)
    u5 = 0.125 * (Qxx + Qyy - 2 * Qxy + 4 * Qss)

    th = np.linspace(0, np.pi, 300)
    Q11 = u1 + u2 * np.cos(2 * th) + u3 * np.cos(4 * th)
    Q22 = u1 - u2 * np.cos(2 * th) + u3 * np.cos(4 * th)
    Q12 = u4 - u3 * np.cos(4 * th)
    Q66 = u5 - u3 * np.cos(4 * th)
    Q16 = u2 / 2 * np.sin(2 * th) + u3 * np.sin(4 * th)
    Q26 = u2 / 2 * np.sin(2 * th) - u3 * np.sin(4 * th)

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    deg = np.degrees(th)
    scale = 1e9
    for arr, label, style in [
        (Q11, 'Q̄11', dict(color='#1d6fa5', lw=2)),
        (Q22, 'Q̄22', dict(color='#2f7d55', lw=2)),
        (Q12, 'Q̄12', dict(color='#888', lw=1.3, ls='--')),
        (Q66, 'Q̄66', dict(color='#b3791f', lw=1.3, ls='--')),
        (Q16, 'Q̄16 (曲げ-ねじり連成項)', dict(color='#ab4a3a', lw=2.2)),
        (Q26, 'Q̄26', dict(color='#ab4a3a', lw=1, ls=':')),
    ]:
        ax.plot(deg, arr / scale, label=label, **style)

    ax.axhline(0, color='#333', lw=0.6)
    for x in (0, 90, 180):
        ax.axvline(x, color='#ccc', lw=0.6, zorder=0)
    ax.set_xlim(0, 180)
    ax.set_xticks([0, 45, 90, 135, 180])
    ax.set_xlabel('繊維角度 θ [deg]')
    ax.set_ylabel('Q̄ij [GPa]')
    ax.set_title('繊維角度による縮約剛性Q̄の変化(代表的なCFRP一方向材の例)', fontsize=10.5)
    ax.legend(fontsize=8, ncol=2, loc='upper right')
    ax.annotate('0°/90°ではQ̄16=Q̄26=0\n(連成なし)', xy=(0, 0), xytext=(20, -18),
                fontsize=8, color='#ab4a3a',
                arrowprops=dict(arrowstyle='->', color='#ab4a3a', lw=0.8))
    fig.tight_layout()
    save(fig, 'qbar_rotation.svg')


# ============================================================
# 図4: 円環断面の層境界z2による直接積分イメージ (04_構造理論編.md)
# ============================================================
def fig_ring_layers():
    fig, ax = plt.subplots(figsize=(5.2, 5.2))

    id_r = 0.9
    thicknesses = [0.12, 0.10, 0.09, 0.08, 0.07]
    colors = ['#dcebf5', '#c7d2dc', '#b3d1e8', '#a3c4dd', '#8fb6d4']
    r = id_r
    boundaries = [r]
    for t, c in zip(thicknesses, colors):
        r_out = r + t
        wedge = Wedge((0, 0), r_out, 0, 360, width=t, facecolor=c, edgecolor='#14283d', lw=0.8)
        ax.add_patch(wedge)
        r = r_out
        boundaries.append(r)

    inner = Circle((0, 0), id_r, facecolor='white', edgecolor='#14283d', lw=0.8)
    ax.add_patch(inner)

    n_b = len(boundaries)
    angles = np.linspace(10, 80, n_b)   # 各境界を扇状に異なる角度へ振り分け、ラベルの重なりを防ぐ
    for i, (b, ang) in enumerate(zip(boundaries, angles)):
        x, y = b * np.cos(np.radians(ang)), b * np.sin(np.radians(ang))
        ax.plot([0, x], [0, y], color='#333', lw=0.5, ls=':')
        lx, ly = (b + 0.09) * np.cos(np.radians(ang)), (b + 0.09) * np.sin(np.radians(ang))
        ax.text(lx, ly, f'z{i}', fontsize=9.5, color='#14283d', ha='center', va='center')

    ax.annotate('プライ1枚分の層厚み', xy=(boundaries[1] * np.cos(np.radians(-20)),
                                            boundaries[1] * np.sin(np.radians(-20))),
                xytext=(1.55, -0.9), fontsize=8.5,
                arrowprops=dict(arrowstyle='->', color='#333', lw=0.8))

    lim = boundaries[-1] * 1.25
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('円環断面の層境界 z0(内径)〜zN(外径)\nEIy = Σ (2/3・Q̄11) × (z_k⁴ − z_{k-1}⁴)', fontsize=10)
    fig.tight_layout()
    save(fig, 'ring_layers.svg')


# ============================================================
# 図5: パイプ周方向4点 / UD2点の応力評価位置 (05_構造実装編.md)
# ============================================================
def fig_stress_eval_points():
    fig, ax = plt.subplots(figsize=(5.5, 5.5))

    R = 1.0
    circle = Circle((0, 0), R, facecolor='#eef2f5', edgecolor='#14283d', lw=1.3)
    ax.add_patch(circle)

    # パイプ4点(0/90/180/270°)
    pipe_angles = [0, 90, 180, 270]
    for a in pipe_angles:
        x, y = R * np.cos(np.radians(a)), R * np.sin(np.radians(a))
        ax.scatter([x], [y], color='#1d6fa5', s=60, zorder=5)
        lx, ly = 1.22 * np.cos(np.radians(a)), 1.22 * np.sin(np.radians(a))
        ax.text(lx, ly, f'φ={a}°', fontsize=9, ha='center', va='center', color='#1d6fa5')

    # UD補強: パイプを挟んで対称な2箇所(90°側・270°側、桁の曲げで最も応力が
    # 大きくなる上下の縁)に分けて巻かれ、それぞれの中心(φ=90°, 270°)で評価する
    # (Mod17_桁強度座屈.bas: phi = (iphi-1)*pi + pi/2 → iphi=1で90°、iphi=2で270°)
    ud_span = 70  # UD補強が覆う円周角の目安(図示用)
    ud_angles = [90, 270]
    for center in ud_angles:
        wedge = Wedge((0, 0), R * 1.12, center - ud_span / 2, center + ud_span / 2,
                       width=0.12, facecolor='#f6ead2', edgecolor='#b3791f', lw=1)
        ax.add_patch(wedge)
        x, y = R * 1.06 * np.cos(np.radians(center)), R * 1.06 * np.sin(np.radians(center))
        ax.scatter([x], [y], color='#b3791f', s=55, marker='D', zorder=5)
        ly_sign = 1 if center == 90 else -1
        ax.text(0, ly_sign * R * 1.62, f'UD補強(φ={center}°側)\nここで評価',
                fontsize=8.5, ha='center', va='center', color='#b3791f')

    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.95, 1.95)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('パイプ周方向4点(青)・UD補強2点(橙◆、φ=90°/270°)の\nTsai-Wu応力評価位置', fontsize=10.5)
    fig.tight_layout()
    save(fig, 'stress_eval_points.svg')


# ============================================================
# 図6: Tsai-Wu破壊包絡線 (04_構造理論編.md)
# ============================================================
def fig_tsai_wu_envelope():
    # 代表的な強度値の例(説明用。実データベースの値そのものではない)
    stx, stxd = 2000e6, 1500e6     # 繊維方向 引張/圧縮
    sty, styd = 60e6, 200e6        # 直角方向 引張/圧縮

    F11 = 1 / (stx * stxd)
    F22 = 1 / (sty * styd)
    F1 = 1 / stx - 1 / stxd
    F2 = 1 / sty - 1 / styd
    F12 = -0.5 * (F11 * F22) ** 0.5

    s1 = np.linspace(-stxd * 1.15, stx * 1.15, 600)
    s2 = np.linspace(-styd * 1.6, sty * 1.6, 600)
    S1, S2 = np.meshgrid(s1, s2)
    Z = F11 * S1 ** 2 + 2 * F12 * S1 * S2 + F22 * S2 ** 2 + F1 * S1 + F2 * S2

    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    ax.contour(S1 / 1e6, S2 / 1e6, Z, levels=[1], colors=['#ab4a3a'], linewidths=2.2)
    ax.contourf(S1 / 1e6, S2 / 1e6, Z, levels=[-1e9, 1], colors=['#dcefe3'], alpha=0.6)

    ax.axhline(0, color='#888', lw=0.6)
    ax.axvline(0, color='#888', lw=0.6)
    ax.scatter([stx / 1e6, -stxd / 1e6], [0, 0], color='#1d6fa5', s=30, zorder=5)
    ax.scatter([0, 0], [sty / 1e6, -styd / 1e6], color='#1d6fa5', s=30, zorder=5)
    ax.text(stx / 1e6, 40, 'stx', fontsize=8, color='#1d6fa5', ha='center')
    ax.text(-stxd / 1e6, 40, '-stxd', fontsize=8, color='#1d6fa5', ha='center')
    ax.text(60, sty / 1e6, 'sty', fontsize=8, color='#1d6fa5', va='center')
    ax.text(60, -styd / 1e6, '-styd', fontsize=8, color='#1d6fa5', va='center')

    ax.scatter([600], [10], color='#2f7d55', s=45, marker='o', zorder=6)
    ax.annotate('安全 (楕円の内側)\nR>1', xy=(600, 10), xytext=(-1400, 150),
                fontsize=8.5, color='#2f7d55',
                arrowprops=dict(arrowstyle='->', color='#2f7d55'))
    ax.scatter([1700], [40], color='#ab4a3a', s=45, marker='x', zorder=6)
    ax.annotate('破壊 (楕円の外側)\nR<1', xy=(1700, 40), xytext=(700, -180),
                fontsize=8.5, color='#ab4a3a',
                arrowprops=dict(arrowstyle='->', color='#ab4a3a'))

    ax.set_xlabel('σ1 (繊維方向応力) [MPa]')
    ax.set_ylabel('σ2 (直角方向応力) [MPa]')
    ax.set_title('Tsai-Wu破壊包絡線 (σ6=0断面、強度値は説明用の例)', fontsize=10.5)
    fig.tight_layout()
    save(fig, 'tsai_wu_envelope.svg')


if __name__ == '__main__':
    fig_cosine_grid()
    fig_fourier_circulation()
    fig_qbar_rotation()
    fig_ring_layers()
    fig_stress_eval_points()
    fig_tsai_wu_envelope()
    print('all figures generated ->', OUT_DIR)

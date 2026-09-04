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


# ============================================================
# 図7: 典型的な2次元翼型のCl-α/Cd-α曲線 (02_空力理論編.md §6)
# ============================================================
def fig_airfoil_polar():
    alpha = np.linspace(-8, 16, 300)

    # 説明用の典型的な曲線(実データベースの特定翼型の値ではない)
    a0 = 2 * np.pi / 180 * 0.9   # 揚力傾斜[1/deg]相当(概ね2π/radを翼型分だけ少し下げた値)
    alpha_l0 = -4.0
    cl_lin = a0 * (alpha - alpha_l0)
    stall_start = 11.0
    cl = np.where(alpha < stall_start, cl_lin,
                  cl_lin[np.searchsorted(alpha, stall_start)] *
                  np.exp(-0.15 * (alpha - stall_start)))

    cd0 = 0.008
    stall_excess = np.clip(alpha - stall_start, 0, None)
    cd = cd0 + 0.012 * ((alpha - 4) / 10) ** 2 + 0.05 * stall_excess ** 1.5 / 10

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 4))

    ax1.plot(alpha, cl, color='#1d6fa5', lw=2)
    ax1.axhline(0, color='#888', lw=0.6)
    ax1.axvline(alpha_l0, color='#ab4a3a', lw=0.8, ls='--')
    ax1.text(alpha_l0, -0.15, 'α_L0', color='#ab4a3a', fontsize=9, ha='center')
    ax1.axvline(stall_start, color='#b3791f', lw=0.8, ls=':')
    ax1.text(stall_start, max(cl) * 0.5, ' 失速開始\n(テーブル外挿)', color='#b3791f', fontsize=8)
    ax1.set_xlabel('迎角 α [deg]')
    ax1.set_ylabel('Cl(揚力係数)')
    ax1.set_title('Cl-α曲線(概念図)', fontsize=10)

    ax2.plot(alpha, cd, color='#2f7d55', lw=2)
    ax2.set_xlabel('迎角 α [deg]')
    ax2.set_ylabel('Cd(抗力係数)')
    ax2.set_title('Cd-α曲線(概念図)', fontsize=10)

    fig.suptitle('2次元翼型データの典型例(特定の翼型の実測値ではなく説明用)', fontsize=10.5, y=1.02)
    fig.tight_layout()
    save(fig, 'airfoil_polar.svg')


# ============================================================
# 図8: 圧力中心Cpの移動 vs 空力中心ACの固定 (02_空力理論編.md §7)
# ============================================================
def fig_pressure_center():
    fig, ax = plt.subplots(figsize=(7.5, 3.6))

    # 簡易翼型シルエット(キャンバー付き、説明用)
    x = np.linspace(0, 1, 200)
    y_camber = 0.06 * np.sin(np.pi * x) * (1 - 0.3 * x)
    y_upper = y_camber + 0.04 * np.sin(np.pi * x) * (1 - x)
    y_lower = y_camber - 0.02 * np.sin(np.pi * x) * (1 - x)
    ax.fill_between(x, y_lower + 0.35, y_upper + 0.35, color='#dcebf5', edgecolor='#14283d', lw=1)

    ax.axhline(0, color='#333', lw=0.8)
    ax.plot([0, 1], [0, 0], color='#333', lw=0.8)
    ax.text(-0.03, 0, '0%\n(前縁)', fontsize=8, ha='right', va='center')
    ax.text(1.03, 0, '100%\n(後縁)', fontsize=8, ha='left', va='center')

    # 空力中心(固定)
    ax.scatter([0.25], [0], color='#2f7d55', marker='*', s=180, zorder=6)
    ax.text(0.25, -0.13, '空力中心(AC)\n迎角によらずほぼ一定', fontsize=8.5, color='#2f7d55', ha='center')

    # 圧力中心(迎角で移動)の例3点
    cp_examples = [(0.60, '低迎角'), (0.35, '中迎角'), (0.27, '高迎角')]
    ys = [0.06, 0.10, 0.14]
    for (cpx, label), yy in zip(cp_examples, ys):
        ax.scatter([cpx], [0], color='#ab4a3a', s=45, zorder=5)
        ax.annotate('', xy=(cpx, 0), xytext=(cpx, yy),
                     arrowprops=dict(arrowstyle='->', color='#ab4a3a', lw=0.8))
        ax.text(cpx, yy + 0.015, f'{label}\nCp', fontsize=7.5, color='#ab4a3a', ha='center')

    ax.set_xlim(-0.15, 1.15)
    ax.set_ylim(-0.2, 0.55)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('圧力中心(Cp、迎角で移動)と空力中心(AC、ほぼ固定)の違い(概念図)', fontsize=10.5)
    fig.tight_layout()
    save(fig, 'pressure_center.svg')


# ============================================================
# 図9: プライごとの物性→積層等価物性への重み付き平均 (04_構造理論編.md §3)
# ============================================================
def fig_ply_to_laminate():
    # 説明用の例(4層、角度違い)。実データではない
    angles = [0, 45, -45, 90]
    thick = [0.15, 0.20, 0.20, 0.15]  # mm、厚み比の重み
    Ex, Ey, Gxy, nu_xy = 130e9, 9e9, 5e9, 0.30
    nu_yx = nu_xy * Ey / Ex
    R = 1 / (1 - nu_xy * nu_yx)
    Qxx, Qyy, Qxy, Qss = R * Ex, R * Ey, R * nu_yx * Ex, Gxy
    u1 = 0.125 * (3 * Qxx + 3 * Qyy + 2 * Qxy + 4 * Qss)
    u2 = 0.5 * (Qxx - Qyy)
    u3 = 0.125 * (Qxx + Qyy - 2 * Qxy - 4 * Qss)

    def q11_of(theta_deg):
        t = np.radians(theta_deg)
        return u1 + u2 * np.cos(2 * t) + u3 * np.cos(4 * t)

    q11_per_ply = [q11_of(a) for a in angles]
    total_t = sum(thick)
    ex_eff = sum(q * t for q, t in zip(q11_per_ply, thick)) / total_t   # 簡易版(A11相当の重み付き平均のイメージ)

    fig, ax = plt.subplots(figsize=(7, 4.2))
    xs = np.arange(len(angles))
    bars = ax.bar(xs, np.array(q11_per_ply) / 1e9, width=0.5, color='#8fb6d4', edgecolor='#14283d')
    for i, (a, t) in enumerate(zip(angles, thick)):
        ax.text(i, q11_per_ply[i] / 1e9 + 2, f'{a}°\n厚み比{t/total_t:.0%}', ha='center', fontsize=8.5)

    ax.axhline(ex_eff / 1e9, color='#ab4a3a', lw=2, ls='--')
    ax.text(len(angles) - 0.4, ex_eff / 1e9 + 3, '積層全体の等価値\n(厚み比で重み付き平均)',
            color='#ab4a3a', fontsize=8.5)

    ax.set_ylim(0, max(q11_per_ply) / 1e9 * 1.22)
    ax.set_xticks(xs)
    ax.set_xticklabels([f'層{i+1}' for i in range(len(angles))])
    ax.set_ylabel('Q̄11 [GPa](層ごとの軸方向剛性に相当)')
    ax.set_title('層ごとに異なる物性 → 積層全体の等価物性への重み付き平均(概念図)', fontsize=10.5)
    fig.tight_layout()
    save(fig, 'ply_to_laminate.svg')


# ============================================================
# 図10: 桁の片持ち梁モデル(座標系) (04_構造理論編.md §1)
# ============================================================
def fig_cantilever_model():
    fig, ax = plt.subplots(figsize=(8, 4.4))

    beam_y = 0
    ax.plot([0, 10], [beam_y, beam_y], color='#14283d', lw=4, solid_capstyle='butt', zorder=3)

    # 固定端のハッチング(翼根)
    for i in range(8):
        yy = -0.35 + i * 0.1
        ax.plot([-0.35, -0.05], [yy, yy + 0.1], color='#333', lw=1)
    ax.plot([-0.05, -0.05], [-0.35, 0.45], color='#14283d', lw=2)

    # 座標軸(梁の上側)
    ax.annotate('', xy=(1.3, beam_y), xytext=(0, beam_y), arrowprops=dict(arrowstyle='->', color='#2f7d55', lw=1.5))
    ax.text(1.45, beam_y + 0.55, 'x(スパン方向)', color='#2f7d55', fontsize=8.5, ha='left')
    ax.annotate('', xy=(0, beam_y + 1.15), xytext=(0, beam_y), arrowprops=dict(arrowstyle='->', color='#ab4a3a', lw=1.5))
    ax.text(0.15, beam_y + 1.2, 'y(揚力方向)', color='#ab4a3a', fontsize=8.5)

    # 節点ラベル(梁の上側、座標軸と被らない位置)
    ax.text(0, beam_y + 0.75, '翼根(節点1)\n完全固定(変位・回転=0)', fontsize=8.5, ha='left', color='#333')
    ax.text(10, beam_y + 0.35, '翼端\n(自由端)', fontsize=8.5, ha='center', color='#333')
    ax.scatter([10], [0], color='#14283d', s=30, zorder=5)

    # 分布荷重(揚力)矢印: 下から上向き(揚力は上向きの力であることを明示)
    for x in np.linspace(1, 9.3, 9):
        h = 0.5 + 0.15 * np.sin((x / 10) * np.pi)
        ax.annotate('', xy=(x, beam_y), xytext=(x, beam_y - h),
                     arrowprops=dict(arrowstyle='->', color='#1d6fa5', lw=1.2))
    ax.text(5, -1.15, '分布荷重(揚力、翼根〜翼端で変化。上向きの力)', color='#1d6fa5', fontsize=9, ha='center')

    ax.set_xlim(-1.2, 11)
    ax.set_ylim(-1.5, 1.6)
    ax.axis('off')
    ax.set_title('桁の片持ち梁モデル(翼根固定・翼端自由、分布荷重を受ける)', fontsize=10.5)
    fig.tight_layout()
    save(fig, 'cantilever_model.svg')


# ============================================================
# 図11: 3D梁要素の6自由度 (04_構造理論編.md §6)
# ============================================================
def fig_beam_6dof():
    fig, ax = plt.subplots(figsize=(7.5, 4.5))

    n1, n2 = (2.6, 1.0), (8.6, 1.0)
    ax.plot([n1[0], n2[0]], [n1[1], n2[1]], color='#14283d', lw=5, solid_capstyle='round', zorder=1)
    ax.scatter([n1[0], n2[0]], [n1[1], n2[1]], color='#14283d', s=70, zorder=5)
    ax.text(n1[0], n1[1] - 0.35, '節点 i', fontsize=10, ha='center')
    ax.text(n2[0], n2[1] - 0.35, '節点 i+1', fontsize=10, ha='center')
    ax.text(n2[0], n2[1] + 2.55, '(節点i+1にも\n同じ6自由度がある)', fontsize=8, ha='center', color='#666')

    # ---- 左側の凡例エリア: 並進3方向(u,v,w) ----
    ox, oy = 0.9, 3.6
    trans = [('u(軸方向)', (1, 0), '#1d6fa5'), ('v(揚力方向)', (0, 1), '#ab4a3a'), ('w(抗力方向)', (-0.7, 0.7), '#b3791f')]
    ax.text(ox, oy + 1.5, '並進 3方向', fontsize=9.5, ha='center', fontweight='bold')
    for label, (dx, dy), c in trans:
        ax.annotate('', xy=(ox + dx * 1.1, oy + dy * 1.1), xytext=(ox, oy),
                     arrowprops=dict(arrowstyle='->', color=c, lw=1.8))
        ax.text(ox + dx * 1.35, oy + dy * 1.35, label, fontsize=8.5, color=c, ha='center', va='center')

    # ---- 右側の凡例エリア: 回転3方向(θx,θy,θz) ----
    from matplotlib.patches import Arc
    rx = 6.5
    rot_specs = [('θx(ねじれ)', 0, '#2f7d55'), ('θy', 1.0, '#6b4fa0'), ('θz', -1.0, '#c26a2d')]
    ax.text(rx, oy + 1.5, '回転 3方向', fontsize=9.5, ha='center', fontweight='bold')
    for label, offset, c in rot_specs:
        cx, cy = rx + offset * 1.15, oy
        arc = Arc((cx, cy), 0.55, 0.55, angle=0, theta1=30, theta2=330, color=c, lw=1.6)
        ax.add_patch(arc)
        ax.text(cx, cy - 0.5, label, fontsize=8, color=c, ha='center', va='top')

    # 凡例エリアから節点iへの引き出し線
    ax.annotate('', xy=(n1[0] - 0.15, n1[1] + 0.15), xytext=(ox, oy - 0.7),
                 arrowprops=dict(arrowstyle='-', color='#999', lw=0.8, ls='dotted'))
    ax.annotate('', xy=(n1[0] + 0.15, n1[1] + 0.15), xytext=(rx, oy - 0.7),
                 arrowprops=dict(arrowstyle='-', color='#999', lw=0.8, ls='dotted'))

    ax.set_xlim(-0.5, 10)
    ax.set_ylim(-0.3, 5.6)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('3D梁要素: 1節点あたり6自由度(並進3+回転3)', fontsize=10.5)
    fig.tight_layout()
    save(fig, 'beam_6dof.svg')


# ============================================================
# 図12: EIyの2/3係数 vs 第一原理のπ/4係数 (07_既知の制限事項.md)
# ============================================================
def fig_eiy_coefficient_bar():
    fig, ax = plt.subplots(figsize=(5, 4))
    labels = ['コード実装\n(2/3 ≈ 0.667)', '第一原理の積分\n(π/4 ≈ 0.785)']
    vals = [2 / 3, np.pi / 4]
    colors = ['#b3791f', '#1d6fa5']
    bars = ax.bar(labels, vals, color=colors, width=0.5)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.02, f'{v:.3f}', ha='center', fontsize=10)
    diff_pct = (vals[1] - vals[0]) / vals[1] * 100   # 第一原理値(π/4)を基準とした差(本編の記述と統一)
    ax.annotate(f'約{diff_pct:.0f}%の差', xy=(0.5, (vals[0] + vals[1]) / 2), xytext=(0.5, 0.9),
                fontsize=9.5, ha='center', color='#ab4a3a',
                arrowprops=dict(arrowstyle='-[', color='#ab4a3a'))
    ax.set_ylim(0, 1.0)
    ax.set_ylabel('EIy円環積分の係数')
    ax.set_title('EIy計算式の係数比較', fontsize=10.5)
    fig.tight_layout()
    save(fig, 'eiy_coefficient_bar.svg')


# ============================================================
# 図13: 桁材料データベースの物性比較 (05_構造実装編.md §1)
# ============================================================
def fig_material_comparison():
    # 材料データベース\材料物性.csv の実データ(2026-08時点)
    materials = ['TR30', 'HRX350\nG125S_G35', '46t', '60t', '80t', 'HR40']
    ex_gpa = [128.9, 217.53, 237.47, 349.96, 424.95, 251.0]

    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(materials, ex_gpa, color='#8fb6d4', edgecolor='#14283d')
    for b, v in zip(bars, ex_gpa):
        ax.text(b.get_x() + b.get_width() / 2, v + 5, f'{v:.0f}', ha='center', fontsize=8.5)
    ax.set_ylabel('Ex(繊維方向ヤング率) [GPa]')
    ax.set_title('材料データベースの繊維方向ヤング率Ex比較(材料物性.csvの実データ)', fontsize=10.5)
    fig.tight_layout()
    save(fig, 'material_comparison.svg')


# ============================================================
# 図14: ワイヤー機の桁支持と1次不静定 (04_構造理論編.md §10)
# ============================================================
def _wall_hatch(ax, x, y0, y1, n=8, length=0.35, angle=45):
    """固定端(壁)のハッチング。fig_cantilever_modelと同じ流儀。"""
    ax.plot([x, x], [y0, y1], color='#333', lw=2.5, solid_capstyle='butt')
    dy = (y1 - y0) / n
    dx = -length * np.cos(np.radians(angle))
    ddy = -length * np.sin(np.radians(angle))
    for i in range(n + 1):
        yy = y0 + dy * i
        ax.plot([x, x + dx], [yy, yy + ddy], color='#333', lw=1.0)


def _ground_hatch(ax, x, y, w=0.6, n=6, length=0.22, angle=-55):
    """アンカー(胴体側固定点)のハッチング。"""
    ax.plot([x - w / 2, x + w / 2], [y, y], color='#333', lw=2.0)
    for i in range(n + 1):
        xx = x - w / 2 + (w / n) * i
        ax.plot([xx, xx + length * np.cos(np.radians(angle))],
                [y, y + length * np.sin(np.radians(angle))], color='#333', lw=0.9)


def fig_wire_brace_indeterminate():
    WIRE = '#7a4fab'
    fig, ax = plt.subplots(figsize=(7.9, 4.6))
    ax.set_xlim(-2.2, 10.8)
    ax.set_ylim(-3.6, 3.2)
    ax.axis('off')
    ax.set_aspect('equal')

    L, xWire, hEff = 10.0, 6.5, 2.0
    ax.plot([0, L], [0, 0], color='#14283d', lw=4, solid_capstyle='round', zorder=3)
    _wall_hatch(ax, 0, -0.9, 0.9)
    ax.plot([L], [0], marker='o', ms=4, color='#14283d', zorder=4)
    ax.plot([xWire], [0], marker='o', ms=7, color='#14283d', mfc='white', mew=2, zorder=5)

    anchor = (0, -hEff)
    _ground_hatch(ax, anchor[0], anchor[1] - 0.05, w=1.0)
    ax.plot([xWire, anchor[0]], [0, anchor[1]], color=WIRE, lw=2.2, zorder=4)
    ax.plot([anchor[0]], [anchor[1]], marker='^', ms=8, color=WIRE, zorder=5)

    ax.add_patch(FancyArrowPatch((0, -1.5), (xWire, -1.5), arrowstyle='<->',
                                  color='#2f7d55', lw=1.4, mutation_scale=10, shrinkA=0, shrinkB=0))
    ax.text(xWire / 2, -1.72, 'xWire (スパン方向距離)', color='#2f7d55', ha='center', va='top', fontsize=10)
    ax.add_patch(FancyArrowPatch((xWire + 0.55, 0), (xWire + 0.55, anchor[1]), arrowstyle='<->',
                                  color='#ab4a3a', lw=1.4, mutation_scale=10, shrinkA=0, shrinkB=0))
    ax.text(xWire + 0.75, anchor[1] / 2, 'hEffective\n(マスト長+定常時たわみ)',
            color='#ab4a3a', ha='left', va='center', fontsize=9.5)

    ax.annotate('翼根: 完全固定\n反力6成分\n(Fx,Fy,Fz,Mx,My,Mz)', xy=(0, 0.05), xytext=(-2.1, 2.4),
                fontsize=10, color='#333', ha='left', arrowprops=dict(arrowstyle='-', color='#333', lw=1.0))
    ax.annotate('ワイヤー取付点', xy=(xWire, 0.15), xytext=(xWire - 2.6, 1.6),
                fontsize=10, color='#14283d', ha='left', arrowprops=dict(arrowstyle='-', color='#14283d', lw=1.0))
    ax.annotate('ワイヤー反力1成分\n(張力T、方向は固定)', xy=(xWire / 2, anchor[1] / 2), xytext=(4.6, -3.15),
                fontsize=10, color=WIRE, ha='left', arrowprops=dict(arrowstyle='-', color=WIRE, lw=1.0))
    ax.annotate('アンカー\n(胴体側固定点、動かない)', xy=anchor, xytext=(-2.1, -3.1),
                fontsize=9.5, color=WIRE, ha='left', arrowprops=dict(arrowstyle='-', color=WIRE, lw=1.0))
    ax.text(7.2, 2.7, '未知数 7個\n(翼根の反力6+ワイヤーの張力1)\n＞ 釣り合い式 6本\n→ 1次不静定',
            fontsize=10.5, color='#333', ha='left', va='top',
            bbox=dict(boxstyle='round,pad=0.4', fc='#f5f0fa', ec=WIRE, lw=1.2))

    fig.tight_layout()
    save(fig, 'wire_brace_indeterminate.svg')


# ============================================================
# 図15: たわみ適合法の3ステップ (04_構造理論編.md §10)
# ============================================================
def fig_wire_force_method():
    WIRE, FAINT = '#7a4fab', '#c8ccd2'
    L, xWire = 10.0, 6.5
    x = np.linspace(0, L, 200)
    iw = int((xWire / L) * (len(x) - 1))
    fig, axes = plt.subplots(1, 3, figsize=(11.4, 4.0))

    def base(ax):
        ax.set_xlim(-1.6, 11.2)
        ax.set_ylim(-1.3, 3.6)
        ax.axis('off')
        ax.set_aspect('equal')
        ax.plot(x, np.zeros_like(x), color=FAINT, lw=2.5, ls='--')
        _wall_hatch(ax, 0, -0.7, 0.7, n=7, length=0.3)

    # ① ケース0
    ax = axes[0]
    base(ax)
    y0 = 2.6 * (x / L) ** 2
    ax.plot(x, y0, color='#14283d', lw=3.2)
    ax.plot([x[iw]], [y0[iw]], marker='o', ms=6, color='#14283d', mfc='white', mew=1.8)
    ax.add_patch(FancyArrowPatch((x[iw], 0), (x[iw], y0[iw]), arrowstyle='-|>',
                                  color='#ab4a3a', lw=1.6, mutation_scale=12, shrinkA=0, shrinkB=2))
    ax.text(x[iw] + 0.3, y0[iw] * 0.5, 'δ0', color='#ab4a3a', fontsize=13, va='center')
    ax.set_title('① ケース0\n空力荷重のみ(ワイヤーなし)', fontsize=11, color='#333')
    ax.text(L * 0.5, -1.15, '取付点の変位をワイヤー方向へ投影 → δ0', fontsize=8.5, color='#333', ha='center')

    # ② ケース1
    ax = axes[1]
    base(ax)
    y1 = 0.55 * (x / L) ** 2
    ax.plot(x, y1, color='#14283d', lw=3.2)
    ax.plot([x[iw]], [y1[iw]], marker='o', ms=6, color='#14283d', mfc='white', mew=1.8)
    ax.add_patch(FancyArrowPatch((x[iw], y1[iw]), (x[iw] - 1.3, y1[iw] - 0.9), arrowstyle='-|>',
                                  color=WIRE, lw=2.0, mutation_scale=14, shrinkA=0, shrinkB=0))
    ax.text(x[iw] - 1.65, y1[iw] - 1.25, '単位張力\n(ワイヤー方向)', color=WIRE, fontsize=8.5, ha='right', va='top')
    ax.add_patch(FancyArrowPatch((x[iw], 0), (x[iw], y1[iw]), arrowstyle='-|>',
                                  color='#ab4a3a', lw=1.6, mutation_scale=12, shrinkA=0, shrinkB=2))
    ax.text(x[iw] + 0.3, y1[iw] * 0.5 + 0.15, 'δ1', color='#ab4a3a', fontsize=13, va='center')
    ax.set_title('② ケース1\n単位ワイヤー力のみ', fontsize=11, color='#333')
    ax.text(L * 0.5, -1.15, '同じ点の変位(単位力あたり)→ δ1', fontsize=8.5, color='#333', ha='center')

    # ③ 重ね合わせ
    ax = axes[2]
    base(ax)
    yC = y0 - 2.05 * y1
    ax.plot(x, yC, color='#14283d', lw=3.2)
    ax.plot([x[iw]], [yC[iw]], marker='o', ms=6, color='#14283d', mfc='white', mew=1.8)
    anchor = (0, -1.05)
    _ground_hatch(ax, anchor[0], anchor[1] - 0.03, w=0.8, n=5, length=0.18)
    ax.plot([x[iw], anchor[0]], [yC[iw], anchor[1]], color=WIRE, lw=2.0)
    ax.plot([anchor[0]], [anchor[1]], marker='^', ms=7, color=WIRE)
    ax.set_title('③ 重ね合わせ = ①＋T×②', fontsize=11, color='#333')
    ax.text(L * 0.5, -1.25, 'T = (目標値 − δ0) / δ1 を満たすTで合成', fontsize=8.5, color='#333', ha='center')

    fig.tight_layout()
    save(fig, 'wire_force_method.svg')


if __name__ == '__main__':
    fig_cosine_grid()
    fig_fourier_circulation()
    fig_qbar_rotation()
    fig_ring_layers()
    fig_stress_eval_points()
    fig_tsai_wu_envelope()
    fig_airfoil_polar()
    fig_pressure_center()
    fig_ply_to_laminate()
    fig_cantilever_model()
    fig_beam_6dof()
    fig_eiy_coefficient_bar()
    fig_material_comparison()
    fig_wire_brace_indeterminate()
    fig_wire_force_method()
    print('all figures generated ->', OUT_DIR)

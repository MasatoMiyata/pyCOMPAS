import numpy as np

def heatb(q1, q2, cn, rm, t1, t2, w, dx, dy, ifl1, ifl2):

    jf1 = ifl1
    jf2 = abs(ifl2)
    r1 = rm[abs(ifl1) - 1]  # Adjusting for 0-indexing

    while True:
        if jf1 > 0:
            if jf2 in [1, 2, 3]:
                r2 = rm[jf2 - 1]
                q = 2.0 * r1 * r2 / (r1 + r2) * dx / dy
                q2 += q * t2
                q1 += q
            elif jf2 in [4, 5, 6]:
                a = cn[jf2 - 4]
                t = cn[jf2 - 1]
                q = 2.0 * a * r1 / (a + 2.0 * r1 / dy) * dx / dy
                q2 += q * t
                q1 += q
                t2 = (a * t + 2.0 * r1 / dy * t1) / (a + 2.0 * r1 / dy)
            elif jf2 in [7, 8, 9]:
                t = cn[jf2 - 1]
                q = 2.0 * r1 * dx / dy
                q2 += q * t
                q1 += q
                t2 = t
            elif jf2 == 10:
                t2 = t1
            break
        elif ifl2 < 0 and ifl2 > -4:
            r2 = rm[jf2 - 1]
            q = 2.0 * r1 * r2 / (r1 + r2) * dx / dy
            q2 += q * t2 + r1 * dx / (r1 + r2) * w
            q1 += q
            break
        else:
            jf1 = abs(ifl1)

    return q1, q2, t2


def dmake(isx, iex, isy, iey, k, jfl):
    for i in range(isx, iex + 1):
        for j in range(isy, iey + 1):
            jfl[i, j] = k


import numpy as np

def relax(t, ix, iy, rm, cn, jfl, wx, wy, dx, dy, ic, eps):
    """壁体の断面形状（二次元）と境界条件等を与えて、壁体内部及び表面の温度を求める
    （定常計算）

    Args:

        ix (_type_): X方向のメッシュ数
        iy (_type_): Y方向のメッシュ数
        rm (_type_): 材料番号iの熱伝導率[kcal/mhK]
        cn (_type_): 熱伝導率[kcal/m2hK]
                    上記熱伝導率に対応する流体などの温度[℃]
                    壁体が接する物体の温度[℃]
        jfl (_type_): メッシュの計算条件
        wx (_type_): X方向に平行な面発熱体の発熱量[kcal/m2h]
        wy (_type_): Y方向に平行な面発熱体の発熱量[kcal/m2h]
        dx (_type_): X方向のメッシュ間隔[m]
        dy (_type_): Y方向のメッシュ間隔[m]
        ic (_type_): 打ち切り計算回数
        eps (_type_): 計算終了条件

    Returns:
        t (_type_): 各メッシュの温度及び壁面の表面温度[℃]
    """

    for k in range(ic):
        ij = 0
        for i in range(ix):
            for j in range(iy):
                jfl1 = jfl[i, j]
                if jfl1 == 0 or jfl1 <= -4:
                    continue

                t1 = t[i, j]
                q1 = 0.0
                q2 = 0.0

                # Call heatb for each direction
                q1, q2, _ = heatb(q1, q2, cn, rm, t1, t[i, j - 1], wx, dx, dy, jfl1, jfl[i, j - 1])
                q1, q2, _ = heatb(q1, q2, cn, rm, t1, t[i + 1, j], wy, dy, dx, jfl1, jfl[i + 1, j])
                q1, q2, _ = heatb(q1, q2, cn, rm, t1, t[i, j + 1], wx, dx, dy, jfl1, jfl[i, j + 1])
                q1, q2, _ = heatb(q1, q2, cn, rm, t1, t[i - 1, j], wy, dy, dx, jfl1, jfl[i - 1, j])

                t[i, j] = q2 / q1
                if abs(t1 - t[i, j]) > eps:
                    ij = 1

        if ij == 0:
            break

    return t, k


if __name__ == '__main__':

    print("テスト未実装")


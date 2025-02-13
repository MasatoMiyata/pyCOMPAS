import numpy as np
import math

def pol2(n, x, y, xa):
  # x = np.array(x)
  # y = np.array(y)
    if xa < x[0]:
        print('*** ERROR input pol2 subroutine ***')
        raise ValueError("Invalid input")
    for j in range(1, n):
        if xa <= x[j]:
            i = j - 1
            ya = (xa - x[i]) * (y[i + 1] - y[i]) / (x[i + 1] - x[i]) + y[i]
            return ya
    print('*** ERROR input pol2 subroutine ***')
    raise ValueError("Invalid input")

def pol3(m, n, x, y, z, xa, ya):
    """
    Interpolates ZA value for given XA, YA using bilinear interpolation method.

    Parameters:
        m: int
            Number of dataset X.
        n: int
            Number of dataset Y.
        x: np.array
            Dataset for X.
        y: np.array
            Dataset for Y.
        z: np.array
            Dataset for Z.
        xa: float
            Input data for XA.
        ya: float
            Input data for YA.

    Returns:
        za: float
            Output data F(XA,YA).
    """
    if xa < x[0]:
        raise ValueError("*** ERROR INPUT POL3 FUNCTION ***")

    for k in range(1, m):
        if xa <= x[k]:
            break
    else:
        raise ValueError("*** ERROR INPUT POL3 FUNCTION ***")

    i = k - 1

    if ya < y[0]:
        raise ValueError("*** ERROR INPUT POL3 FUNCTION ***")

    for k in range(1, n):
        if ya <= y[k]:
            break
    else:
        raise ValueError("*** ERROR INPUT POL3 FUNCTION ***")

    j = k - 1

    z1 = (xa - x[i]) * (z[i + 1, j] - z[i, j]) / (x[i + 1] - x[i]) + z[i, j]
    z2 = (xa - x[i]) * (z[i + 1, j + 1] - z[i, j + 1]) / (x[i + 1] - x[i]) + z[i, j + 1]
    za = (ya - y[j]) * (z2 - z1) / (y[j + 1] - y[j]) + z1

    return za



def drinf(w, h, tr, ta, dq):

    """建物内のドア開放時に、その両室の温度差によって侵入する隙間風量を計算する

    Args:
        w, h (float): ドアの幅, 高さ [m]
        tr, ta (float): 計算室温, 隣室温 (tr≧ta+0.5 とする) [℃]
        dq (float): 計算室の空調吹出量から吸込量を引いたもの ΔQ [m^3/h]

    Returns:
        qi (float): ドアからの流入隙間風量 [m^3/h]

    制約・欠点
        1) ta + 10 ≧ tr ≧ ta + 0.5  (⊿Q > 0 のとき) である。
        2) 副プログラム pol2 (p.90  3.2.6), pol3 (p.91  3.2.6) が必要である。
    """

    c = 0.8
    g = 9.8
    dtx = np.array([0.5, 1.0, 2.0, 5.0, 10.0])
    vfy = np.array([0.0, 0.05, 0.10, 0.15, 0.2, 0.25, 0.3])
    cvz0 = np.array([
        [1.0,  1.0,  1.0,  1.0,  1.0],
        [0.66, 0.76, 0.81, 0.86, 0.93],
        [0.46, 0.59, 0.65, 0.75, 0.86],
        [0.24, 0.47, 0.55, 0.68, 0.81],
        [-0.1,  0.36, 0.49, 0.65, 0.78],
        [-0.6,  0.15, 0.46, 0.62, 0.77],
        [-1.0, -0.5,  0.4,  0.62, 0.78]
    ])
    cvz = cvz0.T

    cty = np.array([1.3, 1.0, 0.85, 0.77, 0.85])

    gamr = 353 / (273 + tr)
    gama = 353 / (273 + ta)
    dgam = gama - gamr

    if dgam <= 0:
        print('*** error input  drinf function ***')
        raise ValueError("Invalid input")

    gamm = 0.5 * (gamr + gama)

    if dq <= 0.0:
        qi = 1200 * c * w * (g * dgam / gamm) **0.5  * h ** 1.5
        return qi

    dt = tr - ta
    vf = dq / (w * h * 3600)

    ct = pol2(5, dtx, cty, dt)
    cv = pol3(5, 7, dtx, vfy, cvz, dt, vf)

    if cv <= 0.0:
        cv = 0.0

    y1 = g * dgam / gamm * h - (dq / (3600 * w * h)) ** 2

    if y1 <= 0.0:
        y1 = 0.0

    qi = 1200 * ct * cv * w * gamm / g / dgam * y1 ** 1.5

   # print ('dt=', dt, ' dq=', dq, ' ct=', ct, ' cv=', cv)

    return qi

if __name__ == "__main__":
    w = 0.9   # ドアの巾 (m)
    h = 2.0   # ドアの高さ (m)
    tr = 22.0   # 計算室温 (℃)

    ta = [tr + 0.5 - it for it in range(1, 11)]
    dq_values = [0, 360, 720, 1080]

    print('*** door infiltration (m^3/h) ***')
    print('    w =', w, '(m),  h =', h, '(m),  tr =', tr)
    print('          ta (deg C)')
    print('    dq(m3/h)    ', ta)

    for dq in dq_values:
        q = [drinf(w, h, tr, t, dq) for t in ta]
        q_rounded = [round(val, 1) for val in q]  # 小数点以下1桁に丸める
        print('       ', dq, '    ', q_rounded)

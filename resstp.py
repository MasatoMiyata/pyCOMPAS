import numpy as np

def resstp(n, r, c, ao, at, aa, alp, i):
    """一般の多層壁の単位応答（ステップ応答）を求める。

    Args:
        n (_type_): 壁体の層数
        r (_type_): 各層の熱抵抗[m2hK/kcal]
        c (_type_):  各層の熱容量[kcal/m2℃]
        
    Returns:
        ao (_type_): 単位応答の係数
        at (_type_): 単位応答の係数
        aa (_type_): 単位応答の係数
        alp (_type_): 単位応答の係数
        i (_type_): 単位応答の係数
    """
    
    rc = r * c
    d = np.zeros((20, 3))
    dd = np.zeros((20, 3))
    cd = np.zeros((20, 4))
    cdd = np.zeros((20, 4))
    imx, almx = 15, 90
    ao = 1.0 / ao
    i = 0
    s = 0

    while True:
        for k in range(n):
            d[k, :] = [1.0, r[k], 0.0]
            dd[k, :] = [0.5 * rc[k], 0.1666667 * r[k] * rc[k], c[k]]

        cd[0, :] = d[0, :]
        cdd[0, :] = dd[0, :]
        for k in range(1, n):  # Fortranの2からnまでのループはPythonでは1からn-1まで
            k1 = k - 1
            cd[k, 0] = cd[k1, 0] * d[k, 0] + cd[k1, 1] * d[k, 2]
            cd[k, 1] = cd[k1, 0] * d[k, 1] + cd[k1, 1] * d[k, 0]
            cd[k, 2] = cd[k1, 2] * d[k, 0] + cd[k1, 3] * d[k, 2]
            cd[k, 3] = cd[k1, 2] * d[k, 1] + cd[k1, 3] * d[k, 0]
            cdd[k, 0] = cd[k1, 0] * dd[k, 0] + cdd[k1, 0] * d[k, 0] + cd[k1, 1] * dd[k, 2] + cdd[k1, 1] * d[k, 2]
            cdd[k, 1] = cd[k1, 0] * dd[k, 1] + cdd[k1, 0] * d[k, 1] + cd[k1, 1] * dd[k, 0] + cdd[k1, 1] * d[k, 0]
            cdd[k, 2] = cd[k1, 2] * dd[k, 0] + cdd[k1, 2] * d[k, 0] + cd[k1, 3] * dd[k, 2] + cdd[k1, 3] * d[k, 2]
            cdd[k, 3] = cd[k1, 2] * dd[k, 1] + cdd[k1, 2] * d[k, 1] + cd[k1, 3] * dd[k, 0] + cdd[k1, 3] * d[k, 0]

        y = cd[n - 1, 1]
        yd = cdd[n - 1, 1]
        if i != 0:
            w1 = sum(1.0 / (s + alp[ii]) for ii in range(i))
            yd -= y * w1

        s1 = s - y / yd
        if s1 >= s:
            i += 1
            alp[i] = -s1
            at[i] = 1.0 / (s1 * cdd[n - 1, 2])
            aa[i] = cd[n - 1, 3] * at[i]
            if i < imx and alp[i] < almx:
                s = s1
                continue
            break

        s = s1
        for k in range(n):
            if c[k] == 0:
                break
            w1 = np.sqrt(-s * rc[k])
            w2 = np.cos(w1)
            w3 = np.sin(w1)
            d[k, 0] = w2
            d[k, 1] = r[k] * w3 / w1
            d[k, 2] = -w1 * w3 / r[k]
            dd[k, 0] = 0.5 * rc[k] * w3 / w1
            dd[k, 1] = 0.5 * r[k] * rc[k] * (w3 / w1 - w2) / w1**2
            dd[k, 2] = 0.5 * c[k] * (w3 / w1 + w2)

        i += 1
        alp[i] = -s1
        at[i] = 1.0 / (s1 * cdd[n - 1, 1])
        aa[i] = cd[n - 1, 3] * at[i]

        if i < imx and alp[i] < almx:
            break

    return ao, at, aa, alp, i


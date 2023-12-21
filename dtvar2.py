import numpy as np

from sucft2 import sucft2
from suc2 import suc2

def dtvar2(istep, ik, ao, at, aa, alp, ept, epa, dt, ndt, ip, tr, q):
    """逐次積分熱流法により室温、熱流の計算を行う。
    入力は壁の単位貫流・吸熱応答の諸係数。

    Args:
        istep (bool): _description_
        ik (_type_): _description_
        ao (_type_): _description_
        at (_type_): _description_
        aa (_type_): _description_
        alp (_type_): _description_
        ept (_type_): _description_
        epa (_type_): _description_
        dt (_type_): _description_
        ndt (_type_): _description_
        ip (_type_): _description_
        tr (_type_): _description_
        q (_type_): _description_
    """

    r = np.zeros(5)
    xt = np.zeros(5)
    xa = np.zeros(5)
    y = np.zeros(5)
    xto = np.zeros(10)
    xao = np.zeros(10)
    r1 = np.zeros((10, 5))
    xa1 = np.zeros((10, 5))
    y1 = np.zeros((10, 5))
    z1 = np.zeros(5)
    tr1 = 0.0

    if istep == 1:

        for idt in range(ndt):
            sucft2(ik, ao, at, aa, alp, ept, epa, dt[idt], r, xt, xa, y, xto[idt], xao[idt])
            for k in range(ik):
                r1[idt, k] = r[k]
                xa1[idt, k] = xa[k]
                y1[idt, k] = y[k]

        for k in range(ik):
            z1[k] = 0.0

    elif istep == 2:

        for k in range(ik):
            r[k] = r1[ndt - 1, k]
            xa[k] = xa1[ndt - 1, k]
            y[k] = y1[ndt - 1, k]

        suc2(ip, ik, ao, r, xa, y, xao[ndt - 1], dt[ndt - 1], tr1, z1, tr, q)


if __name__ == '__main__':
    
    print("テスト未実装")


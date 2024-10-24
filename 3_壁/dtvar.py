import numpy as np
from sucft1 import sucft1
from suc1 import suc1

def dtvar(istep, ik, ao, at, aa, alp, eps, dt, ndt, ip, tr, q):
    """逐次積分熱流法により室温、熱流の計算を行う。
    入力は壁の単位貫流・吸熱応答の諸係数。

    Args:
        istep (bool): 計算ステップ（1: 初期設定、2:本計算）
        ik (_type_): 根の数（ik≦10）
        ao (_type_): 単位応答の定数項
        at (_type_): 単位応答の貫流係数項
        aa (_type_): 単位応答の吸熱係数項
        alp (_type_): 単位応答の根
        eps (_type_): 単位応答のデルタ関数係数
        dt (_type_): 計算時間間隔（大きさndt以上の一次元配列）[h]
        ndt (_type_): istep=1のとき、DTの種類数（1～10）、istep=2のとき、DT識別記号
        ip (_type_): 計算種類（1:熱流計算、2: 室温計算）
        tr (_type_): 室温[℃]
        q (_type_): 熱流、供給熱量 [kcal/h]
    """

    r = np.zeros(10)
    xt = np.zeros(10)
    xa = np.zeros(10)
    r1 = np.zeros((10, 10))
    xa1 = np.zeros((10, 10))
    txt = np.zeros(10)
    txa = np.zeros(10)
    z1 = np.zeros(10)
    tr1 = 0.0

    if istep == 1:

        for idt in range(ndt):
            sucft1(ik, at, aa, alp, dt[idt], r, xt, xa, txt[idt], txa[idt])
            for k in range(ik):
                r1[idt, k] = r[k]
                xa1[idt, k] = xa[k]
        for k in range(ik):
            z1[k] = 0.0

    elif istep == 2:

        for k in range(ik):
            r[k] = r1[ndt - 1, k]
            xa[k] = xa1[ndt - 1, k]
        suc1(ip, ik, ao, r, xa, txa[ndt - 1], eps, dt[ndt - 1], tr1, z1, tr, q)

    return tr, q


if __name__ == '__main__':
    
    print("テスト未実装")



import numpy as np

def dend2(xmax, ymax, dl, gmax, icmax, tsw):
    """ 任意形状の内部温度を２次元定常熱伝導により求める。
    計算によらず常に一定温度とする格子点（i,j）に対して、tsw(i,j)=1としておき
    かつ、その一定温度をT(i,j)に与えておく。なお、境界にはすべて一定温度を与えること。

    Args:
        xmax (_type_): X軸側の最大長さ[m]
        ymax (_type_): Y軸側の最大長さ[m]
        dl (_type_): 計算格子間隔[m]
        gmax (_type_): 最大許容誤差[-]
        icmax (_type_): 最大計算回数[-]
        tsw (_type_): 温度固定スイッチ（1:固定する, 0:固定しない）

    Returns:
        TI: 内部温度[℃]
        M: X軸側分割数[-]
        N: Y軸側分割数[-]
        IC: 計算終了時の計算回数[-]
    """

    m = int(xmax / dl + 0.5)
    n = int(ymax / dl + 0.5)
    ti = np.zeros((m + 2, n + 2))  # Fortranの101x101はPythonではm+2 x n+2に相当

    ic = 0
    while True:
        ic += 1
        g = 0
        for i in range(1, m + 1):  # Fortranの2からMまでのループはPythonでは1からmまで
            for j in range(1, n + 1):  # 同上
                if tsw[i, j] == 1.0:
                    continue
                to = ti[i, j]
                ti[i, j] = (ti[i, j + 1] + ti[i, j - 1] + ti[i + 1, j] + ti[i - 1, j]) / 4
                g += abs(ti[i, j] - to)

        if g <= gmax or ic >= icmax:
            break

    return ti, m, n, ic


if __name__ == '__main__':
    
    print("テスト未実装")


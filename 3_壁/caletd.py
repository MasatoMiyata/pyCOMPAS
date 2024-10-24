import numpy as np

def caletd(y, it, ta, tr): 
    """ある壁構造の実行温度差用応答係数、壁面全天日射量、外気温より実行温度差ETDを求める

    Args:
        y (numpy.array): 実行温度差用応答係数（i=1～24時）
        it (numpy.array): 壁面全天日射量 [kcal/m2h]（i=1～24時）
        ta (numpy.array): 外気温度 [℃]（i=1～24時）
        tr (numpy.array): 設定室温 [℃]

    Returns:
        etd(numpy.array): 実行温度差ETD[℃]（i=1～24時）
    """

    alpha = 20.0    # 外表面熱伝達率 [kcal/m2h℃]
    a = 0.7         # 日射吸収率 [-]
    
    deltat = np.zeros(24)
    etd = np.zeros(24)
    sat = np.zeros(24)
    ntime = np.zeros(24)
    
    for i in range(24):
        ntime[i] = i + 1
        etd[i] = 0.0
        sat[i] = ta[i] + (a / alpha) * it[i]
        deltat[i] = sat[i] - tr
    
    for n in range(24):
        for j in range(24):
            ii = n - j + 1
            if ii <= 0:
                ii += 24
            etd[n] += y[j] * deltat[ii - 1]
    
    return etd


if __name__ == '__main__':

    y = np.array([0.1] * 24)  # 実行温度差用応答係数
    it = np.array([500] * 24)  # 壁面全天日射量 [kcal/m2h]
    ta = np.array([25] * 24)  # 外気温度 [℃]
    tr = 20.0  # 設定室温 [℃]

    etd = caletd(y, it, ta, tr)
    print(etd)


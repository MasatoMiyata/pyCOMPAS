import numpy as np

def froot(x, y):
    return x * np.tan(x) - y

def moit(sd, rmd, axp, anyu, dt, st):
    """空間の温度がステップ状に変化した場合の壁体等の単位面積あたりの吸放湿量積分値を求める

    Args:
        sd (_type_): 壁体等の材料の厚さ
        rmd (_type_): 壁体等の材料の湿気伝導率[kg/mh(kg/kg')]
        axp (_type_): 壁体等の材料の湿度変化に対する含湿率変化量[kg/m3(kg/kg')]
        anyu (_type_): 壁体等の材料の温度変化に対する含湿率変化量[kg/m3K]
        dt (_type_): 温度変化幅[℃]
        st (_type_): 積分時間[h]

    Returns:
        w (_type_): 壁体等の材料の表面湿流の積分値[kg/m2]
    """

    sl1 = sd / 2
    alfad = 38
    hd = alfad / rmd
    sma = rmd / axp
    al = sl1 * hd
    t = sma * st / sl1**2
    sad = 0
    alfa = np.zeros(21)

    for i in range(21):
        sa = sad
        sb = sa + np.pi
        while abs(sa - sb) > 0.0001:
            sc = (sa + sb) / 2
            if froot(sa, al) * froot(sc, al) > 0:
                sa = sc
            else:
                sb = sc
        alfa[i] = sa
        sad += np.pi

    sum_ = 0
    for i in range(21):
        if alfa[i]**2 * t > 60:
            sum1 = 0
        else:
            sum1 = 2 * al**2 / (alfa[i]**2 * (al * (al + 1) + alfa[i]**2)) * np.exp(-alfa[i]**2 * t)
        sum_ += sum1

    flt = 1 - sum_
    w = sl1 * dt * anyu * flt

    return w

if __name__ == '__main__':

    print("テスト未実装")

import numpy as np

def midzon(to, ti, vel, k, rk, dw, dhl, dhu, wk):
    """複数の開口をもつ単室の中性帯高さと出入り流量を求める。

    Args:
        qos (float):        コンクリート壁体外側の仕上げ材等の熱容量 [kcal/m2℃]
        to (float):         外気温度 [℃]
        ti (float):         室内温度 [℃]
        vel (float):        外部風速 [m/sec]
        k (int):            開口の数 [-]
        rk (NDArray[k]):    流速係数 [-]
        dw (NDArray[k]):    開口の幅 [m]
        dhl (NDArray[k]):   開口の下端高さ [m]
        dhu (NDArray[k]):   開口の上端高さ [m]
        wk  (NDArray[k]):   風圧係数 [-]    

    Returns:
        gi (NDArray[k]):   流入量 [kg/sec]
        go (NDArray[k]):   流出量 [kg/sec]
        dy (NDArray[k]):   中性帯高さ [m]
    """
    grv = 9.8  # 重力加速度 (m/sec^2)

    gi = np.zeros(k)
    go = np.zeros(k)
    dy = np.zeros(k)

    ro = 353.2 / (273.0 + to)
    ri = 353.2 / (273.0 + ti)
    dr = ro - ri
    ddy = (wk * ro * vel**2) / (19.6 * dr)

    dhl1 = dhl - ddy
    dhu1 = dhu - ddy

    y1 = np.min(dhl1)
    y2 = np.max(dhu1)

    for _ in range(100):
        yy = (y1 + y2) * 0.5
        tgi = 0.0
        tgo = 0.0

        for i in range(k):
            dy[i] = yy + ddy[i]

            if dhl[i] >= dy[i]:
                gi[i] = 0.0
                go[i] = fluxo(rk[i], dw[i], dhu[i], yy, ddy[i], ri, dr)
            elif dhu[i] <= dy[i]:
                gi[i] = fluxi(rk[i], dw[i], yy, ddy[i], dhl[i], ro, dr)
                go[i] = 0.0
            else:
                gi[i] = fluxi(rk[i], dw[i], yy, ddy[i], dhl[i], ro, dr)
                go[i] = fluxo(rk[i], dw[i], dhu[i], yy, ddy[i], ri, dr)

            tgi += gi[i]
            tgo += go[i]

        if np.abs(tgi - tgo) < (tgi + tgo) * 0.005:
            return dy, gi, go

        if tgi > tgo:
            y2 = yy
        else:
            y1 = yy

    return dy, gi, go

def fluxi(x1, x2, x3, x4, x5, x6, x7):
    return 2.0/3.0 * x1 * x2 * ((x3 + x4 - x5)**1.5) * np.sqrt(2.0 * 9.8 * x6 * x7)

def fluxo(x1, x2, x3, x4, x5, x6, x7):
    return 2.0/3.0 * x1 * x2 * ((x3 - (x4 + x5))**1.5) * np.sqrt(2.0 * 9.8 * x6 * x7)

def main():
    # データの読み込み
    with open('MIDZON_MAIN.DAT', 'r') as file:
        data = file.readlines()

    # 各行のデータ部分を抽出
    to, ti, vel, k = map(float, data[0][:35].split())
    k = int(k)  # 開口の数は整数で扱う

    rk = np.zeros(k)
    dw = np.zeros(k)
    dhl = np.zeros(k)
    dhu = np.zeros(k)
    wk = np.zeros(k)

    for i in range(k):
        rk[i], dw[i], dhl[i], dhu[i], wk[i] = map(float, data[i + 1][:45].split())

    # 計算の実行
    dy, gi, go = midzon(to, ti, vel, k, rk, dw, dhl, dhu, wk)

    # 結果の表示
    print("output")
    print("    i      dy(i)      gi(i)      go(i)")
    for i in range(k):
        print(f"{i + 1:5d} {dy[i]:10.3f} {gi[i]:10.3f} {go[i]:10.3f}")

if __name__ == "__main__":
    main()
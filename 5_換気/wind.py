def wind(v, iwd, h, hb, e, ti, to, a, al):
    """窓からのすきま風量をクラック法により計算する
    Args:
        v: 風速（気象台観測値：測定高さ 15 m）[m/sec]
        iwd: 風向 (報告書 p.319 図１参照；16方位)
        h: 窓面の地上高さ [m]
        hb: 建物軒高 [m]
        e: 窓面の方位角 [度]
        ti: 室温 [℃]
        to: 外気温 [℃]
        a: サッシのすきま定数
        al: すきま長さ [m]

    Returns:
        q: すきま風量 [m^3/h]
    """
    ho = 15.0
    an = 1.5

    gi = 353.0 / (273.0 + ti)
    go = 353.0 / (273.0 + to)

    if h <= ho:
        vh = v
    else:
        vh = v * (h / ho) ** 0.25

    w = 22.5 * iwd - 180.0
    gw = abs(w - e) % 360.0

    if gw > 180.0:
        gw = 360.0 - gw

    if gw <= 30.0:
        c = 0.75
    elif 30.0 < gw <= 75.0:
        c = 1.25 - gw / 60.0
    elif 75.0 < gw <= 90.0:
        c = 2.0 - gw / 37.5
    elif gw > 90.0:
        c = -0.4

    dp = c * go * vh * vh * 0.5 / 9.8 + (gi - go) * (h - 0.5 * hb)

    if dp <= 0.0:
        q = 0
    else:
        q = a * al * dp ** (1.0 / an)

    return q

def read_data(file_path):
    with open(file_path, 'r') as file:
        while True:
            lines = file.readlines()
            #v = list(map(float, lines[0].split()))
            #iwd = list(map(float, lines[1].split()))
            to = list(map(float, lines[0].split()))
            iwd = list(map(float, lines[1].split()))
            v = list(map(float, lines[2].split()))
            m,n = list(map(int, lines[3].split()))
            # Check the condition to exit the loop
            if m == 1 and n == 1:
                break
    return to, iwd, v, m, n

if __name__ == "__main__":
    # p.319 wind
    # 使用例
    to = [0.0] * 24
    v = [0.0] * 24
    iwd = [0] * 24
    a = 2.0
    al = 87.0
    h = 5.0
    hb = 20.0
    e = 180.0
    ti = 22.0

    filename = 'wind_py.dat'
    to, iwd, v, m, n = read_data(filename)

    print(f"to (temp+50): {to}")
    print(f"iwd: {iwd}")
    print(f"v: {v}")
    print(f"m: {m}, n: {n}")

    for j in range(24):
        to[j] -= 50.0
        q = wind(v[j], iwd[j], h, hb, e, ti, to[j], a, al)
        print('j={}, iwd={}, v={}, to={}, q={}'.format(j, iwd[j], v[j], to[j], q))

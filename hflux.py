def hbalnc(t1, t2, t3, ifl1, ifl2, q, rm, cn, a, dx, w):

    jf1 = ifl1
    jf2 = abs(ifl2)

    while True:
        if jf1 > 0:

            r1 = rm[jf1 - 1]

            if jf2 in [1, 2, 3]:
                r2 = rm[jf2 - 1]
                a1 = a[jf1 - 1]
                q += 2.0 * a1 / dx / dx * (r2 / (r1 + r2) * (t2 - t1))
                return q, t3

            elif jf2 in [4, 5, 6]:
                al = cn[jf2 - 4]
                t = cn[jf2 - 1]
                a1 = a[jf1 - 1]
                q += a1 * al / dx / (r1 + 0.5 * al * dx) * (t - t1)
                t3 = (r1 * t1 + 0.5 * al * dx * t) / (r1 + 0.5 * al * dx)
                return q, t3

            elif jf2 in [7, 8, 9]:
                t = cn[jf2 - 1]
                a1 = a[jf1 - 1]
                q += 2.0 * a1 / dx / dx * (t - t1)
                t3 = t
                return q, t3

            elif jf2 == 10:
                t3 = t1
                return q, t3

        elif -3 <= ifl2 <= -1:
            jf1 = abs(ifl1)
            r1 = rm[jf1 - 1]
            r2 = rm[jf2 - 1]
            a1 = a[jf1 - 1]
            q += 2.0 * a1 / dx / dx * (r2 / (r1 + r2) * (t2 - t1) +
                                       0.5 * dx / (r1 + r2) * w)
            return q, t3

        else:
            jf1 = abs(ifl1)


def hflux(t, ix, iy, rm, cn, a, ifl, dx, dy, dt, td, wx, wy, hbalnc):
    """壁体の断面形状（二次元）と境界条件等を与えて、壁体内部及び表面の温度を求める。
    （非定常計算）

    Args:
        t (_type_): _description_
        ix (_type_): _description_
        iy (_type_): _description_
        rm (_type_): _description_
        cn (_type_): _description_
        a (_type_): _description_
        ifl (_type_): _description_
        dx (_type_): _description_
        dy (_type_): _description_
        dt (_type_): _description_
        td (_type_): _description_
        wx (_type_): _description_
        wy (_type_): _description_
        hbalnc (_type_): _description_
    """

    for i in range(ix):
        for j in range(iy):
            ifl1 = ifl[i, j]
            if ifl1 == 0 or ifl1 < -3:
                continue

            q = 0.0
            t1 = td[i, j]

            # 各方向についてhbalncを呼び出し
            ifl2 = ifl[i, j - 1]
            q, _ = hbalnc(t1, td[i, j - 1], t[i, j - 1], ifl1, ifl2, q, rm, cn, a, dy, wx)

            ifl2 = ifl[i + 1, j]
            q, _ = hbalnc(t1, td[i + 1, j], t[i + 1, j], ifl1, ifl2, q, rm, cn, a, dx, wy)

            ifl2 = ifl[i, j + 1]
            q, _ = hbalnc(t1, td[i, j + 1], t[i, j + 1], ifl1, ifl2, q, rm, cn, a, dy, wx)

            ifl2 = ifl[i - 1, j]
            q, _ = hbalnc(t1, td[i - 1, j], t[i - 1, j], ifl1, ifl2, q, rm, cn, a, dx, wy)

            t[i, j] = q * dt + t1

    # 更新されたTをTDにコピー
    for i in range(ix):
        for j in range(iy):
            td[i, j] = t[i, j]



if __name__ == '__main__':
    
    print("テスト未実装")

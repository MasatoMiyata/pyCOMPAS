import numpy as np

def ventqi(po, to, dho, pi, ti, dhi, s):
    def hjyu(x1, x2):
        return 353.2 / (273.16 + x1) * x2

    def rryo(x1, x2, x3, x4):
        return 3600.0 * x1 * np.sqrt(2.0 * 9.8 * (273.16 + x2) / 353.2 * (x3 - x4))

    xx = pi - hjyu(ti, dhi)
    yy = po - hjyu(to, dho)

    if xx > yy:
        g = -1.0 * rryo(s, ti, xx, yy)
    else:
        g = rryo(s, to, yy, xx)

    return g

def ventqr(mcnt, sper, kst, ked, po, to, dho, s, ti, dhi, g):
    x1 = -1000.0
    x2 = 1000.0

    for _ in range(mcnt):
        gall = 0.0
        gout = 0.0

        for i in range(kst - 1, ked):
            x = (x1 + x2) * 0.5
            g[i] = ventqi(po[i], to[i], dho[i], x, ti, dhi[i], s[i])

            if g[i] < 0.0:
                gout -= g[i]
            gall += g[i]

        if gout > 0.0:
            gosa = abs(gall / gout)
            if gosa <= sper:
                break

        if gall > 0.0:
            x1 = x
        else:
            x2 = x

        if x1 == x2:
            break

    pi = x
    return pi

def ventt(kst, ked, g, to, kwsu, wka, tw, qi):
    gtin = 0.0
    gin = 0.0

    for i in range(kst - 1, ked):
        if g[i] > 0.0:
            gtin += g[i] * to[i]
            gin += g[i]

    tka = 0.0
    tkat = 0.0

    if kwsu > 0:
        for i in range(kwsu):
            tka += wka[i]
            tkat += wka[i] * tw[i]

    if gin != 0.0:
        ti = (0.288 * gtin + qi + tkat) / (0.288 * gin + tka)
    else:
        ti = 0.0

    return ti

def vent(mcnt, sper, krsu, kst, ked, kwsu, wka, tw, qi, ksw, ktsu, nr, nkno, po, dh1, dh2, to, s, ti):
    """複数の室が外部開口および内部開口により繋がっている場合、各開口部の出入り流量・室の圧力・温度を算出する。

    Args:
        mcnt (int):                 最大反復回数 [回]
        sper (float):               収束条件 [%]
        krsu (int):                 総室数 [-]
        ktsu (int):                 総開口部数 [-]
        kst,ked (NDArray[krsu]):    開口部の開始・終了番号 [-]
        kwsu (NDArray[krsu]):       貫流熱を考慮する壁体の数 [-]
        wka (NDArray[ktsu][krsu]):  貫流率ｘ面積 [kcal/h℃]
        tw (NDArray[ktsu][krsu]):   壁体面の外気温度 [℃]
        qi (NDArray[krsu]):         発生熱量 [kcal/h]
        ti (NDArray[krsu]):         室内温度（初期値） [℃]
        ksw (NDArray[krsu]):        室内温度固定スイッチ（固定するとき1を入力）
        nr (NDArray[ktsu]):         隣室の番号 [-]
        nkno (NDArray[ktsu]):       隣室からみた開口番号 [-]
        po (NDArray[ktsu]):         外部圧力（外部開口の場合のみ [mmAg]
        dh1 (NDArray[ktsu]):        床面から開口部中心までの高さ [m]
        dh2 (NDArray[ktsu]):        隣室からみた中心までの高さ（入力不要）
        to (NDArray[ktsu]):         外気温度（外部開口の場合のみ） [℃]
        s (NDArray[ktsu]):          有効開口面積 [m^2]

    Returns:
        ti (NDArray[krsu]):         室内温度（固定の場合は初期値） [℃]
        pi (NDArray[krsu]):         室内の壁面における圧力 [mmAg]
        g (NDArray[ktsu]):          各開口部の出入流量（+は流入, -は流出） [m^3/h]
    
    制約：
        ventqr, ventqi, venttの関数を使用しているので、各々の制約・欠点が適用される。
        室数が多かったり、収束条件が厳しいと、収束条件が3回「入れ子」になっているので、計算時間がかなりかかる。
    """
    pi = np.zeros(krsu)
    g = np.zeros(ktsu)

    wka1 = np.zeros(10)
    tw1 = np.zeros(10)

    for i in range(ktsu):
        if nr[i] == 0:
            dh2[i] = 0.0
        else:
            for j in range(krsu):
                #if (nr[i]) != j:
                if (nr[i]) != j+1:
                    continue
                to[i] = ti[j]
                po[i] = 0.0
            dh2[i] = dh1[nkno[i]-1]

    sper *= 0.01

    for iii in range(mcnt):
        for ii in range(mcnt):
            for i in range(krsu):
                pi[i] = ventqr(mcnt, sper, kst[i], ked[i], po, to, dh2, s, ti[i], dh1, g)
                for j in range(ktsu):
                    #if i != nr[j]:
                    if i != nr[j]-1:
                        continue
                    po[j] = pi[i]

                for j in range(kst[i] - 1, ked[i]):
                    if nr[j] == 0:
                        continue
                    g[nkno[j]-1] = -1.0 * g[j]

            gosa = 0.0
            for i in range(krsu):
                gout = 0.0
                gall = 0.0
                for j in range(kst[i]-1 , ked[i]):
                    if g[j] > 0.0:
                        gall += g[j]
                    else:
                        gout -= g[j]
                        gall += g[j]

                if gout == 0.0:
                    gosa1 = 999.0
                else:
                    gosa1 = abs(gall / gout)

                if gosa1 < gosa:
                    continue
                gosa = gosa1

            if gosa < sper:
                print ('gosa break: iii,ii,gosa=', iii,ii,gosa,sper) 
                break

        gosa = 0.0
        for i in range(krsu):
            tix = ti[i]
            for j in range(kwsu[i]):
                wka1[j] = wka[j][i]
                tw1[j] = tw[j][i]
                print('iii,i,j,wka(i,j),tw(i,j)= ', iii,i,j,wka[j][i],tw[j][i])

            if ksw[i] != 1:
                ti[i] = ventt(kst[i], ked[i], g, to, kwsu[i], wka1, tw1, qi[i])

            print ('iii,i,qi,ti,ksw= ', iii, i, qi[i], ti[i], ksw[i] )

            if ti[i] == 0.0:
                gosa1 = abs(ti[i] - tix)
            else:
                gosa1 = abs((ti[i] - tix) / ti[i])

            if gosa1 < gosa:
                continue
            gosa = gosa1

        if gosa < sper:
            print('収束 回数')
            print(iii, ii)
            return pi, g

        for i in range(krsu):
            for j in range(ktsu):
                #if i != nr[j]:
                if i != nr[j]-1:
                    continue
                to[j] = ti[i]

    return pi, g

def main():
    # 初期条件の設定
    mcnt = 100
    sper = 0.1
    krsu = 3
    ktsu = 9
    kst = [1, 3, 7, 0, 0, 0, 0, 0, 0, 0]
    ked = [2, 6, 9, 0, 0, 0, 0, 0, 0, 0]
    kwsu = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
    wka = [[0.0, 0.0, 50.0, 0.0, 0.0], [0.0] * 5, [0.0] * 5, [0.0] * 5, [0.0] * 5,
           [0.0] * 5, [0.0] * 5, [0.0] * 5, [0.0] * 5, [0.0] * 5]
    tw = [[0.0, 0.0, 30.0, 0.0, 0.0], [0.0] * 5, [0.0] * 5, [0.0] * 5, [0.0] * 5,
          [0.0] * 5, [0.0] * 5, [0.0] * 5, [0.0] * 5, [0.0] * 5]
    qi = [0.0, 1000.0, 5000.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    ksw = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ti = [ 20.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0,  30.0, 30.0]
    nr = [0, 2, 1, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    nkno = [0, 3, 2, 0, 0, 7, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    po = [2.7, 0.0, 0.0, -4.5, -2.4, 0.0, 0.0, 1.6, -1.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    dh1 = [1.8, 1.1, 3.5, 2.5, 1.8, 1.1, 2.1, 1.8, 1.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    dh2 = [0.0] * 20
    to = [30.0, 0.0, 0.0, 30.0, 30.0, 0.0, 0.0, 30.0, 30.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    s = [4.0, 2.0, 2.0, 10.0, 4.0, 5.0, 5.0, 2.0, 10.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    # vent関数を呼び出して計算を実行
    pi, g = vent(mcnt, sper, krsu, kst, ked, kwsu, wka, tw, qi, ksw, ktsu, nr, nkno, po, dh1, dh2, to, s, ti)

    # 結果の出力
    print('室の床面における圧力:', pi)
    print('室内温度:', ti)
    print('各開口部の出入流量:', g)

if __name__ == "__main__":
    main()
from gtrans import gtrans

def spacwf(IC, AW, AC, ALR, AO, AA, ALP, IK, ALPF, IFIXK, W):
    """壁体熱取得に対する負荷の応答
    """

    if IC == 1:
        for I in range(IFIXK + 2):
            W[I] = 0.0

    for I in range(IFIXK):
        W[I] += AW * gtrans(AO, AA, ALP, IK, ALPF[I])

    W[IFIXK] += AW * AO
    W[IFIXK + 1] += AW

    if IC == -1:
        Y1 = AC * W[IFIXK + 1]
        Y2 = ALR / (AC + ALR)
        for I in range(IFIXK + 2):
            W[I] = Y1 / (Y1 + Y2 * W[I])

    return W

if __name__ == '__main__':

    IC = 1
    AW = 1.0  # 仮の値
    AC = 1.0  # 仮の値
    ALR = 1.0  # 仮の値
    AO = 1.0  # 仮の値
    AA = [1.0]  # 仮の値リスト
    ALP = [1.0]  # 仮の値リスト
    IK = 1  # 仮の値
    ALPF = [1.0]  # 仮の値リスト
    IFIXK = 1  # 仮の値
    W = [0.0] * (IFIXK + 2)  # 初期化

    W = spacwf(IC, AW, AC, ALR, AO, AA, ALP, IK, ALPF, IFIXK, W)
    print(W)

import math

def sucft1(IK, AT, AA, ALP, DT):
    """逐次積分熱流法のための係数
    """

    R = [0] * IK
    XT = [0] * IK
    XA = [0] * IK
    TXT = 0.0
    TXA = 0.0

    for I in range(IK):
        R[I] = math.exp(-ALP[I] * DT)
        XT[I] = AT[I] / ALP[I] * (1.0 - R[I])
        XA[I] = AA[I] / ALP[I] * (1.0 - R[I])
        TXT += XT[I]
        TXA += XA[I]

    return R, XT, XA, TXT, TXA


if __name__ == '__main__':

    IK = 3
    AT = [1.0, 2.0, 3.0]
    AA = [0.5, 1.0, 1.5]
    ALP = [0.1, 0.2, 0.3]
    DT = 1.0

    result = sucft1(IK, AT, AA, ALP, DT)
    print(result)

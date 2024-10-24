import math

def sucft2(IK, AO, AT, AA, ALP, EPST, EPSA, DT):
    """逐次積分熱量法のための係数
    """
    R = [0] * IK
    XT = [0] * IK
    XA = [0] * IK
    Y = [0] * IK
    XTO = AO * DT ** 2 * 0.5 + EPST * DT
    XAO = AO * DT ** 2 * 0.5 + EPSA * DT

    for I in range(IK):
        R[I] = math.exp(-ALP[I] * DT)
        Y[I] = (1.0 - R[I]) / ALP[I]
        XT[I] = AT[I] * Y[I]
        XA[I] = AA[I] * Y[I]
        Y1 = (DT - Y[I]) / ALP[I]
        XTO += AT[I] * Y1
        XAO += AA[I] * Y1

    return R, XT, XA, Y, XTO, XAO

if __name__ == '__main__':

    IK = 3
    AO = 1.0
    AT = [1.0, 2.0, 3.0]
    AA = [0.5, 1.0, 1.5]
    ALP = [0.1, 0.2, 0.3]
    EPST = 0.1
    EPSA = 0.2
    DT = 1.0

    result = sucft2(IK, AO, AT, AA, ALP, EPST, EPSA, DT)
    print(result)

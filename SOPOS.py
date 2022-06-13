import math

def DEL(W):
    """
    日赤緯[°]を求める関数（滝沢による）
    """

    y = 0.3622133 \
        - 23.24763  * math.cos( W + 0.153231) \
        - 0.3368908 * math.cos(2.0 * W + 0.2070988) \
        - 0.1852646 * math.cos(3.0 * W + 0.6201293)

    return y

def EQT(W):

    y = -0.0002786409 \
        + 0.1227715   * math.cos( W + 1.498311) \
        - 0.1654575   * math.cos(2.0 * W - 1.261546) \
        - 0.005353830 * math.cos(3.0 * W - 1.157100)

    return y

def D(M,N):

    y = 30*(M-1)+(M+M/8)/2-(M+7)/10+N

    return y

def SOPOS(FN,EL,M,N,HJ):
    
    PAI = 3.141593
    RADI = 0.01745329
    ELS = 135.0

    W = PAI * D(M,N) / 183.0

    T = 15.0 * (HJ - 12.0 + EQT(W)) + EL - ELS
    # T = 15.0 * (HJ - 12.0)

    TJ = T/15.+12
    FN1=FN*RADI
    SF=math.sin(FN1)
    CF=math.cos(FN1)
    DEL1=DEL(W)*RADI

    SD=math.sin(DEL1)
    CD=math.cos(DEL1)

    T1=T*RADI
    CT=math.cos(T1)
    ST=math.sin(T1)

    SH=SF*SD+CF*CD*CT

    if (SH > 0):
        CH=math.sqrt(1.0-SH**2)
        SA=CD*ST/CH
        CA=(SH*SF-SD)/(CH*CF)
    else:
        SH=0.0
        SA=0.0
        CA=0.0

    return SH, SA, CA, TJ


if __name__ == '__main__':

    FN = 35.68
    EL = 139.77
    M = 8
    N = 23

    for hour in range(0,24):

        HJ = hour
        SH, SA, CA, TJ = SOPOS(FN,EL,M,N,HJ)

        print(SH, SA, CA, TJ)









def suc2(IP, IK, AO, R, X, Y, XO, DT, F1, Z1, F, Q):
    """熱量法による逐次積分
    """
        
    # IP=1...SPACE TEMPERATURE KNOWN, THERMAL LOAD UNKNOWN
    # IP=2...THERMAL LOAD KNOWN, SPACE TEMPERATURE UNKNOWN
    # INPUT...IP,IK,AO,R,X,Y,XO,DT,(F1,Z1),F OR Q
    # OUTPUT..(F1,Z1),F OR Q

    TZ1 = 0.0
    for I in range(IK):
        TZ1 += Z1[I] * Y[I]

    if IP == 1:
        DF = (F - F1) / DT
        Q = AO * F1 + (TZ1 + DF * XO) / DT
    elif IP == 2:
        F = F1 + DT * (DT * (Q - AO * F1) - TZ1) / XO
        DF = (F - F1) / DT

    for I in range(IK):
        Z1[I] = Z1[I] * R[I] + DF * X[I]

    F1 = F
    return F1, Z1, F, Q


if __name__ == '__main__':

    IK = 3
    R = [1.0, 2.0, 3.0]
    X = [0.5, 1.0, 1.5]
    Y = [0.3, 0.6, 0.9]
    Z1 = [1.0, 1.0, 1.0]
    F1 = 0
    F = 10
    Q = 0
    XO = 1.0
    DT = 1.0

    result = suc2(1, IK, 1.0, R, X, Y, XO, DT, F1, Z1, F, Q)
    
    print(result)

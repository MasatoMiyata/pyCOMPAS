def suc1(IP, IK, AO, R, X, TX, EPS, DT, F1, Z1, F, Q):
    """熱流法による逐次積分
    """

    # IP=1...SPACE TEMPERATURE KNOWN, THERMAL LOAD UNKNOWN
    # IP=2...THERMAL LOAD KNOWN, SPACE TEMPERATURE UNKNOWN
    # INPUT...IP,IK,AO,R,X,TX,EPS,DT,(F1,Z1),F OR Q
    # OUTPUT..(F1,Z1),F OR Q

    TZ1 = 0.0
    for I in range(IK):
        Z1[I] = Z1[I] * R[I]
        TZ1 += Z1[I]

    if IP == 1:
        DF = (F - F1) / DT
        TZ1 += TX * DF
        Q = AO * F + TZ1 + EPS * DF
    elif IP == 2:
        TXE = TX + EPS
        F = (DT * (Q - TZ1) + F1 * TXE) / (AO * DT + TXE)
        DF = (F - F1) / DT

    for I in range(IK):
        Z1[I] = Z1[I] + X[I] * DF

    F1 = F
    
    return F1, Z1, F, Q


if __name__ == '__main__':

    IK = 10
    R = [1.0] * IK
    X = [1.0] * IK
    Z1 = [1.0] * IK
    F1 = 0
    F = 0
    Q = 0

    result = suc1(1, IK, 1.0, R, X, 1.0, 0.1, 1.0, F1, Z1, F, Q)
    print("テストケース 1 の結果:", result)

    # テストケース 1
    # IP=1, IK=3, AO=1.0, R=[1.0, 2.0, 3.0], X=[0.5, 1.0, 1.5],
    # TX=1.0, EPS=0.1, DT=1.0, F1=0.0, Z1=[1.0, 1.0, 1.0], F=10.0, Q=0.0
    result = suc1(1, 3, 1.0, [1.0, 2.0, 3.0], [0.5, 1.0, 1.5], 1.0, 0.1, 1.0, 0.0, [1.0, 1.0, 1.0], 10.0, 0.0)
    print("テストケース 1 の結果:", result)

    # テストケース 2
    result = suc1(2, 3, 1.5, [2.0, 3.0, 4.0], [1.0, 1.5, 2.0], 1.5, 0.2, 1.0, 5.0, [2.0, 2.0, 2.0], 0.0, 20.0)
    print("テストケース 2 の結果:", result)


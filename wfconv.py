def WFCONV(ISTEP, WF, WFF, C, NK, HSM, FS, G, F1, DF1, HS, F):

    if ISTEP == 0:
        G = [0.0 for _ in range(NK - 2)]
        F1 = 0.0
        DF1 = 0.0
    else:
        Q1 = G[0] + F1 * WF[1]
        for J in range(2, NK - 1):
            if J - 1 < len(G):
                G[J - 1] = G[J - 2] + F1 * WF[1]
        G[NK - 3] = G[NK - 3] * C + F1 * WF[NK - 1]

        if ISTEP in [4, 14]:
            Q1 += DF1 * WFF[1]
            for J in range(2, NK - 1):
                if J - 1 < len(G):
                    G[J - 1] += DF1 * WFF[J]
            G[NK - 3] += DF1 * WFF[NK - 1]

    if ISTEP < 11:
        if ISTEP in [1, 4]:
            F = (HS - Q1) / WF[0]
        elif ISTEP == 2:
            F = -Q1 / WF[0]
            DF1 = HS / WFF[0]
            if F + DF1 > FS:
                DF1 = FS - F
                DF1 = max(DF1, 0.0)
                HS = DF1 * WFF[0]
        elif ISTEP == 3:
            F = (HS - Q1) / WF[0]
            DF1 = -HS / WFF[0]
    else:
        if ISTEP in [11, 14]:
            HS = Q1 + F * WF[0]
        elif ISTEP == 12:
            HS = Q1 + F * WF[0]
            DF1 = FS - F
            DHS = DF1 * WFF[0]
            if HS + DHS > HSM:
                DHS = HSM - HS
                DHS = max(DHS, 0.0)
                DF1 = DHS / WFF[0]
        elif ISTEP == 13:
            HS = Q1 + F * WF[0]
            DF1 = -HS / WFF[0]

    F1 = F
    return G, F1, DF1, HS, F

if __name__ == '__main__':

    ISTEP = 0
    WF = [0.5, 1.0, 1.5, 2.0, 2.5]
    WFF = [0.6, 1.1, 1.6, 2.1, 2.6]
    C = 1.2
    NK = 5
    HSM = 10.0
    FS = 5.0
    G = [0] * (NK - 2)
    F1 = 0.0
    DF1 = 0.0
    HS = 8.0
    F = 0.0

    result = WFCONV(ISTEP, WF, WFF, C, NK, HSM, FS, G, F1, DF1, HS, F)
    print(result)
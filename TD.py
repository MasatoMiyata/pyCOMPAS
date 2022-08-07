import math

from PS import PS

def TD(X):
    # X 絶対湿度[kg/kg]

    X = math.exp(X)

    # [kg/kg]から[atm]に変換
    X = X / (0.622 + X)

    T = 1200 * X - 5

    print(T)

    PST = PS(T)
    DEL = PST - X

    J = 0
    flag = True
    while (flag and J<20):
            
        if (T <= 0):
            PSDT = (8.233478*10**(-2) + T*(-6.138824*10**(-4) + T*(2.891727*10**(-6) - 2.570456*10**(-8)*T))) * PST
        else:
            PSDT = (7.265429*10**(-2) + T*(-5.972668*10**(-4) + T*(3.340251*10**(-6) + T*(-1.371924*10**(-8) + 3.090725*10**(-11)*T) ))) * PST

        DELT = DEL / PSDT

        print(DELT)
        if abs(DELT) > 0.01:
            J += 1
            T = T - DELT
            PST = PS(T)
            DEL = PST - X
        else:
            flag = False

        print(J)

    return T



if __name__ == '__main__':

    # 結果がおかしい。再確認
    print(TD(0.010))
    

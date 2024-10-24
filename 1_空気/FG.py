from PS import PS

def FG(H:float, X:float) -> float:
    """
    エンタルピーと絶対湿度から湿球温度を算出する関数

    Args:
        H (float): エンタルピー[kcal/kg]
        X (float): 絶対湿度[kg/kg]

    Returns:
        float: 湿球温度[℃]
    """

    # 松尾の近似式
    TS = ( -5.638340 + H*(2.677933 + H*(-6.721679*10**(-2) + 7.856989*10**(-4)*H )) ) \
        / ( 1.0 + (2.860526 + H*(-1.82433*10**(-1) + H*(5.77939*10**(-3) - 7.1060*10**(-5)*H))) * X )

    # 精度を高めるための収束計算
    J = 0
    flag = True
    while (flag and J<10):

        P1 = PS(TS)
        XS = 0.622 * P1 / (1 - P1)
        TSN = (H - 597.3*XS) / (0.240 - 0.559*XS + X)

        if abs(TSN-TS) > 0.001:
            J += 1
            TS = TS * 0.6 + TSN * 0.4
        else:
            flag = False

    return TS

if __name__ == '__main__':

    # ケース① H=52.335 kJ/kg, X=10.5g/kg のとき、 Twb=18.6
    # https://www.techno-ryowa.co.jp/rrlab/

    H_kJ = 52.335
    H_cal = H_kJ / 4.1868
    Twb = FG(H_cal, 0.0105)
    print(Twb)

    # ケース② H=20.0kJ/kg, X=2.0g/kg のとき、 Twb=5.9
    # https://www.techno-ryowa.co.jp/rrlab/

    H_kJ = 20
    H_cal = H_kJ / 4.1868
    Twb = FG(H_cal, 0.002)
    print(Twb)
from typing import Tuple
import math
from PS import PS
from FG import FG

def calc_AH(P):
    # 水蒸気圧 mmHg から 絶対湿度 kg/kg を算出する。
    AH = 0.622 * P / (760 - P)
    return AH

def calc_A(P):
    # 水蒸気圧 atm から 絶対湿度 kg/kg を算出する。
    A = 0.622 * P / (1 - P)
    return A

def calc_CH(X):
    # 絶対湿度 kg/kg から 水蒸気圧 mmHg を算出する。
    CH = 760 * X / (0.622 + X)
    return CH

def calc_C(X):
    # 絶対湿度 kg/kg から 水蒸気圧 atm を算出する。
    C = X / (0.622 + X)
    return C

def calc_B(XS, DB, WB):
    # 温度WBのときの飽和絶対湿度[kg/kg]、乾球温度、湿球温度から絶対湿度[kg/kg]を算出する。
    B = ( (597.3 - 0.559*WB)*XS - 0.240*(DB-WB) ) / (597.3 + 0.441*DB - WB)
    return B

def calc_TD(x):
    # 絶対湿度[kg/kg]から露点温度を算出する。
    X = math.log(x)
    TD = 90.93743 + X*(16.98006 + X*(-0.7905916 + X*(-0.2411693-0.01389958*X))) + 0.8045291*abs(X+5.580150)
    return TD

def calc_HF(T,X):
    # 乾球温度[℃]と絶対湿度[kg/kg]からエンタルピー[kcal/kg]を算出する。
    HF = 0.240*T + (597.3+0.441*T)*X
    return HF

def calc_XF(H,T):
    # 乾球温度[℃]とエンタルピー[kcal/kg]から絶対湿度[kg/kg]を算出する。
    XF = (H-0.240*T) / (597.3+0.441*T)
    return XF

def PSY(Tdb:float, Twb:float=None, Tdew:float=None, R:float=None, X:float=None, P:float=None, H:float=None) -> Tuple[float,float,float,float,float,float,float]:
    """
    乾球温度と「湿球温度、露点温度、相対湿度、絶対湿度、水蒸気分圧、エンタルピー」のいずれかから
    乾球温度、湿球温度、露点温度、相対湿度、絶対湿度、水蒸気分圧、エンタルピーを算出する関数

    Args:
        Tdb (float): 乾球温度[℃]
        Twb (float, optional): 湿球温度[℃]. Defaults to None.
        Tdew (float, optional): 露点温度[℃]. Defaults to None.
        R (float, optional): 相対湿度[%]. Defaults to None.
        X (float, optional): 絶対湿度[kg/kg]. Defaults to None.
        P (float, optional): 水蒸気分圧[mmHg]. Defaults to None.
        H (float, optional): エンタルピー[kcal/kJ]. Defaults to None.

    Returns:
        Tuple[float,float,float,float,float,float,float]: 乾球温度、湿球温度、露点温度、相対湿度、絶対湿度、水蒸気分圧、エンタルピー
    """

    if Tdb is not None:

        if Twb is not None: # 湿球温度が入力された場合

            P1 = PS(Twb) # 湿球温度のときの飽和水蒸気圧[atm]
            X0 = calc_A(P1) # 湿球温度のときの飽和絶対湿度[kg/kg]
            X  = calc_B(X0,Tdb,Twb)  # 絶対湿度[kg/kg]
            Tdew = calc_TD(X)  # 露点温度[℃]
            R  = calc_C(X) / PS(Tdb) * 100  # 相対湿度[%]
            P  = calc_CH(X) # 水蒸気分圧[mmHg]
            H  = calc_HF(Tdb, X)   # エンタルピー[kcal/kg]

        elif Tdew is not None: # 露点温度が入力された場合

            P1 = PS(Tdew)   # 露点温度のときの飽和水蒸気分圧[atm]
            P  = P1 * 760   # 水蒸気分圧[mmHg]
            X  = calc_A(P1) # 絶対湿度[kg/kg] 
            H  = calc_HF(Tdb,X)  # エンタルピー[kcal/kg]
            Twb = FG(H,X)   # 湿球温度[℃]
            R  = P1 / PS(Tdb) * 100  # 相対湿度[%]

        elif R is not None: # 相対湿度が入力された場合

            P1 = PS(Tdb) * R / 100  # 水蒸気分圧[atm]
            P  = P1 * 760   # 水蒸気分圧[mmHg]
            X  = calc_A(P1) # 絶対湿度[kg/kg] 
            H  = calc_HF(Tdb,X)  # エンタルピー[kcal/kg]
            Twb = FG(H,X)   # 湿球温度[℃]
            Tdew = calc_TD(X)  # 露点温度[℃]

        elif X is not None: # 絶対湿度が入力された場合

            H  = calc_HF(Tdb,X)  # エンタルピー[kcal/kg]
            Twb = FG(H,X)   # 湿球温度[℃]
            Tdew = calc_TD(X)  # 露点温度[℃]
            P  = calc_CH(X) # 水蒸気分圧[mmHg]
            R  = calc_C(X) / PS(Tdb) * 100  # 相対湿度[%]

        elif P is not None: # 水蒸気分圧[mmHg]が入力された場合

            X = calc_AH(P)  # 絶対湿度[kg/kg]
            H  = calc_HF(Tdb,X)  # エンタルピー[kcal/kg]   
            Twb = FG(H,X)   # 湿球温度[℃]
            Tdew = calc_TD(X)  # 露点温度[℃]
            R  = P / (PS(Tdb)*760) * 100  # 相対湿度[%]

        elif H is not None: # エンタルピーが入力された場合

            X  = calc_XF(H,Tdb)  # 絶対湿度[kg/kg]
            Twb = FG(H,X)  # 湿球温度[℃]
            Tdew = calc_TD(X)  # 露点温度[℃]
            R  = calc_C(X) / PS(Tdb) * 100  # 相対湿度[%]
            P  = calc_CH(X) # 水蒸気分圧[mmHg]

        else:
            raise Exception("湿球温度、露点温度、相対湿度、絶対湿度、水蒸気分圧、エンタルピーのいずれかの入力が必要です。")
    else:
            raise Exception("乾球温度 Tdb の入力が必要です。")       

    return Tdb, Twb, Tdew, R, X, P, H


if __name__ == '__main__':

    # https://www.techno-ryowa.co.jp/rrlab/
    # https://atmos.miyakyo-u.ac.jp/water/water_vapor.html
    # 1 atm = 1013.25 hPa = 101325 Pa
    # 1 mmhg ＝ 133.3 Pa = 1.333 hPa
    # 1 J = 4.1868 cal
    
    # テスト①
    # Tdb=26, Twb=18.8, Tdew=14.8, R=50, X=0.0105, P=16.818hPa=12.645mmHg, H=52.9kJ/kg=12.635kcal/kg

    (Tdb, Twb, Tdew, R, X, P, H) = PSY(26,18.8)
    (Tdb, Twb, Tdew, R, X, P, H) = PSY(26,Twb=18.8)
    print(Tdb, Twb, Tdew, R, X, P, H)
    (Tdb, Twb, Tdew, R, X, P, H) = PSY(26,None,14.8)
    print(Tdb, Twb, Tdew, R, X, P, H)
    (Tdb, Twb, Tdew, R, X, P, H) = PSY(26,None,None,50)
    print(Tdb, Twb, Tdew, R, X, P, H)
    (Tdb, Twb, Tdew, R, X, P, H) = PSY(26,None,None,None,0.0105)
    print(Tdb, Twb, Tdew, R, X, P, H)
    (Tdb, Twb, Tdew, R, X, P, H) = PSY(26,None,None,None,None,12.645)
    print(Tdb, Twb, Tdew, R, X, P, H)
    (Tdb, Twb, Tdew, R, X, P, H) = PSY(26,None,None,None,None,None,12.635)
    print(Tdb, Twb, Tdew, R, X, P, H)

    # テスト②
    # Tdb=7, Twb=6, Tdew=4.9, R=86.7, X=0.0054, P=8.684hPa=6.5146mmHg, H=20.6kJ/kg=4.92kcal/kg

    (Tdb, Twb, Tdew, R, X, P, H) = PSY(7,6)
    print(Tdb, Twb, Tdew, R, X, P, H)
    (Tdb, Twb, Tdew, R, X, P, H) = PSY(7,None,4.9)
    print(Tdb, Twb, Tdew, R, X, P, H)
    (Tdb, Twb, Tdew, R, X, P, H) = PSY(7,None,None,86.7)
    print(Tdb, Twb, Tdew, R, X, P, H)
    (Tdb, Twb, Tdew, R, X, P, H) = PSY(7,None,None,None,0.0054)
    print(Tdb, Twb, Tdew, R, X, P, H)
    (Tdb, Twb, Tdew, R, X, P, H) = PSY(7,None,None,None,None,6.5146)
    print(Tdb, Twb, Tdew, R, X, P, H)
    (Tdb, Twb, Tdew, R, X, P, H) = PSY(7,None,None,None,None,None,4.92)
    print(Tdb, Twb, Tdew, R, X, P, H)
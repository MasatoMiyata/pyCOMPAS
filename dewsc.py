import numpy as np

def dewsc(xr, tg):
    """壁体内表面で結露が起こっているか否かを調べる
    結露がなければ、xg=xr, 結露があれば xg<xr となって出力される。

    Args:
        xr (_type_): 室内絶対湿度 [g/kg]
        tg (_type_): 壁の表面温度 [℃]

    Returns:
        xg (_type_): 壁表面絶対湿度[g/kg]
    """

    def td(x):
        return 4030.18 / (16.654 - np.log(x)) - 235

    def xp(x, po):
        return po * x / (622 + x)

    def px(x, po):
        return 622 * x / (po - x)

    def ps(x):
        return np.exp(16.654 - 4030.18 / (x + 235))

    
    po = 101.325

    pp = xp(xr, po)
    tdd = td(pp)
    if tg > tdd:
        xg = xr
    else:
        pps = ps(tg)
        xg = px(pps, po)

    return xg


if __name__ == '__main__':
    
    print("テスト未実装")

import numpy as np

def crmat(ik, ao, at, aa, alp, dt):
    """非定常伝熱・項別公比法による係数
    応答係数法の変形として、松尾による項別公比利用法があるが、それに必要な係数を求める

    Args:
        ik (_type_): 単位応答の根の数＜RESSTPの出力＞
        ao (_type_): 熱コンダクタンス[kcal/m2hK]＜RESSTPの出力＞
        at (_type_): AT(1)～AT(IK)＜RESSTPの出力＞
        aa (_type_): AA(1)～AA(IK)＜RESSTPの出力＞
        alp (_type_): ALP(1)～ALP(IK)＜RESSTPの出力＞
        dt (_type_): 時間巾

    Returns:
        rft (_type_): 三角パルス励振大魚等係数の第１項目（貫流）
        rfa (_type_): 三角パルス励振大魚等係数の第１項目（吸熱）
        r (_type_): R(1)～R(IK) 項別公比
        yt (_type_): YT(1)～YT(IK) 貫流係数
        ya (_type_): YA(1)～YA(IK) 吸熱係数
    """    
    
    r  = np.zeros(ik)
    yt = np.zeros(ik)
    ya = np.zeros(ik)
    
    r1 = 0.0
    r2 = 0.0
    
    for i in range(ik):
        r[i] = np.exp(-alp[i] * dt)
        e1 = (1.0 - r[i]) / alp[i]
        r1 += e1 * at[i]
        r1 += e1 * at[i]
        r2 += e1 * aa[i]
        e1 = -(1.0 - r[0]) ** 2 / (alp[i] * dt)
        yt[i] = at[i] * e1
        ya[i] = aa[i] * e1
    
    rft = ao + r1 / dt
    rfa = ao + r2 / dt
    
    return rft, rfa, yt, ya


if __name__ == '__main__':
    
    print("テスト未実装")


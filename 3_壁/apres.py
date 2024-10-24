import numpy as np
import math
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['font.family'] = 'Noto Sans JP'
plt.rcParams['grid.linestyle']='--'
plt.rcParams['grid.linewidth'] = 0.5


def apres(qos, qs, qis, rod, ros, rs, ris, rid):
    """コンクリート壁体の単位応答近似式を求める。

    Args:
        qos (float): コンクリート壁体外側の仕上げ材等の熱容量 [kcal/m2℃]
        qs (float): コンクリート壁体の熱容量 [kcal/m2℃]
        qis (float): コンクリート壁体内側の仕上げ材等の熱容量 [kcal/m2℃]
        rod (float): 外側表面熱伝達抵抗 [m2h℃/kcal]
        ros (float): コンクリート壁体外側の仕上げ材等の熱抵抗 [m2h℃/kcal]
        rs (float): コンクリート壁体の熱抵抗 [m2h℃/kcal]
        ris (float): コンクリート壁体内側の仕上げ材等の熱抵抗 [m2h℃/kcal]
        rid (float): 内側表面熱伝達抵抗 [m2h℃/kcal]

    Returns:
        ck (float): 熱貫流率 [kcal/m2h℃]
        a (NDArray[2]): 式の係数
        b (NDArray[3]): 式の係数
        al (NDArray[3]): 式の係数

    制約：
        壁体の中央部分にコンクリートの層があり、その両側または片側に仕上げ材がある場合に適用可能。
    """
    
    a  = np.zeros(2)
    b  = np.zeros(3)
    al = np.zeros(3)
    
    cpgc = 481.0
    clam = 1.4
    rcod = qos / (cpgc * clam)
    rcid = qis / (cpgc * clam)

    # 熱貫流率
    ck = 1. / (rod + ros + rs + ris + rid)

    ri = ris + rid - rcid
    r = rcod + rs + rcid
    ro = 1. / ck - r - ri
    q = qos + qs + qis
    
    # 貫流応答の係数
    r11 = (ri + ro) * 0.5 + r / 6. + ri * ro / r
    r22 = (ri + ro) / 24. + r / 120. + ri * ro / (6. * r)
    al[0] = r11 / (q * r * (ck * r11 * r11 - r22))
    al[1] = r11 / (q * r * r22)
    a[0] = ck * al[1] / (al[0] - al[1])
    a[1] = -ck * al[0] / (al[0] - al[1])
    
    # 吸熱応答の係数
    r33 = ro / r + r * ck / 2. - ri * ro * ck / r
    r44 = r / 30. + ro * (r + ro) / (6. * r)
    b[0] = ((q * r * al[0] * ck) ** 2) * (r11 * r33 - r44)
    b[1] = q * r * al[1] * ck * ck * (r / 3. + ro * (r + ro) / r - al[0] * q * r * (r11 * r33 - r44))
    b[2] = 1. / ri - (ck + b[0] + 2)
    al[2] = 10
    
    return ck, a, b, al


if __name__ == '__main__':
    
    # Case-1
    # qos = 0              # 熱容量 [kcal/m2℃] 外側部材は無
    # qs  = 462.0 * 0.150  # 熱容量 [kcal/m2℃] コンクリート150mm
    # qis = 246.0 * 0.012  # 熱容量 [kcal/m2℃] せっこうボード12mm、断熱材の熱容量は無視

    # rod = 1/20           # 外側表面熱伝達抵抗 [m2h℃/kcal]
    # ros = 0              # 熱抵抗 [m2h℃/kcal] 外側部材は無
    # rs  = 0.15/1.2       # 熱抵抗 [m2h℃/kcal] コンクリート150mm
    # ris = 0.05/0.032 + 0.012/0.15   # 熱抵抗 [m2h℃/kcal] 断熱材 50mm、せっこうボード 12mm
    # rid = 1/8            # 内側表面熱伝達抵抗 [m2h℃/kcal]

    # Case-2
    qos = 7.6+4.8    # 熱容量 [kcal/m2℃]
    qs  = 67.5       # 熱容量 [kcal/m2℃]
    qis = 3.4        # 熱容量 [kcal/m2℃]

    rod = 1/20           # 外側表面熱伝達抵抗 [m2h℃/kcal]
    ros = 0.015+0.009    # 熱抵抗 [m2h℃/kcal] 
    rs  = 0.115          # 熱抵抗 [m2h℃/kcal] 
    ris = 0.133+0.100    # 熱抵抗 [m2h℃/kcal] 
    rid = 1/8            # 内側表面熱伝達抵抗 [m2h℃/kcal]


    ck, a, b, al = apres(qos, qs, qis, rod, ros, rs, ris, rid)

    print(f"熱貫流率: {ck} kcal/m2h℃")
    print(f"係数a: {a}")
    print(f"係数b: {b}")
    print(f"係数al: {al}")

    time = range(0,100,1)
    phi_t = np.zeros(100)
    phi_a = np.zeros(100)
    
    for t in time:
        phi_t[t] = ck + a[0] * math.exp(-1*al[0]*t) + a[1] * math.exp(-1*al[1]*t)
        phi_a[t] = ck + b[0] * math.exp(-1*al[0]*t) + b[1] * math.exp(-1*al[1]*t) + b[2] * math.exp(-1*al[2]*t)

    plt.figure(figsize=(10,5))
    plt.plot(phi_t, 'b', label="貫流応答")
    plt.plot(phi_a, 'r', label="吸熱応答")
    plt.xlabel("時刻 [h]")
    plt.ylabel("熱流")
    plt.legend()
    plt.grid()
    plt.show()
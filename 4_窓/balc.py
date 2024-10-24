import numpy as np

# ガラス窓が庇等によって遮られた場合の日照面積率を求める

def balc(
        sh: float,
        sa: float,
        gh: float,
        ge: float,
        x1: float,
        x2: float,
        x3: float,
        x4: float,
        x5: float,
        y0: float,
        y1: float,
        y2: float,
        y3: float,
        y4: float,
        y5
        ) -> float:
    """_summary_

    Args:
        sh (float): 太陽高度[rad]
        sa (float): 太陽方位角[rad]
        gh (float): ガラス面の傾斜角[rad]
        ge (float): ガラス面の方位角[rad]
        x1 (float): 庇の平面方向の寸法[任意]
        x2 (float): 庇の平面方向の寸法[任意]
        x3 (float): 庇の平面方向の寸法[任意]
        x4 (float): 庇の平面方向の寸法[任意]
        x5 (float): 庇の平面方向の寸法[任意]
        y0 (float): 庇の断面方向の寸法[任意]
        y1 (float): 庇の断面方向の寸法[任意]
        y2 (float): 庇の断面方向の寸法[任意]
        y3 (float): 庇の断面方向の寸法[任意]
        y4 (float): 庇の断面方向の寸法[任意]
        y5 (_type_): 庇の断面方向の寸法[任意]

    Returns:
        float: 窓の日照面積率[%]
    """
    pg = 0.0

    ag = x3 * y3
    yy2 = y2
    yy3 = y3

    if y0 != 0.0:
        if y0 >= y2:
            y2 -= y0
        else:
            y2 = 0.0
            y3 -= (y0 - y2)
            if y3 < 0.0:
                y3 = 0.0

    ssh = np.sin(sh)

    if ssh <= 0.0:
        return pg

    cch = np.cos(sh)
    ssa = np.sin(sa)
    cca = np.cos(sa)
    cx = cca * np.cos(ge) + ssa * np.sin(ge)
    cg = ssh * np.cos(gh) + cch * np.sin(gh) * cx

    if cg <= 0.0:
        return pg

    y = ssh / (cch * cx)
    x = (np.cos(ge) * ssa - np.sin(ge) * cca) / (cx * np.sin(gh) + y * np.cos(gh))
    y = (-np.cos(gh) + y * np.sin(gh)) / (y * np.cos(gh) + np.sin(gh))

    if x > 0.0:
        a1 = x2
        a3 = x4
        x = x * x5
    else:
        a1 = x4
        a3 = x2
        x = -x * x1

    if y > 0.0:
        b1 = y2
        b3 = y4
        y = y * y1
    else:
        b1 = y4
        b3 = y2
        y = -y * y5

    if (x - x2 - x3 - x4) >= 0.0:
        return pg
    if (y - y2 - y3 - y4) >= 0.0:
        return pg

    w1 = (x2 + x3 + x4 - x) * (y2 + y3 + y4 - y)

    if (x - x3 - a3) >= 0.0:
        w4 = 0.0
    elif (x - a3) >= 0.0:
        w2 = x3 + a3 - x
    else:
        w2 = x3

    if (y - b1 - y3) >= 0.0:
        w4 = 0.0
    elif (y - b1) > 0.0:
        w4 = (b1 + y3 - y) * w2
    else:
        w4 = y3 * w2

    pg = w4 / ag * 100.0

    y2 = yy2
    y3 = yy3

    return pg

# Example usage
sh = np.radians(60.0)  # Example values for sh
sa = np.radians(0.0)  # Example values for sa
gh = np.radians(90.0)
ge = np.radians(0.0)  # Example value for ge
x1, x2, x3, x4, x5 = 1, 0.5, 2, 0.5, 1  # Example values for x variables
y0, y1, y2, y3, y4, y5 = 0.2, 1.0, 0.3, 3.5, 0.0, 1.0  # Example values for y variables

pg = balc(sh, sa, gh, ge, x1, x2, x3, x4, x5, y0, y1, y2, y3, y4, y5)
print(pg)

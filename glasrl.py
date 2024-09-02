import math

def glasrl(ic: int, ca: float) -> (float, float, float):
    """_summary_

    Args:
        ic (_type_): 求める対象　ic=-1 天空日射に対するもの
                                ic=-2 天空光に対するもの
                                ic= 1 直達日射に対するもの
                                ic= 2 直射日光に対するもの
        ca (_type_): 入射角の余弦

    Returns:
        tg: 透過率[－]
        arg: 吸収率[－]（ただし、天空光・直射日光の場合は反射率となる）
    """
    # Initialize constants
    t = [0.7754, 0.8101]
    a = [0.0483, 0.0243]
    c = [
        [2.028453, 1.319053, -9.00484, 10.48669, -3.955356],
        [0.957882, 9.34036, -27.72065, 28.44739, -10.12499],
        [0.402978, -1.40129, 2.421752, -2.01593, 0.64249],
        [0.164208, -1.248435, 4.197183, -5.379285, 2.286329]
    ]

    if ic < 0:
        i = -ic
        tg = t[i-1]
        arg = a[i-1]
    elif ic == 0:
        print("ic can not be nought.")
        return None, None, None
    else:
        tg = 0.0
        arg = 0.0
        k = ic - 1
        l = ic + 2 - 1
        for j in range(5):
            tg += c[k][j] * ca**(j+1)
            arg += c[l][j] * ca**(j+1)

    rhog = 1.0 - tg - arg

    return tg, arg, rhog

# Example usage
ic = 0
ca = math.cos(0.0)
tg, arg, rhog = glasrl(ic, ca)
print(f"tg: {tg}, arg: {arg}, rhog:{rhog}")

import math

def airflw(
        to: float, ti: float, ao: float, ai: float, ar: float, ac: float,
        q1: float, q2: float, q3: float, xl: float, afv: float, ib: float
        ) -> (float, float, float, float):
    """_summary_

    Args:
        to (_type_): 外気温度[℃]
        ti (_type_): 室温[℃]
        ao (_type_): 室外総合熱伝達率[kcal/(m2 g C)]
        ai (_type_): 室内総合熱伝達率[kcal/(m2 g C)]
        ar (_type_): 放射熱伝達率[kcal/(m2 g C)]
        ac (_type_): 対流熱伝達率[kcal/(m2 g C)]
        q1 (_type_): 部材1に吸収される放射熱量[kcal/(m2 h)]
        q2 (_type_): 部材2に吸収される放射熱量[kcal/(m2 h)]
        q3 (_type_): 部材3に吸収される放射熱量[kcal/(m2 h)]
        xl (_type_): 窓高さ[m]
        afv (_type_): 通過風量[m3/(m h)](単位窓幅あたり)
        ib (_type_): ブラインド開のときに1 開のとき0

    Returns:
        t1: 部材1の温度[℃]
        t2: 部材2の温度[℃]（ただし、部材1と部材2の平均温度）
        t3: 部材3の温度[℃]
        tout: 通過空気出口温度[℃]
    """
    # Initialize output variables
    t1, t2, t3, tout = 0.0, 0.0, 0.0, 0.0
    
    # Constants and intermediate variables
    acrd = ac + 2.0 * ar

    if ib > 0:
        acr = ac + ar
        ay = -2.0 * acrd / 0.29 / afv / acr
        ayl = ay * xl
        exl = math.exp(ayl)
        ax = (ai + acr) / (ao + acr)
        az = ac / ay / xl * (exl - 1.0)
        azr = az * ar
        t3 = -(ai + acr) + 0.5 * (acr - az - azr / acr) * (1.0 + ax)
        t3 = 1.0 / t3
        t3 = t3 * (-q3 - (az + azr / acr + ai) * ti +
                   q2 * (0.5 * az - 0.5 * ac + 0.5 * azr / acr - ar) / acrd +
                   0.5 * (q1 - q3 + ao * to - ai * ti) / (ao + acr) * (az - acr + azr / acr))
        t1 = ax * t3 + (q1 - q3 + ao * to - ai * ti) / (ao + acr)
        tout = ti * exl + 0.5 * (q2 / acrd + t1 + t3) * (1.0 - exl)
        t2 = (ac / acr * (ti - 0.5 / acrd + (t1 + t3)) / ay * (exl - 1.0) / xl +
              0.5 / acr * (q2 + ac / acrd * q2 + acr * (t1 + t3)))
    else:
        ax = (ao + acrd) / (ai + acrd)
        ay = -2.0 * ac / 0.29 / afv
        ayl = ay * xl
        exl = math.exp(ayl)
        az = (-q1 + q2 - ao * to + ai * ti) / (ai + acrd)
        aa = ac * (exl - 1.0) * 0.5 / ay / xl
        t1 = -ao - (1.0 + ax) * aa - (1.0 - ax) * (0.5 * ac + ar)
        t1 = 1.0 / t1
        t1 = t1 * (-q1 - ao * to - aa * 2.0 * ti + (aa - 0.5 * ac - ar) * az)
        t3 = ax * t1 + az
        tout = (ti - 0.5 * (t1 + t3)) * exl + 0.5 * (t1 + t3)
    
    return t1, t2, t3, tout

# Example usage
to = 20.0
ti = 22.0
ao = 0.5
ai = 1.0
ar = 0.2
ac = 0.3
q1 = 5.0
q2 = 10.0
q3 = 15.0
xl = 1.0
afv = 0.1
ib = 1

t1, t2, t3, tout = airflw(to, ti, ao, ai, ar, ac, q1, q2, q3, xl, afv, ib)
print(f"t1: {t1}, t2: {t2}, t3: {t3}, tout: {tout}")

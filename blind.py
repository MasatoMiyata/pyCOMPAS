import math

def calc_blind_transmittance(slat_absorption: float, slat_spacing: float,
                             slat_width: float, profile_angle_rad: float,
                             slat_angle_rad: float) -> (float, float, float):
    """
    ブラインドの透過率を計算する
    :param slat_absorption: スラットの日射吸収率[－]
    :param slat_spacing: スラット間隔[mm]
    :param slat_width: スラット幅[mm]
    :param profile_angle_rad: プロファイル角[rad]
    :param slat_angle_rad: スラット角[rad]
    :return: ブラインドの透過率、すきまを通る透過率、反射率[－]
    """

    # 三角関数の計算
    sin_t = math.sin(slat_angle_rad)
    cos_t = math.cos(slat_angle_rad)
    tan_t = math.tan(slat_angle_rad)
    sin_p = math.sin(profile_angle_rad)
    tan_p = math.tan(profile_angle_rad)

    # 各部寸法の計算
    ab = slat_spacing
    bc = slat_width
    cd = slat_spacing
    ad = slat_width
    be = min(slat_spacing / (cos_t * tan_p + sin_t), slat_width)
    ce = max(bc - be, 0.0)
    ac = math.sqrt((slat_width * cos_t) ** 2 + (slat_spacing - slat_width * sin_t) ** 2)
    ae = math.sqrt((be * cos_t) ** 2 + (slat_spacing - be * sin_t) ** 2)
    bd = math.sqrt((slat_width * cos_t) ** 2 + (slat_spacing + slat_width * sin_t) ** 2)
    de = math.sqrt((slat_spacing * cos_t) ** 2 + (slat_spacing * sin_t + ce) ** 2)
    l_gap = max(slat_spacing - slat_width * sin_t - slat_width * cos_t * tan_p, 0.0)
    z = slat_width * l_gap / (slat_spacing - l_gap)
    r_w = slat_width / (slat_width + z)
    r_z = z / (slat_width + z)

    # 面体面の形態係数の計算
    F12 = ((bd + ae) - (ab + de)) / (2 * ad)
    F13 = ((ac + de) - (ae + cd)) / (2 * ad)
    F14 = ((ad + ab) - bd) / (2 * ad)
    F15 = ((ad + cd) - ac) / (2 * ad)
    F21 = 0.0
    F24 = 0.0
    F25 = 0.0
    if be > 0.01:
        F21 = ((bd + ae) - (ab + de)) / (2 * be)
        F24 = ((ab + be) - ae) / (2 * be)
        F25 = max(((bc + de) - (bd + ce)) / (2 * be), 0.0)
    F31 = 0.0
    F34 = 0.0
    F35 = 0.0
    if ce > 0.01:
        F31 = ((ac + de) - (ae + cd)) / (2 * ce)
        F34 = ((bc + ae) - (be + ac)) / (2 * ce)
        F35 = ((cd + ce) - de) / (2 * ce)

    a1 = 1.0 - slat_absorption
    deno = 1.0 - a1 ** 2 * (F12 * F21 + F13 * F31)

    q_1 = r_w * a1 * F21 / deno
    q_2 = r_w * (1.0 + a1 ** 2 * F12 * F21 / deno)
    q_3 = r_w * a1 ** 2 * F21 * F13 / deno
    q_4 = r_w * a1 * (a1 * F21 * F14 + deno * F24 + a1 ** 2 * F21 * (F12 * F24 + F13 * F34)) / deno
    q_5 = r_w * a1 * (a1 * F21 * F15 + deno * F25 + a1 ** 2 * F21 * (F12 * F25 + F13 * F35)) / deno + r_z

    trance = q_5
    reflect = q_4

    return trance, r_z,  reflect


if __name__ == '__main__':

    # 透過率、反射率の計算
    trance, tau_pass_through, reflect = calc_blind_transmittance(slat_absorption=0.5, slat_width=25, slat_spacing=21.5,
                                   profile_angle_rad=math.radians(10), slat_angle_rad=math.radians(0))
    # 吸収率の計算
    absorpt = max(1.0 - trance - reflect, 0.0)

    print(trance, absorpt, reflect)

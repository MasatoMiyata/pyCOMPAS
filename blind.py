import math
import numpy as np

def calc_blind_transmittance(slat_absorption: np.ndarray, slat_spacing: float,
                             slat_width: float, profile_angle_rad: np.ndarray,
                             slat_angle_rad: np.ndarray) -> (np.ndarray, np.ndarray, np.ndarray):
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
    sin_t = np.sin(slat_angle_rad)
    cos_t = np.cos(slat_angle_rad)
    tan_t = np.tan(slat_angle_rad)
    sin_p = np.sin(profile_angle_rad)
    tan_p = np.tan(profile_angle_rad)

    # 各部寸法の計算
    ab = slat_spacing
    bc = slat_width
    cd = slat_spacing
    ad = slat_width
    be = np.minimum(slat_spacing / (cos_t * tan_p + sin_t), slat_width)
    ce = np.maximum(bc - be, 0.0)
    ac = np.sqrt((slat_width * cos_t) ** 2 + (slat_spacing - slat_width * sin_t) ** 2)
    ae = np.sqrt((be * cos_t) ** 2 + (slat_spacing - be * sin_t) ** 2)
    bd = np.sqrt((slat_width * cos_t) ** 2 + (slat_spacing + slat_width * sin_t) ** 2)
    de = np.sqrt((slat_spacing * cos_t) ** 2 + (slat_spacing * sin_t + ce) ** 2)
    l_gap = np.maximum(slat_spacing - slat_width * sin_t - slat_width * cos_t * tan_p, 0.0)
    z = slat_width * l_gap / (slat_spacing - l_gap)
    r_w = slat_width / (slat_width + z)
    r_z = z / (slat_width + z)

    # 面体面の形態係数の計算
    F12 = ((bd + ae) - (ab + de)) / (2 * ad)
    F13 = ((ac + de) - (ae + cd)) / (2 * ad)
    F14 = ((ad + ab) - bd) / (2 * ad)
    F15 = ((ad + cd) - ac) / (2 * ad)
    F21 = np.where(be > 0.01, ((bd + ae) - (ab + de)) / (2 * be), 0.0)
    F24 = np.where(be > 0.01, ((ab + be) - ae) / (2 * be), 0.0)
    F25 = np.where(be > 0.01, np.maximum(((bc + de) - (bd + ce)) / (2 * be), 0.0), 0.0)

    F31 = np.where(ce > 0.01, ((ac + de) - (ae + cd)) / (2 * ce), 0.0)
    F34 = np.where(ce > 0.01, ((bc + ae) - (be + ac)) / (2 * ce), 0.0)
    F35 = np.where(ce > 0.01, ((cd + ce) - de) / (2 * ce), 0.0)

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

    tan_p = np.tan(np.radians(np.array([90]))) / np.cos(np.radians(np.array([0])))
    pro = np.arctan(tan_p)
    print(math.tan(math.radians(90)) / math.cos(math.radians(0)))

    # 透過率、反射率の計算
    trance, tau_pass_through, reflect = calc_blind_transmittance(slat_absorption=np.array([0.5]), slat_width=25, slat_spacing=21.5,
                                   profile_angle_rad=np.array([math.radians(80)]), slat_angle_rad=np.array([math.radians(0)]))
    # 吸収率の計算
    absorpt = max(1.0 - trance - reflect, 0.0)

    print(trance, absorpt, reflect)

    # 入射角
    incident_angle_deg = np.arange(start=1, stop=91, dtype=float)
    incident_angle_rad = np.radians(incident_angle_deg)
    # スラット角度
    slat_angle_legend_deg = np.arange(start=0, stop=76, step=15)
    slat_angle_legend_rad = np.radians(slat_angle_legend_deg)

    for theta in slat_angle_legend_rad:
        trance, tau_pass_through, reflect = \
            calc_blind_transmittance(slat_absorption=np.array([0.5]), slat_width=25, slat_spacing=21.5,
                                        profile_angle_rad=incident_angle_rad, slat_angle_rad=theta)



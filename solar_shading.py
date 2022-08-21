import math

def calc_sunshine_area_ratio(
    h_sun: float,
    a_sun: float,
    window_inc: float,
    window_azm: float,
    window_width: float,
    window_height: float,
    sunshade_width: float,
    sunshade_height: float,
    bottom_margin: float,
    roof_depth: float,
    sidefin_depth: float) -> float:
    """日除けによる日照面積率の計算

    Args:
        h_sun (float): 太陽高度[rad]
        a_sun (float): 太陽方位角[rad]
        window_inc (float): 窓の傾斜角[rad]
        window_azm (float): 窓の方位角[rad]
        window_width (float): 窓の幅[m]
        window_height (float): 窓の高さ[m]
        sunshade_width (float): 庇の幅[m]
        sunshade_height (float): 庇のFLからの高さ[m]
        bottom_margin (float): FLから窓下端までの距離[m]
        roof_depth (float): 庇の出幅[m]
        sidefin_depth (float): 袖壁の出幅[m]

    Returns:
        float: 日照面積率[-]
    """

    # 窓面積の計算[m2]
    window_area = window_width * window_height

    # 窓両端から日除けまでの距離（日除けは窓の中心についている）
    side_margin = (sunshade_width - window_width) / 2.0

    # 入射角の方向余弦[-]
    sh = math.sin(h_sun)
    sw = math.cos(h_sun) * math.sin(a_sun)
    ss = math.cos(h_sun) * math.cos(a_sun)
    cos_theta = sh * math.cos(window_inc) \
        + math.cos(h_sun) * math.sin(window_inc) * math.cos(a_sun - window_azm)

    # 太陽が裏面にある場合は、日照面積率0で関数を抜ける
    if cos_theta <= 0.0:
        return 0.0

    # 壁面太陽方位[rad]
    tan_gamma = (sw * math.cos(window_azm) - ss * math.sin(window_azm)) / cos_theta

    # プロファイル角の計算[rad]
    tan_phi = (sh * math.sin(window_inc) \
        - sw * math.cos(window_inc) * math.sin(window_azm) \
            - ss * math.cos(window_inc) * math.cos(window_azm))\
         / cos_theta

    # 影の水平長さ
    x = sunshade_width - side_margin - sidefin_depth * abs(tan_gamma)
    # 影の垂直長さ
    y = sunshade_height- bottom_margin - roof_depth * tan_phi

    # 日照面積率の初期化
    sunshine_area_ratio = 0.0

    # 日照面積率の計算
    if x > 0.0 and y > 0.0 and tan_phi > 0.0:
        if x <= window_width and y <= window_height:
            sunshine_area_ratio = x * y / window_area
        elif x > window_width and y <= window_height:
            sunshine_area_ratio = y / window_height
        elif x <= window_width and y > window_height:
            sunshine_area_ratio = x / window_width
        elif x > window_width and y > window_height:
            sunshine_area_ratio = 1.0
    
    return sunshine_area_ratio


if __name__ == '__main__':
    
    print(calc_sunshine_area_ratio(
            h_sun=math.radians(30.0),
            a_sun=math.radians(0.0),
            window_inc=math.radians(90.0),
            window_azm=math.radians(0.0),
            window_width=3.0,
            window_height=2.5,
            sunshade_width=5.0,
            sunshade_height=3.0,
            bottom_margin=0.0,
            roof_depth=1.0,
            sidefin_depth=0.0))

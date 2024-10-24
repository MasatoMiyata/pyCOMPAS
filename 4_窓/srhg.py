def srhg(itype: int, srd: float, srs: float, ci: float) -> (float, float):
    """標準日射熱取得量を計算する

    Args:
        itype (_type_): ガラス種類 (1: 透明ガラスまたは吸熱ガラス, 2: 熱反射ガラス)
        srd (float): 窓面にあたる直達日射量 (W/m2)
        srs (float): 窓面にあたる天空放射量 (W/m2)
        ci (float): 入射角の余弦 (-)
        float (_type_): _description_

    Returns:
        _type_: 直達日射量の標準日射熱取得量 (W/m2), 天空放射量の標準日射熱取得量 (W/m2)
    """
    # FG1(Y)の定義
    def FG1(y):
        return y * (2.63899 + y * (1.00185 + y * (-19.9934 + y * (53.6021 +
            y * (-79.2915 + y * (70.6736 + y * (-35.3006 + y * 7.55907)))))))

    # FG2(Z)の定義
    def FG2(z):
        return z * (3.9486 + z * (0. + z * (-25.814 + z * (49.0163 +
            z * (-30.6415 + z * (0. + z * 4.3798))))))

    # 初期化
    hgd = 0
    hgs = 0

    # ガラスのタイプに応じて計算
    if itype == 1:  # TRANSPARENT GLASS OR HEAT ABSORPTION GLASS
        hgd = srd * FG1(ci)
        hgs = srs * 0.8112
    elif itype == 2:  # HEAT REFLECTION GLASS
        hgd = srd * FG2(ci)
        hgs = srs * 0.8641

    return hgd, hgs

if __name__ == '__main__':
    itype = 1
    srd = 0.846
    srs = 0.540
    ci = 0.866
    hgd, hgs = srhg(itype, srd, srs, ci)
    print(f'hgd = {hgd:.3f}, hgs = {hgs:.3f}')
    itype = 2
    srd = 0.846
    srs = 0.540
    ci = 0.866
    hgd, hgs = srhg(itype, srd, srs, ci)
    print(f'hgd = {hgd:.3f}, hgs = {hgs:.3f}')
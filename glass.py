import numpy as np

def glass(K: int, D: float, CI: float) -> (float, float):
    """透明ガラスまたは吸熱ガラスの直達日射に対する透過率、反射率を求める

    Args:
        K (_type_): ガラスの種類 (0: 透明ガラス, 1: 吸熱ガラス)
        D (float): ガラスの厚さ (m)
        CI (float): 入射角の余弦 (-)

    Returns:
        _type_: 透過率と反射率
    """
    # 初期化 (DO, TO)
    DO = [0.005, 0.005]
    TO = [0.846, 0.540]
    C = 1.52

    # 計算
    R0 = ((1 - C) / (1 + C)) ** 2
    TT0 = (-(1 - R0) ** 2 + np.sqrt((1 - R0) ** 4 + 4 * R0 ** 2 * TO[K] ** 2)) / (2 * R0 ** 2 * TO[K])
    TN = TT0 ** (D / DO[K])
    SI = np.sqrt(1 - CI ** 2)
    Y1 = np.sqrt(C ** 2 - SI ** 2)
    Y2 = C ** 2 * CI
    RI = 0.5 * (((Y2 - Y1) / (Y2 + Y1)) ** 2 + ((CI - Y1) / (CI + Y1)) ** 2)
    SID = SI / C
    SEID = 1.0 / np.sqrt(1.0 - SID ** 2)
    TI = TN ** SEID
    Y1 = 1 - RI ** 2 * TI ** 2
    T = (1 - RI) ** 2 * TI / Y1
    R = RI + RI * (1 - RI) ** 2 * TI ** 2 / Y1

    return T, R

if __name__ == '__main__':
    K = 0
    D = 0.005
    CI = np.cos(np.radians(30))
    T, R = glass(K, D, CI)
    print(f'T = {T:.3f}, R = {R:.3f}')
    K = 1
    D = 0.005
    CI = np.cos(np.radians(30))
    T, R = glass(K, D, CI)
    print(f'T = {T:.3f}, R = {R:.3f}')

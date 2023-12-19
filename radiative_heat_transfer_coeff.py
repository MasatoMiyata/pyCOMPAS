import numpy as np
from scipy import optimize

def calc_radiative_heat_transfer_coeff(area: np.ndarray, emissivity: np.ndarray, mrt: float) -> np.ndarray:

    """永田の方法による放射熱伝達率の計算
        area: 部位の面積[m2]
        emissivity: 放射率[-]
        mrt: 放射熱伝達率計算時のMRT[C]

    Returns:
        np.ndarray: 微小球に対する放射熱伝達率[W/(m2･K)]
    """


    # ステファンボルツマン定数
    SIGMA = 5.67e-8

    # 面積比の計算
    area_ratio= area / np.sum(area)

    # f_barの計算
    f_bar = optimize.fsolve(lambda f_bar: calc_f(f_bar, area_ratio=area_ratio), 1.0e-6)

    # 微小球に対する形態係数
    f_mrt = 0.5 * (1.0 - np.sqrt(1.0 - 4.0 * area_ratio / f_bar))

    # 微小球に対する放射熱伝達率
    return emissivity / (1.0 - emissivity * f_mrt) * 4.0 * SIGMA * (mrt + 273.15) ** 3


def calc_f(f_bar: float, area_ratio: np.ndarray) -> float:

    return 0.5 * np.sum(1.0 - np.sign(1.0 - 4 * area_ratio / f_bar) * np.sqrt(np.abs(1.0 - 4 * area_ratio / f_bar))) - 1.0


def calc_weights_for_mrt(h_r: np.ndarray, area: np.ndarray) -> np.ndarray:

    """放射伝熱計算時の微小球の放射温度計算における各面の重みを計算する
        h_r: 室内微小球に対する放射熱伝達率[W/(m2･K)]
        area: 部位の面積[m2]

    Returns:
        np.ndarray: 微小球の放射温度計算における各面の重み
    """
    
    return h_r * area / np.sum(h_r * area)

if __name__ == '__main__':

    area = np.array([20.0, 20.0, 5.0, 5.0, 5.0, 5.0])
    emissivity = np.full(len(area), 0.9)

    h_r = calc_radiative_heat_transfer_coeff(area=area, emissivity=emissivity, mrt=20.0)

    print (h_r)

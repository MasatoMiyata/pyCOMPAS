import numpy as np
import math
from typing import Tuple

def calc_alpha_matsuo_method(rs: np.ndarray, cs: np.ndarray, i_max: int) \
    -> Tuple[float, np.ndarray, np.ndarray, np.ndarray]:

    """ 留数定理で根を求める
        rs: 熱抵抗（室内側から）[m2 K/W]
        cs: 熱容量（室内側から）[J/(m2 K)]
        i_max: 根を探索する上限数

    Returns:
        a0: 定常項（熱貫流率）[W/(m2 K)]
        aa: 吸熱応答のパラメータ
        at: 貫流応答のパラメータ
        alpha: 根[1/s]
    """

    # 根を入れるNumpy配列
    alpha = np.zeros(i_max)
    # 貫流応答、吸熱応答パラメータを入れるNumpy配列
    aa = np.zeros(i_max)
    at = np.zeros(i_max)

    # 熱貫流率の計算[W/(m2･K)]
    a0 = 1.0 / np.sum(rs)

    # 時定数の計算[1/s]
    rcs = rs * cs

    # 多層壁の層数
    n_layers = len(rs)

    for i in range(i_max):
        d = np.zeros((n_layers, 4), dtype=float)
        dd = np.zeros((n_layers, 4), dtype=float)
        cd = np.zeros((n_layers, 4), dtype=float)
        cdd = np.zeros((n_layers, 4), dtype=float)
        for k in range(n_layers):
            d[k, 0] = 1.0
            d[k, 1] = rs[k]
            d[k, 2] = 0.0
            d[k, 3] = 1.0
            dd[k, 0] = 0.5 * rcs[k]
            dd[k, 1] = rs[k] * rcs[k] / 6.0
            dd[k, 2] = cs[k]
            dd[k, 3] = dd[k, 0]

        s = 0.0
        mm = 0
        for j in range(9999):
            cd[0, :] = d[0, :]
            cdd[0, :] = d[0, :]
            for k in range(1, n_layers):
                cd[k, 0] = cd[k-1, 0] * d[k, 0] + cd[k-1, 1] * d[k, 2]
                cd[k, 1] = cd[k-1, 0] * d[k, 1] + cd[k-1, 1] * d[k, 0]
                cd[k, 2] = cd[k-1, 2] * d[k, 0] + cd[k-1, 3] * d[k, 2]
                cd[k, 3] = cd[k-1, 2] * d[k, 1] + cd[k-1, 3] * d[k, 0]
                cdd[k, 0] = cd[k-1, 0] * dd[k, 0] + cdd[k-1, 0] * d[k, 0] \
                    + cd[k-1, 1] * dd[k, 2] + cdd[k-1, 1] * d[k, 2]
                cdd[k, 1] =  cd[k-1, 0] * dd[k, 1] + cdd[k-1, 0] * d[k, 1] \
                    + cd[k-1, 1] * dd[k, 0] + cdd[k-1, 1] * d[k, 0]
                cdd[k, 2] = cd[k-1, 2] * dd[k, 0] + cdd[k-1, 2] * d[k, 0] \
                    + cd[k-1, 3] * dd[k, 2] + cdd[k-1, 3] * d[k, 2]
                cdd[k, 3] =  cd[k-1, 2] * dd[k, 1] + cdd[k-1, 2] * d[k, 1] \
                    + cd[k-1, 3] * dd[k, 0] + cdd[k-1, 3] * d[k, 0]
            
            y = cd[n_layers-1, 1]
            yd = cdd[n_layers-1, 1]

            w1 = 0.0
            w2 = 0.0
            if i != 0:
                w1 = 0.0
                for j in range(i):
                    w2 = s + alpha[j]
                    w1 += 1.0 / w2
                yd -= y * w1
            
            s1 = s - y / yd
            if s1 < s:

                s = s1
                for k in range(n_layers):
                    if cs[k] > 0.0:
                        w1 = math.sqrt(- s * rcs[k])
                        w2 = math.cos(w1)
                        w3 = math.sin(w1)

                        d[k, 0] = w2
                        d[k, 1] = rs[k] * w3 / w1
                        d[k, 2] = - w1 * w3 / rs[k]
                        d[k, 3] = w2

                        dd[k, 0] = 0.5 * rcs[k] * w3 / w1
                        dd[k, 1] = 0.5 * rs[k] * rcs[k] * (w3 / w1 - w2) / w1 ** 2
                        dd[k, 2] = 0.5 * cs[k] * (w3 / w1 + w2)
                        dd[k, 3] = dd[k, 0]

                        mm = 0
            else:
                s = s1
                mm = 1
                break

            if mm == 1:
                break
        
        alpha[i] = - s1
        at[i] = 1.0 / (s1 * cdd[n_layers-1, 1])
        aa[i] = cd[n_layers - 1, 3] * at[i]
    
    return (a0, aa, at, alpha)


def calc_step_respose_factor(aa: np.ndarray, at: np.ndarray, alpha: np.ndarray, a0: float, n_max: int, delta_t: float)\
    -> Tuple[np.ndarray, np.ndarray]:

    """単位応答を求める
        aa: 吸熱応答のパラメータ
        at: 貫流応答のパラメータ
        alpha: 根[1/s]
        a0: 定常項（熱貫流率）[W/(m2 K)]
        n_max: 単位応答を計算する項数
        delta_t: 単位応答を計算する時間間隔[s]

    Returns:
        phi_a: 吸熱単位応答[W/(m2 K)]
        phi_t: 貫流単位応答[W/(m2 K)]
    """
    
    phi_a = np.zeros(n_max)
    phi_t = np.zeros(n_max)

    # 単位応答の計算
    for n in range(n_max):
        phi_a[n] = a0 + np.sum(aa * np.exp(-alpha * delta_t * n))
        phi_t[n] = a0 + np.sum(at * np.exp(-alpha * delta_t * n))
    
    return (phi_a, phi_t)


def calc_triangle_response_factor(aa: np.ndarray, at: np.ndarray, alpha: np.ndarray, a0: float, n_max: int, delta_t: float)\
        -> Tuple[np.ndarray, np.ndarray]:
    
    """二等辺三角波励振の応答係数を計算する
        aa: 吸熱応答のパラメータ
        at: 貫流応答のパラメータ
        alpha: 根[1/s]
        a0: 定常項（熱貫流率）[W/(m2 K)]
        n_max: 単位応答を計算する項数
        delta_t: 単位応答を計算する時間間隔[s]

    Returns:
        rft_a: 吸熱単位応答[W/(m2 K)]
        rft_t: 貫流単位応答[W/(m2 K)]
    """
    
    rft_a = np.zeros(n_max)
    rft_t = np.zeros(n_max)

    # 初項の計算
    rft_a[0] = a0 + np.sum(aa / (alpha * delta_t) * (1.0 - np.exp(- alpha * delta_t)))
    rft_t[0] = a0 + np.sum(at / (alpha * delta_t) * (1.0 - np.exp(- alpha * delta_t)))

    # 2項目以降の計算
    for j in range(1, n_max):
        
        rft_a[j] = - np.sum(aa / (alpha * delta_t) * (1.0 - np.exp(- alpha * delta_t)) ** 2 * np.exp(-(float(j) - 1) * alpha * delta_t))
        rft_t[j] = - np.sum(at / (alpha * delta_t) * (1.0 - np.exp(- alpha * delta_t)) ** 2 * np.exp(-(float(j) - 1) * alpha * delta_t))

    return rft_a, rft_t


def calc_Bs(rs: np.ndarray, cs: np.ndarray, alpha: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:

    """計算された根の範囲内でB(s)を計算する
        rs: 熱抵抗（室内側から）[m2 K/W]
        cs: 熱容量（室内側から）[J/(m2 K)]
        alpha: 根[1/s]
    
    Returns:
        Bs: 壁体の4端子行列から求めたB(s)
    """

    n_layer = len(cs)
    laps = np.logspace(np.log10(alpha[0]), np.log10(alpha[-1]), 1000)
    rcs = rs * cs
    Bsarray = np.zeros(len(laps))

    for k, lap in enumerate(laps):
        Ft = np.identity(2, dtype=float)

        for i in range(n_layer):
            Fi = np.zeros((2, 2), dtype=float)
            if cs[i] < 0.0001:
                Fi[0, 0] = 1.0
                Fi[0, 1] = rs[i]
                Fi[1, 0] = 0.0
                Fi[1, 1] = 1.0
            else:
                temp = np.sqrt(rcs[i] * lap)
                Fi[0, 0] = np.cos(temp)
                Fi[0, 1] = rs[i] / temp * np.sin(temp)
                Fi[1, 0] = - temp / rs[i] * np.sin(temp)
                Fi[1, 1] = np.cos(temp)
            
            Ft = np.dot(Ft, Fi)

            Bsarray[k] = Ft[0, 1]
    
    return laps, Bsarray


if __name__ == '__main__':

    rs = np.array([
        1.0 / 9.1,
        0.15 / 1.6,
        0.12 / 0.034,
        1.0 / 11.1
    ])

    cs = np.array([
        0.0,
        2000.0 * 0.15 * 1000.0,
        61.0 * 0.05 * 1000.0,
        0.0 
    ])

    # 根の計算
    a0, aa, at, alpha = calc_alpha_matsuo_method(rs=rs, cs=cs, i_max=15)

    print(a0)
    print(alpha)

    # 単位応答の計算
    phi_a, phi_t = calc_step_respose_factor(aa=aa, at=at, alpha=alpha, a0=a0, n_max=50, delta_t=900)

    # 二等辺三角波励振の応答係数の計算
    rft_a, rft_t = calc_triangle_response_factor(aa=aa, at=at, alpha=alpha, a0=a0, n_max=50, delta_t=900)
    print(rft_t)

    laps, Bs = calc_Bs(rs=rs, cs=cs, alpha=alpha)

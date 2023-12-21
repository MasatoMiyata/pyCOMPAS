import numpy as np

from gtrans import gtrans
from fixalp import fixalp

def modirf(alpf, ifixk, w, alp, ik, ao, a):
    """壁体貫流熱取得に対して、一部は対流により即時負荷となり、
    残りは室内各壁面へ輻射により熱伝達し遅れを伴って負荷となる。
    空気温励振に対する壁体貫流熱取得応答（対流＋輻射）を修正して、
    空気温励振に対する負荷応答（対流）とする。修正された応答関数は固定根で表される。

    Args:
        alpf (_type_): 固定根・一次元配列
        ifixk (_type_): 固定根の数
        w (_type_): 壁体貫流熱取得に対する負荷の応答関数値（伝達関数）
        alp (_type_): 壁体貫流・吸熱熱取得応答の根
        ik (_type_): 壁体貫流・吸熱熱取得応答の根の数
        ao (_type_): 壁の貫流・吸熱応答（入力時は熱取得応答）の係数
        a (_type_): 壁の貫流・吸熱応答（入力時は熱取得応答）の係数

    Returns:
        ao (_type_): 壁の貫流・吸熱応答（出力時は負荷応答）の係数
        a (_type_): 壁の貫流・吸熱応答（出力時は負荷応答）の係数
    """

    g = np.zeros(10)

    for i in range(ifixk):
        g[i] = w[i] * gtrans(ao, a, alp, ik, alpf[i])
    
    ao *= w[ifixk]
    fixalp(ifixk, alpf, g, ao, a)

    return ao, a


if __name__ == '__main__':

    print("テスト未実装")
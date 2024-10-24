import numpy as np

def fixalp(kk, falp, gk, ao, a):
    """固定根による多層壁単位応答近似

    Args:
        kk (_type_): 固定根の数
        falp (_type_): 固定根αk（1～kkの行列）
        gk (_type_): 精解の多層壁伝達関数をG(s)とすると、G(αk)の値（1～kkの行列）
        ao (_type_): 多層壁熱コンダクタンス
    
    Returns:
        a (_type_): 固定根を用いた近似応答の係数Ak（1～kkの行列）
    """

    falpo = np.zeros(15)
    b = np.zeros((15, 15))
    x = np.zeros(15)
    nstop = 0

    for k in range(kk):
        if falp[k] != falpo[k]:
            break
    else:
        for k in range(kk):
            x[k] = gk[k] - ao
        for k in range(kk):
            a[k] = 0.0
            for i in range(kk):
                a[k] += b[k, i] * x[i]
        return

    for k in range(kk):
        falpo[k] = falp[k]
        for i in range(kk):
            b[k, i] = falp[k] / (falp[k] + falp[i])

    try:
        inv_b = np.linalg.inv(b[:kk, :kk])
    except np.linalg.LinAlgError:
        nstop = 1

    if nstop == 1:
        for k in range(kk):
            x[k] = gk[k] - ao
        for k in range(kk):
            a[k] = 0.0
            for i in range(kk):
                a[k] += b[k, i] * x[i]
    else:
        print("***** ERROR FIXALP : NSTOP=", nstop, " *****")

    return a


if __name__ == '__main__':
    
    print("テスト未実装")

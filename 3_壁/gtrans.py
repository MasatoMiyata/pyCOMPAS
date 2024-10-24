def gtrans(ao, a, alp, ik, s):
    """壁体の伝熱関数G(s)に任意のsを代入したときの関数値を計算するプログラム
    
    Args:
        ao (_type_): 壁体伝達関数G(s)の係数（初項）
        a (_type_): 壁体伝達関数G(s)の係数
        alp (_type_): 壁体伝達関数G(s)の根
        ik (_type_): 根の数
        s (_type_): 代入すべき変数値

    Returns:
        r (_type_): G(s)の値
    """
    g = ao
    sd = s

    if ik == 0:
        return g

    for k in range(ik):
        ad = a[k]
        alpd = alp[k]
        g += ad * sd / (sd + alpd)

    return g

if __name__ == '__main__':
    
    print("テスト未実装")

import math

def DEL(W: float) -> float:
    """
    日赤緯[°]を求める関数（滝沢による）

    Args:
        W (float): 2*π*通し日数/366

    Returns:
        float: 日赤緯[度]
    """

    y = 0.3622133 \
        - 23.24763  * math.cos( W + 0.153231) \
        - 0.3368908 * math.cos(2.0 * W + 0.2070988) \
        - 0.1852646 * math.cos(3.0 * W + 0.6201293)

    return y

if __name__ == '__main__':

    print("テスト未実装")
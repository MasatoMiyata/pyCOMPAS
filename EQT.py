import math

def EQT(W:float) -> float:
    """_summary_

    Args:
        W (float): _description_

    Returns:
        float: _description_
    """

    y = -0.0002786409 \
        + 0.1227715   * math.cos( W + 1.498311) \
        - 0.1654575   * math.cos(2.0 * W - 1.261546) \
        - 0.005353830 * math.cos(3.0 * W - 1.157100)

    return y

if __name__ == '__main__':

    print("テスト未実装")
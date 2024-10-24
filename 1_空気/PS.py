import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['font.family'] = 'Noto Sans CJK JP'
plt.rcParams['grid.linestyle']='--'
plt.rcParams['grid.linewidth'] = 0.5

def calc_PS_Goff_Gratch(temperature:float) -> float:

    if temperature < 0:

        Z = 273.16 / (273.16 + temperature)
        Y = Z - 1.0
        PS = 10 ** ( -Y*9.09718 - math.log10(Z)*3.56654 + Y/Z*0.876793 - 2.219877 )

    elif temperature >= 0:

        Z = 373.16 / (273.16 + temperature)
        Y = Z - 1.0
        PS = 10 ** ( -Y*7.90298 + math.log10(Z)*5.02808 - (10**(Y/Z*11.344)-1.0)*1.3816*10**(-7) + (10**(-Y*3.49149)-1)*8.1328*10**(-3) )

    return PS


def calc_PS_Matuo(temperature:float) -> float:

    A0 = -5.111336
    A1 = 7.265429 * 10**(-2)
    A2 = -2.986334 * 10**(-4)
    A3 = 1.113417 * 10**(-6)
    A4 = -3.429809 * 10**(-9)
    A5 = 6.181450 * 10**(-12)

    B0 = -5.111472
    B1 = 8.233478 * 10**(-2)
    B2 = -3.069412 * 10**(-4)
    B3 = 9.639090 * 10**(-7)
    B4 = -6.426140 * 10**(-9)

    if temperature < 0:
        PS = math.exp(B0+temperature*(B1+temperature*(B2+temperature*(B3+B4*temperature))))

    else:
        PS = math.exp(A0+temperature*(A1+temperature*(A2+temperature*(A3+temperature*(A4+A5*temperature)))))

    return PS


def PS(temperature:float) -> float:
    """
    温度より飽和水蒸気圧を求める関数

    Args:
        temperature (float): 温度[℃]

    Returns:
        float: 飽和水蒸気圧[atm]
    """

    PS = calc_PS_Goff_Gratch(temperature)
    # PS = calc_PS_Matuo(temperature)

    return PS


if __name__ == '__main__':

    temperature_set = np.arange(-50, 101, 2)

    PS_Goff_Gratch = np.zeros(len(temperature_set))
    PS_Matsuo      = np.zeros(len(temperature_set))

    for i in range(0, len(temperature_set)):
        PS_Goff_Gratch[i] = calc_PS_Goff_Gratch(temperature_set[i])
        PS_Matsuo[i]      = calc_PS_Matuo(temperature_set[i])


    plt.figure(figsize=(10,5))
    plt.plot(temperature_set,PS_Goff_Gratch, label = "Goff_Gratch")
    plt.plot(temperature_set,PS_Matsuo, label = "松尾")
    plt.xlabel("温度[度]")
    plt.ylabel("飽和水蒸気圧[ATM]")
    plt.legend()
    plt.grid()

    plt.show()
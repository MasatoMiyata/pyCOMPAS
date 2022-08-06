from typing import Tuple
import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['font.family'] = 'Noto Sans CJK JP'
plt.rcParams['grid.linestyle']='--'
plt.rcParams['grid.linewidth'] = 0.5

from DEL import DEL
from EQT import EQT
from NUMDAY import NUMDAY

def SOPOS(FN:float,EL:float,M:int,N:int,HJ:int) -> Tuple[float, float, float]:
    """
    太陽位置を算出する関数

    Args:
        FN (float): 緯度
        EL (float): 経度
        M (int): 月
        N (int): 日
        HJ (int): 時刻

    Returns:
        SH (float): 太陽⾼度(h)の正弦
        SA (float): 太陽方位角(A)の正弦 
        CA (float): 太陽方位角(A)の余弦
    """
    
    RADI = 0.01745329
    ELS = 135.0

    W = 2 * math.pi * NUMDAY(M,N) / 366

    T = 15.0 * (HJ - 12.0 + EQT(W)) + EL - ELS
    # T = 15.0 * (HJ - 12.0)

    TJ = T/15.0+12

    FN1=FN*RADI
    SF=math.sin(FN1)
    CF=math.cos(FN1)
    DEL1=DEL(W)*RADI

    SD=math.sin(DEL1)
    CD=math.cos(DEL1)

    T1=T*RADI
    CT=math.cos(T1)
    ST=math.sin(T1)

    SH=SF*SD+CF*CD*CT

    if (SH > 0):
        CH=math.sqrt(1.0-SH**2)
        SA=CD*ST/CH
        CA=(SH*SF-SD)/(CH*CF)
    else:
        SH=0.0
        SA=0.0
        CA=0.0

    return SH, SA, CA


if __name__ == '__main__':

    FN = 35.68
    EL = 139.77
    N = 1

    SH = np.zeros([24,12])
    SA = np.zeros([24,12])
    CA = np.zeros([24,12])

    for M in range(0,12):
        for HJ in range(0,24):
            SH[HJ,M], SA[HJ,M], CA[HJ,M] = SOPOS(FN,EL,M,N,HJ)

    plt.figure(figsize=(10,5))
    for M in range(0,6):
        plt.plot(SH[:,2*M], label = f"sin(h): {2*M+1}月1日")
    plt.xlabel("時刻")
    plt.ylabel("sin(h)")
    plt.xlim([0,30])
    plt.ylim([0,1.01])
    plt.legend()
    plt.grid()

    plt.figure(figsize=(10,5))
    for M in range(0,6):
        plt.plot(SA[:,2*M], label = f"sin(A): {2*M+1}月1日")
    plt.xlabel("時刻")
    plt.ylabel("sin(A)")
    plt.xlim([0,30])
    plt.ylim([-1.05,1.05])
    plt.legend()
    plt.grid()

    plt.figure(figsize=(10,5))
    for M in range(0,6):
        plt.plot(CA[:,2*M], label = f"cos(A): {2*M+1}月1日")
    plt.xlabel("時刻")
    plt.ylabel("cos(A)")
    plt.xlim([0,30])
    plt.ylim([-1.05,1.05])
    plt.legend()
    plt.grid()

    plt.show()

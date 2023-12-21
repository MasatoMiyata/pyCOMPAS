from TBLM import TBLM

def wallm(IP, NT, NM, D):
    """壁体部位の熱物性値呼出し及びプリントアウト
    """

    RAM = [0] * NT
    CR = [0] * NT
    C = [0] * NT
    ROU = [0] * NT
    ZAI = [''] * NT

    if IP == 1:
        print(' ' * 12 + 'ATSUSA' + ' ' * 6 + 'NETSU' + ' ' * 3 + 'YOUSEKI' + ' ' * 3 + 'HINETSU' + ' ' * 2 + 'MITSUDO')
        print(' ' * 7 + 'NO.' + ' ' * 10 + 'DENDOURITSU' + ' ' + 'HINETSU' + ' ' * 27 + 'NAME')
        print(' ' * 14 + '(M)' + ' ' * 3 + '(KCAL/MHC)' + '(KCAL/M3C)' + '(KCAL/KGC)' + '(KG/M3)')

    for N in range(NT):
        RAM[N], CR[N], C[N], ROU[N], ZAI[N] = TBLM(NM[N])
        if IP == 1:
            print(f'{N:2}   {NM[N]:3} {D[N]:8.3f}   {RAM[N]:6.2f}   {CR[N]:5.3f}   {C[N]:6.1f}   {ROU[N]:6}   {ZAI[N]}')

    if IP == 1:
        print('-' * 80)


if __name__ == '__main__':

    # 使用例
    IP = 1
    NT = 10  # 例えば壁の材料数
    NM = [1, 2, 3, ...]  # 材料番号のリスト
    D = [0.1, 0.2, 0.3, ...]  # 各材料の厚さのリスト
    wallm(IP, NT, NM, D)

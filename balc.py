import numpy as np

def balc(
        sh: float,
        sa: float,
        gh: float,
        ge: float,
        x1: float,
        x2: float,
        x3: float,
        x4: float,
        x5: float,
        y0: float,
        y1: float,
        y2: float,
        y3: float,
        y4: float,
        y5
        ) -> float:
    pg = np.zeros(24)

    ag = x3 * y3
    yy2 = y2
    yy3 = y3

    if y0 != 0.0:
        if y0 >= y2:
            y2 -= y0
        else:
            y2 = 0.0
            y3 -= (y0 - y2)
            if y3 < 0.0:
                y3 = 0.0

    for j in range(24):
        ssh = np.sin(sh[j])

        if ssh <= 0.0:
            continue

        cch = np.cos(sh[j])
        ssa = np.sin(sa[j])
        cca = np.cos(sa[j])
        cx = cca * np.cos(ge) + ssa * np.sin(ge)
        cg = ssh * np.cos(gh) + cch * np.sin(gh) * cx

        if cg <= 0.0:
            continue

        y = ssh / (cch * cx)
        x = (np.cos(ge) * ssa - np.sin(ge) * cca) / (cx * np.sin(gh) + y * np.cos(gh))
        y = (-np.cos(gh) + y * np.sin(gh)) / (y * np.cos(gh) + np.sin(gh))

        if x > 0.0:
            a1 = x2
            a3 = x4
            x = x * x5
        else:
            a1 = x4
            a3 = x2
            x = -x * x1

        if y > 0.0:
            b1 = y2
            b3 = y4
            y = y * y1
        else:
            b1 = y4
            b3 = y2
            y = -y * y5

        if (x - x2 - x3 - x4) >= 0.0:
            continue
        if (y - y2 - y3 - y4) >= 0.0:
            continue

        w1 = (x2 + x3 + x4 - x) * (y2 + y3 + y4 - y)

        if (x - x3 - a3) >= 0.0:
            w4 = 0.0
        elif (x - a3) >= 0.0:
            w2 = x3 + a3 - x
        else:
            w2 = x3

        if (y - b1 - y3) >= 0.0:
            w4 = 0.0
        elif (y - b1) > 0.0:
            w4 = (b1 + y3 - y) * w2
        else:
            w4 = y3 * w2

        pg[j] = w4 / ag * 100.0

    y2 = yy2
    y3 = yy3

    return pg

# Example usage
sh = np.linspace(0, 2 * np.pi, 24)  # Example values for sh
sa = np.linspace(0, 2 * np.pi, 24)  # Example values for sa
gh = np.radians(90.0)
ge = np.radians(0.0)  # Example value for ge
x1, x2, x3, x4, x5 = 1, 2, 3, 4, 5  # Example values for x variables
y0, y1, y2, y3, y4, y5 = 0, 1, 2, 3, 4, 5  # Example values for y variables

pg = balc(sh, sa, gh, ge, x1, x2, x3, x4, x5, y0, y1, y2, y3, y4, y5)
print(pg)

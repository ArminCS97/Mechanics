"""1: si means constant of the friction force fi"""
"""2: All the numbers are rounded to 4 digits that is why the numbers may not be precise"""
"""3: v0=0 however you can change it"""

from sympy import symbols, solve


class Position:
    def __init__(self, t, linear_force_function, M1, M2, M3, s1, s2, s3, x0_M1, x0_M2, x0_M3, v0=0):
        self.M1 = M1
        self.M2 = M2
        self.M3 = M3
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
        self.x0_M1 = x0_M1
        self.x0_M2 = x0_M2
        self.x0_M3 = x0_M3
        self.F = linear_force_function(t)
        self.g = 10
        self.t = t
        self.v0 = v0

    def calculate_All(self):
        F1 = symbols('F1')
        a1 = symbols('a1')
        T = symbols('T')
        a2 = symbols('a2')

        f2k = self.s2 * self.M2 * self.g
        f1k = self.s1 * (T + self.M2 * self.g + self.M1 * self.g + self.s3 * F1)
        beta = -1 * self.F + f1k
        alpha = self.s3 * F1 + f2k
        theta = self.M1 * self.M2 + 2 * self.M2 * self.M3 + self.M1 * self.M3 + self.M3 ** 2

        """Below you can see the codes calculating 4 equations and 4 unknowns"""
        expr1 = (((self.M3 * (beta + self.M2 * self.g)) - self.M2 * (
                alpha - beta)) / theta) - a1  # VI
        expr2 = f2k + self.M2 * a2 - T  # I
        expr3 = -1 * self.M3 * a1 - F1  # II
        expr4 = ((beta + (self.M1 + self.M3) * a1) / -1 * self.M2) - a2
        solve_them = solve([expr1, expr2, expr3, expr4])
        all_the_unknowns = {
            'a1': round(solve_them.get(a1, None), 4),
            'F1': round(solve_them.get(F1, None), 4),
            'T': round(solve_them.get(T, None), 4),
            'a2': round(solve_them.get(a2, None), 4),
            'a3x': round(solve_them.get(a1, None), 4),
            'a37': round(solve_them.get(a1) - solve_them.get(a2), 4)
        }
        return all_the_unknowns

    def calculate_the_x(self):
        a1 = self.calculate_All().get('a1')
        a2 = self.calculate_All().get('a2')
        a3y = self.calculate_All().get('a37')
        v0 = self.v0
        M1_x1 = 1 / 2 * (a1 * self.t ** 2) + v0 * self.t + self.x0_M1
        M2_x1 = 1 / 2 * (a2 * self.t ** 2) + v0 * self.t + self.x0_M2
        M3_x1 = 1 / 2 * (a3y * self.t ** 2) + v0 * self.t + self.x0_M3
        return {
            'M1_x1': round(M1_x1, 4),
            'M2_x1': round(M2_x1, 4),
            'M3_x1': round(M3_x1, 4)
        }


ps = Position(12, lambda t: t * 6 + 1, M1=13, M2=20, M3=30, s1=1, s2=3, s3=0.5, x0_M1=0, x0_M2=0,
              x0_M3=10)
bg = ps.calculate_All()
print(bg)
print(ps.calculate_the_x())

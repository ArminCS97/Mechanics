"""1: si means constant of the friction force fi"""
"""2: All the numbers are rounded to 4 digits that is why the numbers may not be precise"""
"""3: v0=0 however you can change it"""

"""Some important assumptions:
    0- Let the leftmost uppermost part of each body be C. C is considered for all the 
        x0`s and x1`s.
    1- H is the vertical distance of M1 hole and is 100 (you can change it if you wish)
    2- distance_from_M1_to_M3 variable is for when C of M1 = C of M3 (both C`s are at the same level)
        and my Algorithm considers x0_M3 = distance_from_M1_to_M3 + x0_M1
    3- hole_length shows how far M3 can go down 
    4- if abs(M3_y1) > self.hole_length:
            M3_y1 = -self.hole_length
        it means that when M3 has reached the bottom of M1 hole, it does not go further down     
    5- M3_y1 < 0 as we going downward in the opposite direction of Y axis
    6-if abs(M2_x1) > self.distance_from_M1_to_M3:
            M2_x1 = distance_from_M1_to_M3
        it means that we dont let M2 fall off M1 into the hole of M1
    """

from sympy import symbols, solve


class Position:
    def __init__(self, t, linear_force_function, M1, M2, M3, s1, s2, s3, x0_M1, x0_M2,
                 distance_from_M1_to_M3, v0=0, hole_length=1000):
        self.M1 = M1
        self.M2 = M2
        self.M3 = M3
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
        self.x0_M1 = x0_M1
        self.x0_M2 = x0_M2
        self.x0_M3 = distance_from_M1_to_M3 + x0_M1
        self.distance_from_M1_to_M3 = distance_from_M1_to_M3
        self.F = linear_force_function(t)
        self.g = 10
        self.t = t
        self.v0 = v0
        self.hole_length = hole_length

    def __calculate_All(self):
        """These 4 unknowns are the most important ones and solving them can be a breakthrough"""
        F1 = symbols('F1')
        a1 = symbols('a1')
        T = symbols('T')
        a2 = symbols('a2')

        """f1k, f2k and f3k need to be calculated too"""
        f2k = self.s2 * self.M2 * self.g
        f1k = self.s1 * (T + self.M2 * self.g + self.M1 * self.g + self.s3 * F1)
        f3k = self.s3 * F1

        """Below I have used some helping dummy variables just for the sake of readability"""
        beta = -1 * self.F + f1k
        alpha = f3k + f2k
        theta = self.M1 * self.M2 + 2 * self.M2 * self.M3 + self.M1 * self.M3 + self.M3 ** 2

        """Below you can see the codes calculating 4 equations and 4 unknowns"""
        """Find the equations I, II, VI and V on page 4 and 6"""
        expr1 = -(((self.M3 * (beta + self.M2 * self.g)) - self.M2 * (
                alpha - beta)) / theta) - a1  # based on VI to find a1
        expr2 = f2k + self.M2 * a2 - T  # based on I to find T
        expr3 = -1 * self.M3 * a1 - F1  # based on II to find F1
        expr4 = ((beta + (self.M1 + self.M3) * a1) / -1 * self.M2) - a2  # based on V to find a2
        solve_them = solve([expr1, expr2, expr3, expr4])

        """Now that I have all the 4 important unknowns I use them to calculate other unknowns"""
        all_the_unknowns = {
            'a1': round(solve_them.get(a1, None), 4),
            'F1': round(solve_them.get(F1, None), 4),
            'T': round(solve_them.get(T, None), 4),
            'a2': round(solve_them.get(a2, None), 4),
            'a3x': round(solve_them.get(a1, None), 4),
            'a3y': round(solve_them.get(a1) - solve_them.get(a2), 4)
        }
        return all_the_unknowns

    def calculate_the_x(self):
        a1 = self.__calculate_All().get('a1')
        a2 = self.__calculate_All().get('a2')
        a3y = self.__calculate_All().get('a3y')
        a3x = self.__calculate_All().get('a3x')
        v0 = self.v0
        M1_x1 = 1 / 2 * (a1 * self.t ** 2) + v0 * self.t + self.x0_M1
        M2_x1 = 1 / 2 * (a2 * self.t ** 2) + v0 * self.t + self.x0_M2
        M3_x1 = 1 / 2 * (a3x * self.t ** 2) + v0 * self.t + self.x0_M3
        M3_y1 = 1 / 2 * (a3y * self.t ** 2) + v0 * self.t + 0
        if abs(M3_y1) >= self.hole_length:
            M3_y1 = -self.hole_length
        if abs(M2_x1) > self.distance_from_M1_to_M3:
            M2_x1 = distance_from_M1_to_M3
        return {
            'M1_x1': round(M1_x1, 4),
            'M2_x1': round(M2_x1, 4),
            'M3_x1': round(M3_x1, 4),
            'M3_y1': round(M3_y1, 4)
        }


distance_from_M1_to_M3 = 7

ts = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for t in ts:
    position = Position(t=t, linear_force_function=lambda t: 5 * t + 2, M1=6, M2=7, M3=10, s1=0.1,
                        s2=0.2, s3=0.5, x0_M1=0, x0_M2=0,
                        distance_from_M1_to_M3=distance_from_M1_to_M3)
    print(position.calculate_the_x())
    print('\n')

for t in ts:
    position = Position(t=t, linear_force_function=lambda t: -8 * t + 15, M1=6, M2=7, M3=10, s1=0.1,
                        s2=0.2, s3=0.5, x0_M1=1000, x0_M2=1000,
                        distance_from_M1_to_M3=distance_from_M1_to_M3)
    print(position.calculate_the_x())
    print('\n')


"""When M2 is way heavier than M3 we can see that my Algorithm works flawlessly
    as  M2-x1 and M3_y1 never change and a1 < 0 (as we going toward the opposite the side of X axis
    ) M1-x1 is decreasing as we going toward the opposite side of X axis and for a dramatic case 
    when t = 15 then M1_x1': -117.3164 that shows we going leftward and have already passed the origin
    """
for t in [5, 7, 10, 15]:
    special_case = Position(t=t, linear_force_function=lambda t2: -20 * t2, M1=6, M2=10, M3=1, s1=0.1,
                            s2=0.2, s3=0.5, x0_M1=1000, x0_M2=1000,
                            distance_from_M1_to_M3=distance_from_M1_to_M3)
    print(special_case.calculate_the_x())
    print('\n')
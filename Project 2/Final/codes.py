"""1: si means constant of the friction force fi"""
"""2: All the numbers are rounded to 4 digits that is why the numbers may not be precise"""
"""3: v0=0 however you can change it"""

"""Some important assumptions:
    0- Let the leftmost uppermost part of each body be C. C is considered for all the 
        x0`s and x1`s.
    1- hole_length is the vertical distance of M1 hole and is 1000 (you can change it if you wish)
    2- distance_from_M1_to_M3 variable is for when C of M1 = C of M3 (both C`s are at the same level)
        and my Algorithm considers x0_M3 = distance_from_M1_to_M3 + x0_M1
    3- hole_length shows how far M3 can go down 
    4- if abs(M3_y1) > self.hole_length:
            M3_y1 = -self.hole_length
        it means that when M3 has reached the bottom of M1 hole, it does not go further down     
    5- M3_y1 < 0 as we going downward in the opposite direction of Y axis
    6- if abs(M2_x1) < M1_x1:
            M2_x1 = abs(M1_x1)
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

    def calculate_All(self):
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
        expr3 = -self.M3 * a1 - F1  # based on II to find F1
        expr4 = ((beta + (self.M1 + self.M3) * a1) / -self.M2) - a2  # based on V to find a2
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
        a1 = self.calculate_All().get('a1')
        a2 = self.calculate_All().get('a2')
        a3y = self.calculate_All().get('a3y')
        a3x = self.calculate_All().get('a3x')
        v0 = self.v0
        M1_x1 = 1 / 2 * (a1 * self.t ** 2) + v0 * self.t + self.x0_M1
        M2_x1 = 1 / 2 * (a2 * self.t ** 2) + v0 * self.t + self.x0_M2
        M3_x1 = 1 / 2 * (a3x * self.t ** 2) + v0 * self.t + self.x0_M3
        M3_y1 = 1 / 2 * (a3y * self.t ** 2) + v0 * self.t + self.hole_length
        if abs(M3_y1) >= self.hole_length:
            M3_y1 = self.hole_length
        if abs(M2_x1) < M1_x1:
            M2_x1 = abs(M1_x1)
        return {
            'M1_x1': round(M1_x1, 4),
            'M2_x1': round(M2_x1, 4),
            'M3_x1': round(M3_x1, 4),
            'M3_y1': round(M3_y1, 4)
        }


distance_from_M1_to_M3 = 1500  # How far M2 can go

# code block number I
for t in [0, 1, 2, 3]:
    special_case = Position(t=t, linear_force_function=lambda t2: -4 * t2, M1=10, M2=10, M3=0.5,
                            s1=0.5,
                            s2=0.2, s3=0.5, x0_M1=1000, x0_M2=1000,
                            distance_from_M1_to_M3=distance_from_M1_to_M3)
    print(special_case.calculate_the_x())
    print(special_case.calculate_All())
    print('\n')

"""In the special case above when negative F we have interesting cases:
    when F=0 at time 0: {'M1_x1': 1000, 'M2_x1': 1000, 'M3_x1': 2500, 'M3_y1': 1000} meaning that no 
    block changes its position.
    When F starts growing bigger (in negative sign) we see that M1_x1 decreases slowly and goes
    toward the negative side of the X_axis that is why M2 has some force acted on itself and 
    makes it go to the right and therefore M3 goes down. So we see that M3_y1 decreases slowly.
    Rate of DECREASE of M1_x1 and Rate of decrease of M2_x1 depend on a1 and a2 respectively and do 
    depend largely on F magnitude (for this case F <0 as said above)
"""
#
# # code Block number II
# for t in [0, 1, 2, 3]:
#     special_case = Position(t=t, linear_force_function=lambda t2: -100 * t2, M1=10, M2=10, M3=0.5,
#                             s1=0.5,
#                             s2=0.2, s3=0.5, x0_M1=1000, x0_M2=1000,
#                             distance_from_M1_to_M3=distance_from_M1_to_M3)
#     print(special_case.calculate_the_x())
#     print(special_case.calculate_All())
#     print('\n')
#
# """Like the code block number I we have the same details for all but here F is more negative
#     when F=0 we have {'M1_x1': 1000, 'M2_x1': 1000, 'M3_x1': 2500, 'M3_y1': 1000} and as expected
#     all M1_x1, M2_x2, M3_y1 and M3_x1 decrease because F makes the whole system go toward the
#     opposite side of the X-axis and this makes a force (F1) act on M2 to make it go to right.
#     You may say so M2_x1 must increase as we are going rightward but the fact is that the whole
#     system goes leftward that is why rate of DECREASE of M1_x1 >> rate of decrease of M2_x1
# """
#
# # code block number III
# for t in [0, 1, 2, 3]:
#     special_case = Position(t=t, linear_force_function=lambda t2: 4 * t2, M1=10, M2=10, M3=0.5,
#                             s1=0.5,
#                             s2=0.2, s3=0.5, x0_M1=1000, x0_M2=1000,
#                             distance_from_M1_to_M3=distance_from_M1_to_M3)
#     print(special_case.calculate_the_x())
#     print(special_case.calculate_All())
#     print('\n')
#
# """
# When F is positive but its magnitude is not too big so it cannot pull the system leftward.
#     The whole system goes to the left so M1_x1, M2_x1, M3_x1 and M3_y1 all
#     decrease all together. The reason for this event is some forces like F1 or friction forces that
#     make the system go leftward for small F values
# """
#
# # code block number 4
# for t in [0, 1, 2, 3]:
#     special_case = Position(t=t, linear_force_function=lambda t2: 100 * t2, M1=10, M2=10, M3=0.5,
#                             s1=0.5,
#                             s2=0.2, s3=0.5, x0_M1=1000, x0_M2=1000,
#                             distance_from_M1_to_M3=distance_from_M1_to_M3)
#     print(special_case.calculate_the_x())
#     print(special_case.calculate_All())
#     print('\n')

"""When F is positive and very big this is what happens
    As expected the whole system goes to the right and as F is really big it may make M2 fall off 
    the M1. We have assumed that this does not happen so as you can see M1 does not move at all 
    (        if abs(M3_y1) >= self.hole_length:
            M3_y1 = self.hole_length ) takes care of that.
    To make sure that M2 does not fall off M1 I have put 
        if abs(M2_x1) < M1_x1:
            M2_x1 = abs(M1_x1)
"""

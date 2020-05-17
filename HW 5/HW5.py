import math

import matplotlib.pylab as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sympy import symbols, solve

print("Question 2")
my_id = "09170218"  # defining U
U = [int(u) for u in my_id]
X = [x for x in range(1, 9)]

plt.plot(X, U)
plt.xlabel("X")
plt.ylabel("U(x)")
plt.title("U_X graph")
plt.show()

"""
The mechanical energy (E = U + K) to maximize amplitude:
   we set E=5 (U(5) = 0) ==> Xl = 4.7 and Xr = 6 
   ATTENTION: (4.7, 2) this point is approximated by my eyes.
   and we get three points to fit a quadratic function to them (4.7, 2), (5, 0) and (6, 2)
"""

X = np.matrix([4.7, 5, 6]).reshape((3, 1))
U = np.matrix([2, 0, 2]).reshape((3, 1))
a = PolynomialFeatures(degree=2)
a.fit(X, U)
model = make_pipeline(a, LinearRegression())
model.fit(X, U)

alpha = model.steps[1][1].coef_[0][2]
beta = model.steps[1][1].coef_[0][1]
phi = model.steps[1][1].intercept_[0]

print("alpha: ", alpha, " beta: ", beta, " landa: ", phi)


def U(x):
    return alpha * x ** 2 + beta * x + phi


"""
At equilibrium point we have dU(x)/dx = 0
"""

equilibrium_point = symbols('equilibrium_point')
equation = 2 * alpha * equilibrium_point + beta  # dU(x)/dx = 0
find_equilibrium_point = solve([equation])
print("find_equilibrium_point: ", find_equilibrium_point.get(equilibrium_point))

"""
To estimate the frequency of the harmonic oscillations  we do the following:
    we have to convert the quadratic function into this form
    U = 1/2 * k * (x-x0)^2 opening up this equation we get
    alpha = 1/2 * k * x**2
    beta = -1/2 * k * x0 * x
    phi = 1/2 * k * x0**2
"""
k = 2 * alpha
mass = 1
print("k: ", k)
frequency_of_the_harmonic_oscillations = 1 / (2 * math.pi) * math.sqrt(k / mass)
print("frequency_of_the_harmonic_oscillations: ", frequency_of_the_harmonic_oscillations)

print('\n\n\n')
###########  Question 3 ###########################
print("Question 3")
h = 10
M = 10
"""
celli = [x_coordinate, y_coordinate, mass_of_the_cell]
N = [0,1,2,3,4,5,6,7,8,9]
mass of i are all equal if i= N - {4,5} = M/16
mass of i are all equal if i= {4,5} = M/4
"""
cell0 = [h / 8, 7 * h / 8, M / 16]
cell1 = [3 * h / 8, 7 * h / 8, M / 16]
cell2 = [5 * h / 8, 7 * h / 8, M / 16]
cell3 = [7 * h / 8, 7 * h / 8, M / 16]
cell4 = [h / 4, h / 2, M / 4]
cell5 = [3 * h / 4, h / 2, M / 4]
cell6 = [h / 8, h / 8, M / 16]
cell7 = [3 * h / 8, h / 8, M / 16]
cell8 = [5 * h / 8, h / 8, M / 16]
cell9 = [7 * h / 8, h / 8, M / 16]

"""
cell8 is the one that must be removed owing to my id ==>
"""
coordinates_of_all_cells = [cell0, cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell9]

x_of_center_of_mass = 0
center_of_mass = 0
for cell in coordinates_of_all_cells:
    x_of_center_of_mass += cell[0] * cell[2]
    center_of_mass += cell[2]
x_of_center_of_mass = x_of_center_of_mass / center_of_mass

y_of_center_of_mass = 0
center_of_mass = 0
for cell in coordinates_of_all_cells:
    y_of_center_of_mass += cell[1] * cell[2]
    center_of_mass += cell[2]
y_of_center_of_mass = y_of_center_of_mass / center_of_mass

"""Now I want to show all the points (except cell8)"""

all_the_x = [cell[0] for cell in coordinates_of_all_cells]
all_the_y = [cell[1] for cell in coordinates_of_all_cells]
center_of_mass_coordinates = [x_of_center_of_mass, y_of_center_of_mass]

plt.scatter(all_the_x, all_the_y)
plt.xlabel("X")
plt.ylabel("Y")
plt.title("X_Y graph")

plt.scatter(center_of_mass_coordinates[0], center_of_mass_coordinates[1], edgecolors='r')
plt.show()

print('\n\n\n')
################# Question 4 ################################
print("Question 4")

"""mi = [ x_coordinate_of_mi, y_coordinate_of_mi, mass_of_mi ] """
m1 = [0, 9, 1]
m2 = [1, 7, 2]
m3 = [0, 2, 2]
m4 = [1, 8, 1]

all_the_bodies = [m1, m2, m3, m4]
all_the_bodies_x = [body[0] for body in all_the_bodies]
all_the_bodies_y = [body[1] for body in all_the_bodies]

# part 1: will show all the points later on


# part 2:

center_of_mass_x = 0
center_of_mass = 0
for body in all_the_bodies:
    center_of_mass_x += body[0] * body[2]
    center_of_mass += body[2]
center_of_mass_x = center_of_mass_x / center_of_mass

center_of_mass_y = 0
center_of_mass = 0
for body in all_the_bodies:
    center_of_mass_y += body[1] * body[2]
    center_of_mass += body[2]
center_of_mass_y = center_of_mass_y / center_of_mass

center_of_mass_coordinates = [center_of_mass_x,
                              center_of_mass_y]  # center of mass of the original system

plt.scatter(all_the_bodies_x, all_the_bodies_y)
plt.xlabel("X")
plt.ylabel("Y")
plt.title("X_Y graph")
plt.scatter(center_of_mass_coordinates[0], center_of_mass_coordinates[1], edgecolors='r')
plt.show()
print("center_of_mass_coordinates: ", center_of_mass_coordinates)


# part 3

def distance_between_2_points(m1, m2):
    return math.sqrt((m1[0] - m2[1]) ** 2 + (m1[2] - m1[2]) ** 2)


L1 = distance_between_2_points(m1, m2)
L2 = distance_between_2_points(m2, m3)
L3 = distance_between_2_points(m3, m4)

print('L1: ', L1)
print('L2: ', L2)
print('L3: ', L3)

"""
We have obtained that theta is angle between v1 and x-axis and is 63.43 so
    x and y components of v1 are obtained as follows:
"""
theta = 63.43
v1 = L1
v1x = abs(math.cos(theta) * v1)
v1y = abs(math.sin(theta) * v1)
v1 = [-v1x, v1y]  # negative sign is for the fact that we are on the left side of X-axis
new_position_of_m1_after_1_second = [m1[0] + v1[0], m1[1] + v1[1]]
print("new_position_of_m1_after_1_second: ", new_position_of_m1_after_1_second)

"""
We have obtained that alpha is angle between v2 and x-axis and is 80.53 so
    x and y components of v1 are obtained as follows:
"""
alpha = 80.53
v2 = L3
v2x = abs(math.cos(alpha) * v2)
v2y = abs(math.sin(alpha) * v2)
v2 = [v2x, v2y]  # positive sign is for the fact that we are on the right side of X-axis
new_position_of_m4_after_1_second = [m4[0] + v2[0], m4[1] + v2[1]]
print("new_position_of_m4_after_1_second: ", new_position_of_m4_after_1_second)

L2_center_of_mass = 0  # center of mass of the rod L2 1 second after the explosions
"""
There is no external force acting on our system ==> explosion does not change the center of mass
    ==> center_of_mass_coordinates do not change.
The logic is the following:
    we use both new_position_of_m1_after_1_second and new_position_of_m4_after_1_second to calculate
    L2_center_of_mass.
"""
total_mass = m1[2] + m2[2] + m3[2] + m4[2]

L2_center_of_mass_x = symbols('L2_center_of_mass_x')
equation_for_x = ((L2_center_of_mass_x * (m2[2] + m3[2]) + new_position_of_m1_after_1_second[0] *
                   m1[2] + new_position_of_m4_after_1_second[0] * m4[2]) / total_mass) - \
                 center_of_mass_coordinates[0]

L2_center_of_mass_y = symbols('L2_center_of_mass_y')
equation_for_y = ((L2_center_of_mass_y * (m2[2] + m3[2]) + new_position_of_m1_after_1_second[1] *
                   m1[2] + new_position_of_m4_after_1_second[1] * m4[2]) / total_mass) - \
                 center_of_mass_coordinates[1]

L2_center_of_mass_x = solve([equation_for_x]).get(L2_center_of_mass_x)
L2_center_of_mass_y = solve([equation_for_y]).get(L2_center_of_mass_y)

print("L2_center_of_mass_x after explosion: ", L2_center_of_mass_x)
print("L2_center_of_mass_y after explosion: ", L2_center_of_mass_y)

plt.scatter([L2_center_of_mass_x], [L2_center_of_mass_y], edgecolors='r')
plt.xlabel("X")
plt.ylabel("Y")
plt.title("X_Y Graph After Explosion")
plt.show()

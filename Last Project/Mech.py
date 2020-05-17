import math

import matplotlib.pylab as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sympy import symbols, solve

my_id = "09170218"  # defining U
U = [int(u) for u in my_id]
X = [x for x in range(1, 9)]

# plt.plot(X, U)
# plt.xlabel("X")
# plt.ylabel("U(x)")
# plt.title("U_X graph")
# plt.show()

"""
The mechanical energy (E = U + K) to maximize amplitude:
    1- We assume that K = 0 and so E = U
    2- What points to find?
"""

X = np.matrix(X).reshape((len(X), 1))
U = np.matrix(U).reshape((len(U), 1))
a = PolynomialFeatures(degree=2)
a.fit(X, U)
model = make_pipeline(a, LinearRegression())
model.fit(X, U)

alpha = model.steps[1][1].coef_[0][1]
beta = model.steps[1][1].coef_[0][2]
phi = model.steps[1][1].intercept_[0]

print("alpha: ", alpha, " beta: ", beta, " landa: ", phi)

def U(x):
    return alpha * x**2 + beta*x + phi

"""
At equilibrium point we have dU(x)/dx = 0
"""

equilibrium_point = symbols('equilibrium_point')
equation = 2 * alpha * equilibrium_point + beta # dU(x)/dx = 0
find_equilibrium_point = solve([equation])
print("find_equilibrium_point: " ,find_equilibrium_point.get(equilibrium_point))

"""
To estimate the frequency of the harmonic oscillations  we do the following:
    we have to convert the quadratic function into this form
    U = 1/2 * k * (x-x0)^2 opening up this equation we get
    alpha = 1/2 * k * x**2
    beta = -1/2 * k * x0 * x
    phi = 1/2 * k * x0**2
"""
k = 2 * alpha
mass = -1 ##############################

frequency_of_the_harmonic_oscillations = 1/(2*math.pi) * math.sqrt(k/mass)
print("frequency_of_the_harmonic_oscillations: ", frequency_of_the_harmonic_oscillations)

"""
alpha:  -1.0357142857142814  beta:  0.1309523809523807  landa:  4.821428571428558
find_equilibrium_point:  0.0632183908045977
frequency_of_the_harmonic_oscillations:  0.22906308884655488
"""

###########  Question 3 ###########################
h = 10
M = 10
"""
celli = [x_coordinate, y_coordinate, mass_of_the_cell]
N = [0,1,2,3,4,5,6,7,8,9]
mass of i are all equal if i= N - {4,5} = M/16
mass of i are all equal if i= {4,5} = M/4
"""
cell0 = [h/8, 7*h/8, M/16]
cell1 = [3*h/8, 7*h/8, M/16]
cell2 = [5*h/8, 7*h/8, M/16]
cell3 = [7*h/8, 7*h/8, M/16]
cell4 = [h/4, h/2, M/4]
cell5 = [3*h/4, h/2, M/4]
cell6 = [h/8, h/8, M/16]
cell7 = [3*h/8, h/8, M/16]
cell8 = [5*h/8, h/8, M/16]
cell9 = [7*h/8, h/8, M/16]

"""
cell8 is the one that must be removed owing to my id ==>
"""
coordinates_of_all_cells = [cell0, cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell9]

x_of_center_of_mass = 0
center_of_mass = 0
for cell in coordinates_of_all_cells:
    x_of_center_of_mass += cell[0] * cell[2]
    center_of_mass += cell[2]
x_of_center_of_mass = x_of_center_of_mass/center_of_mass

y_of_center_of_mass = 0
center_of_mass = 0
for cell in coordinates_of_all_cells:
    y_of_center_of_mass += cell[1] * cell[2]
    center_of_mass += cell[2]
y_of_center_of_mass = y_of_center_of_mass/center_of_mass

"""Now I want to show all the points (except cell8)"""

all_the_x = [cell[0] for cell in coordinates_of_all_cells]
all_the_y = [cell[1] for cell in coordinates_of_all_cells]
center_of_mass_coordinates = [x_of_center_of_mass, y_of_center_of_mass]
#
# plt.scatter(all_the_x, all_the_y)
# plt.xlabel("X")
# plt.ylabel("Y")
# plt.title("X_Y graph")
#
# plt.scatter(center_of_mass_coordinates[0], center_of_mass_coordinates[1], edgecolors='r')
# plt.show()


################# Question 4 ################################
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

# part 3

def distance_between_2_points(m1, m2):
    return math.sqrt((m1[0] - m2[1]) ** 2 + (m1[2] - m1[2]) ** 2)



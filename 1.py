import math

import matplotlib.pyplot as plt

"""an = ap logically speaking"""
"""the graphs are drawn for each car"""
"""for drawing the graphs the distance is considered as delta_s or delta_s + x0"""
"""Prt 6 is vague. It has not said clearly whether 2 cars are exactly in a line ,I assume they are"""
"""No car can stay on the street so we have to pass it completely or stay at distance x0"""


class Car:
    def __init__(self, v0, an, ap, delta_t, x0, delta_s, v_max=None, condition=None):
        self.v0 = v0  # initial velocity of the car
        self.an = an  # negative acceleration
        self.ap = ap  # positive acceleration
        self.delta_T = delta_t  # duration of the yellow light
        self.x0 = x0  # distance to the intersection
        self.delta_S = delta_s  # width of the intersection
        self.does_it_stop = False
        self.v_max = v_max
        self.condition = condition

    """3 cases may occur and I consider each one of them inside the class"""
    """I: Car has to stop at position of the traffic light
      II: Car can pass easily
      III: None of the above cases is true """

    def does_it_stop_(self):  # the magnitude of acceleration is considered here

        if self.v0 ** 2 == 2 * self.an * self.x0:  # case I
            self.does_it_stop = True
            print("You must stop")

        self.condition = (self.x0 + self.delta_S) == (0.5 * (self.ap * self.delta_T ** 2) + (self.v0 * self.delta_T))
        if self.v_max is not None:
            v1 = math.sqrt(2 * (self.x0 + self.delta_S) + self.v0 ** 2)
            if v1 > self.v_max:
                print("Exceeding the max speed")
                return

        if self.does_it_stop == False and self.condition:  # case II
            self.does_it_stop = False
            print('You can pass easily so accelerate and pass the intersection')

        if self.does_it_stop == False and self.condition == False:
            print('You cannot pass however, you can be in somewhere in the intersection width + x0')
            """Considering the fact that we cannot change width of the intersection, duration of yellow light
            consider 2 sub-cases"""
            new_ap = 2 * (self.x0 + self.delta_S + self.v0 * self.delta_T) / (self.delta_T ** 2)
            print("If your v0 is ", self.v0, " Then your negative acceleration must be ", new_ap, " to pass.")

            new_v0 = (self.x0 + self.delta_S + 0.5 * (self.ap * self.delta_T ** 2)) / self.delta_T
            print("If your ap is ", self.ap, " Then your initial velocity should have been ", new_v0, " to pass.")
        print('\n\n')

    def draw_distance_time(self):  # these are my assumptions
        time = [t / 10 for t in range(self.delta_T * 10, 50, 1)]
        distance = [self.x0]
        for t in time:
            pop = distance.pop()
            x1 = 0.5 * (self.ap * t ** 2) + (self.v0 * t) + pop
            distance.append(pop)
            distance.append(x1)

        # plotting the points
        distance.pop()
        plt.plot(time, distance)

        # naming the x axis
        plt.xlabel('time')
        # naming the y axis
        plt.ylabel('distance')

        # giving a title to my graph
        plt.title('distance > 170 is not accepted')

        # function to show the plot
        plt.show()

    def draw_speed_distance(self):
        speed = []
        distance = []
        if self.does_it_stop:
            distance = [x / 10 for x in range(int(self.x0) * 10, 1700, 1)]
        else:
            distance = [x / 10 for x in range(int(self.x0 + self.delta_S) * 10, 1700, 1)]
        speed.append(self.v0)
        for x in distance:
            pop = speed.pop()
            v1 = math.sqrt(2 * x + pop ** 2)
            speed.append(pop)
            speed.append(v1)

        speed.pop()
        # plotting the points
        plt.plot(distance, speed)

        # naming the x axis
        plt.xlabel('distance')
        # naming the y axis
        plt.ylabel('speed')

        # giving a title to my graph
        plt.title('speed-distance Graph')

        # function to show the plot
        plt.show()


car1 = Car(v0=20, an=3, ap=3, delta_t=3, delta_s=10, x0=400 / 6)
car1.does_it_stop_()
car1.draw_distance_time()
car1.draw_speed_distance()

car2 = Car(v0=20.0, an=3.0, ap=3, delta_t=3, delta_s=10, x0=50.0)
car2.does_it_stop_()

car3 = Car(v0=20.0, an=2, ap=2, delta_t=3, delta_s=10, x0=55.0)
car3.does_it_stop_()

car4 = Car(v0=40, an=4, ap=4, delta_t=3, delta_s=10, x0=50)
car4.does_it_stop_()

car5 = Car(v0=27, an=2, ap=2, delta_t=5, delta_s=10, x0=150)
car5.does_it_stop_()

car6 = Car(v0=60, an=3, ap=3, delta_t=5, delta_s=10, x0=150, v_max=60)
car6.does_it_stop_()

"""2 cars"""

print('\n\n', "Considering 2 cars ", '\n')


def two_cars(frontal_car, rear_car, d):  # car1 is the frontal car, car2 is the rear car
    print("For frontal_car: ")
    frontal_car.does_it_stop_()
    rear_car.x0 = d + frontal_car.x0
    print("For rear_car: ")
    rear_car.does_it_stop_()

    print("Will they crash? ")
    """2 cars will crash if and only if x1 ( x of car 1) == x2 ( x of car 2)"""

    if frontal_car.does_it_stop:  # If car1 has to stop so does car2 => case I
        print("rear car has to stop too as frontal car stops")

    crush = 0.5 * frontal_car.ap * frontal_car.delta_T ** 2 + frontal_car.v0 * frontal_car.delta_T + frontal_car.x0 == \
            0.5 * rear_car.ap * rear_car.delta_T ** 2 + rear_car.v0 * rear_car.delta_T + rear_car.x0

    if frontal_car.does_it_stop is False and rear_car.does_it_stop is False and frontal_car.condition and rear_car.condition \
            and crush is False: # If car1 can pass the intersection easily, then car1 MAY be able to do so without no
        # crash => case II
        print('They will not crash and car2 can accelerate to pass the distance easily')
    """Considering the case III, it is similar to case I because anyway we have to stop based on my own assumption
    that no car can stay on the street"""
    if crush:
        print("They crush so car2 better not accelerate")
    else:
        print("they will not crash")
    print('\n\n')


two_cars(car1, car2, 12)
two_cars(car3, car5, 12)

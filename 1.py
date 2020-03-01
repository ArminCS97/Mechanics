import matplotlib.pyplot as plt

class Car:
    def __init__(self, v0, an, ap, delta_t, x0, delta_s):
        self.v0 = float(v0) # initial velocity of the car
        self.an = an # negative acceleration
        self.ap = ap # positive acceleration
        self.delta_T = delta_t  # duration of the yellow light
        self.x0 = x0  # distance to the intersection
        self.delta_S = delta_s  # width of the intersection
        self.does_it_stop = False

    """3 cases may occur and I consider each one of them inside the class"""
    """I: Car has to stop at position of the traffic light
      II: Car can pass easily
      III: None of the above cases is true """
    def does_it_stop_(self):  # the magnitude of acceleration is considered here

        if self.v0**2 == 2 * self.an *self.x0:  # case I
            self.does_it_stop = True
            print("You must stop")

        condition = (self.x0 + self.delta_S) == (0.5 * ( self.ap * self.delta_T**2) + (self.v0 * self.delta_T))

        if self.does_it_stop == False and condition: # case II
            self.does_it_stop = False
            print('You can pass easily so accelerate and pass the intersection')

        if self.does_it_stop == False and condition == False:
            print('You cannot pass however, you can be in somewhere in the intersection width')
            """Considering the fact that we cannot change width of the intersection, duration of yellow light
            consider 2 sub-cases"""
            new_ap = 2 * (self.x0 + self.delta_S + self.v0*self.delta_T) / (self.delta_T**2)
            print("If your v0 is ", self.v0, " Then your negative acceleration must be " , new_ap, " to pass.")

            new_v0 = (self.x0 + self.delta_S + 0.5 * ( self.ap * self.delta_T**2) ) / self.delta_T
            print("If your ap is ", self.ap, " Then your initial velocity should have been ", new_v0, " to pass.")

        print("")

    def draw_distance_time(self, distance, time):
        # plotting the points
        plt.plot(time, distance)

        # naming the x axis
        plt.xlabel('time')
        # naming the y axis
        plt.ylabel('distance')

        # giving a title to my graph
        plt.title('distance-time Graph')

        # function to show the plot
        plt.show()

    def draw_speed_distance(self, speed, distance):
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


car1 = Car(v0=20, an=3 , ap=30, delta_t=3, delta_s=10, x0=400/6)
car1.does_it_stop_()

car2 = Car(v0=20.0, an=4.0 , ap=40.0, delta_t=3, delta_s=10, x0=50.0)
car2.does_it_stop_()

car2 = Car(v0=20.0, an=4.0 , ap=40.0, delta_t=3, delta_s=10, x0=55.0)
car2.does_it_stop_()

car2 = Car(v0=40, an=4.0 , ap=4, delta_t=3, delta_s=10, x0=50)
car2.does_it_stop_()




import math
import pygame
import numpy as np


def uncertainty_add(distance,angle,sigma):
    mean = np.array([distance,angle])
    covariance = np.diag(sigma ** 2) #noise of distance and angle measurements are not correlated, hence only diagonal is non-zero
    #https://www.cuemath.com/algebra/covariance-matrix/

    distance, angle = np.random.multivariate_normal(mean,covariance) #gets the noisy values

    #this is to make sure we don't get negative values 
    distance = max(distance,0)
    angle = max(angle,0)

    return [distance,angle]


class LaserSensor:

    def __init__(self,Range,map,uncertainty): #uncertainty is an array with 2 values [sigma1,sigma2]
        self.Range = Range
        self.speed = 4 #rotations per second 
        self.sigma = np.array([uncertainty[0], uncertainty[1]])
        self.position = (0,0)
        self.map = map
        self.W, self.H = pygame.display.get_surface().get_size()
        self.sensedObstacles = []

    #Euclidean DISTANCE CALCULATOR
    def distance(self, obstaclePosition):
        px=(obstaclePosition[0]-self.position[0])**2
        py=(obstaclePosition[1]-self.position[1])**2
        return math.sqrt(px+py)
    

    def sense_obstacles(self):
        data=[]
        #store initial position of robot/sensor
        x1, y1 = self.position[0], self.position[1] 
        #discretize polar coordinates
        for angle in np.linspace(0, 2*math.pi,60,False): #scan from 0 to 2pi, 60 degree intervals
            #(interval dictates resolution of scanned map)

            x2,y2 = (x1 + self.Range*math.cos(angle) , y2 + self.Range*math.sin(angle)) #getting distance measurements

            for i in range (0,100):
                u = i/100
                x = int(x2 * u + x1 * (1-u))
                y = int(y2 * u + y1 * (1-u))
                if 0<x<self.W and 0<y<self.H: #if within the window/map
                    color = self.map.get_at((x,y)) #extract RGB value on map at that exact point. 
                    #if color is black aka the walls, calculate this distance from the robot
                    if (color[0],color[1],color[2]) == (0,0,0): 
                        distance = self.distance((x,y)) 
                        output = uncertainty_add(distance,angle, self.sigma) #add uncertainty to measurements
                        output.append(self.position) #add robot's position to list
                        #store measurement
                        data.append(output)
                        break
        

        #when sensor completes a full turn, return the data to be drawn in the map ...which is the responsiblity of the buildEnvironment class in the env.py file
        if len(data>0):
            return data
        else:
            return False








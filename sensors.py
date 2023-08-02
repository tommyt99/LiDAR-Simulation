import math
import pygame
import numpy as np


def uncertainty_add(distance,angle,sigma):
    mean = np.array([distance,angle])
    covariance = np.diag(sigma ** 2) #noise of distance and angle measurements are not correlated, hence only diagonal is non-zero. https://www.cuemath.com/algebra/covariance-matrix/
    distance, angle = np.random.multivariate_normal(mean,covariance) #gets the actual noisy values from Gaussian distribution  
    distance = max(distance,0) #max() function so we don't get negative values
    angle = max(angle,0)
    return [distance,angle]


class LaserSensor:

    def __init__(self,Range,map,uncertainty): #uncertainty is an array with 2 values [sigma1,sigma2]
        self.Range = Range
        self.speed = 0.5 #rotations per second #IS NOT USED THROUGHOUT THIS SCRIPT
        self.sigma = np.array([uncertainty[0], uncertainty[1]])
        self.position = (0,0) #<<< self.position should update to cursor's position!!!! BUG NEEDS TO BE FIXED
        self.map = map
        self.W, self.H = pygame.display.get_surface().get_size()
        self.sensedObstacles = []

    #Euclidean DISTANCE CALCULATOR
    def distance(self, obstaclePosition):
        px=(obstaclePosition[0]-self.position[0])**2
        py=(obstaclePosition[1]-self.position[1])**2
        return math.sqrt(px+py)
    

    def sense_obstacles(self):
        data=[] #stores distance and angle of ONLY WALLS from bot's position  
        x1, y1 = self.position[0], self.position[1]  
        for angle in np.linspace(0, 2*math.pi, 60,False): #scan from 0 to 2pi, 6 degree intervals (Resolution). For every angle, check if there is a wall
            x2,y2 = (x1 + self.Range*math.cos(angle), y1 + self.Range*math.sin(angle)) #coordinate of end of line segment
            for i in range (0,100): #If wall is within laser's path ...
                u = i/100 #Essentially a percentage
                x = int(x1 + (x2-x1)*u)
                y = int(y1 + (y2-y1)*u)

                """
                x = int(x2*u + x1*(1-u))
                y = int(y2*u + y1*(1-u))
                """

                if 0<x<self.W and 0<y<self.H: #if within the window/map. Reference point is pixel (0,0).
                    color = self.map.get_at((x,y)) #extract RGB value on map at every point of iteration within laser's path and do the quick check below ... 
                    if (color[0],color[1],color[2]) == (0,0,0): #if color is black, aka the walls, calculate this distance from the robot
                        distance = self.distance((x,y)) #References method above 
                        output = uncertainty_add(distance,angle, self.sigma) #add uncertainty to measurements
                        output.append(self.position) #add robot's position to list. Robot is always at (0,0) position though... ??? BUG
                        data.append(output) #[Distance, Angle, (x,y)] --> This is the return 
                        break
         
        #when sensor completes a full turn, return the data to be drawn in the map ...which is the responsiblity of the buildEnvironment class in the env.py file
        if len(data)>0:
            return data #[Distance, Angle, (x,y)] --> This is the return
        else:
            return False








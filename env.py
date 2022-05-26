import math
import pygame

class buildEnvironment:

    def __init__(self, MapDimensions):
        self.pointCloud=[]
        self.externalMap=pygame.image.load('floorplan.png')
        self.maph, self.mapw = MapDimensions
        self.MapWindowName = 'RRT path planning'
        pygame.display.set_caption(self.MapWindowName)
        self.map= pygame.display.set_mode((self.mapw, self.maph)) #initializes the blank canvas
        self.map.blit(self.externalMap, (0,0)) #overlays floor plan ontop of blank canvas
        
        #Colors
        self.black = (0,0,0)
        self.grey = (70,70,70)
        self.blue = (0,0,255)
        self.green = (0,255,0)
        self.red =(255,0,0)
        self.white = (255,255,255)


    #helper method that converts raw distance and angle data from sensor.py to cartesian coordinates
    def AD2pos(self,distance, angle, robotPosition):
        x = robotPosition[0] + distance * math.cos(angle)
        y = robotPosition[1] - distance * math.sin(angle) # - for display inverted y axis 
        return ( int(x), int(y) )

    def dataStorage(self,data):
        print(len(self.pointCloud))
        if data != False: #if data exists, then start for loop
            for element in data:
                point = self.AD2pos(element[0],element[1],element[2])
                if point not in self.pointCloud:
                    self.pointCloud.append(point)


    def show_sensorData(self):
        #draw data onto a "new" map
        self.infomap=self.map.copy()
        for point in self.pointCloud:
            self.infomap.set_at( (int(point[0]), int(point[1])), (255,0,0) ) #show sensor_data in RED pointcloud



import env, sensors
import pygame

#Step 1: Initialize environment and laser.

environment = env.buildEnvironment((600,1200)) #build the environment
environment.originalMap = environment.map.copy() #save a copy of the main map with the floor plan as "original map"
laser=sensors.LaserSensor(200, environment.originalMap, uncertainty=(0.5,0.01))
environment.map.fill( (0,0,0) ) #fill map with black to show red lidar scans, simulating blind environment
environment.infomap = environment.map.copy() #created a new object on the fly with this line 

#Step 2: Start pygame simulation
running = True
while running:
    sensorON = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT():
            running = False
        if pygame.mouse.get_focused():    
            sensorON=True  #sensor is only ON IF mouse cursor is INSIDE the window
        elif not pygame.mouse.get_focused():
            sensorON= False
    if sensorON: 
        position= pygame.mouse.get_pos()
        laser.position = position
        sensor_data = laser.sense_obstacles() #stores sensed data array into sensor_data
        environment.dataStorage(sensor_data) #adds sensor_data into point cloud
        environment.show_sensorData()
    environment.map.blit(environment.infomap, (0,0))
    pygame.display.update() 

pygame.quit() #sometimes window will not close after clicking red X 

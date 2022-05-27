import env, sensors
import pygame

#Step 1: Initialize environment and laser.

environment = env.buildEnvironment((600,1200)) #build the environment
environment.originalMap = environment.map.copy() #save a copy of the main map with the floor plan as "original map"
laser=sensors.LaserSensor(200, environment.originalMap, uncertainty=(0.5,0.01))

#fill map with black to show red lidar scans, simulating blind environment, then store as infomap
environment.map.fill( (0,0,0) ) 
environment.infomap = environment.map.copy() 

#Step 2: Setup pygame simulation
running = True
while running:
    sensorON = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.mouse.get_focused():    
            sensorON=True  #sensor is only ON IF mouse cursor is INSIDE the window
        elif not pygame.mouse.get_focused():
            sensorON= False
    if sensorON: 
        position= pygame.mouse.get_pos()
        laser.position = position
        sensor_data = laser.sense_obstacles() #Step 3: Sense. Stores sensed data array into sensor_data 
        environment.dataStorage(sensor_data) #store data in point cloud
        environment.show_sensorData() #Show point cloud
    environment.map.blit(environment.infomap, (0,0)) #overlay black infomap on top of red point cloud scans
    pygame.display.update() 

pygame.quit() #sometimes window will not close after clicking red X 

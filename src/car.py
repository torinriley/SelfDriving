# car.py
import numpy as np
import cv2

class Car:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.heading = 0 
        self.total_reward = 0  

    def move(self, steering_angle, speed):
        self.heading += steering_angle

        self.x += speed * np.cos(self.heading)
        self.y += speed * np.sin(self.heading)

    def draw(self, frame):
        car_color = (255, 0, 0)  
        cv2.rectangle(frame, 
                      (int(self.x), int(self.y)), 
                      (int(self.x + self.width), int(self.y + self.height)), 
                      car_color, 
                      -1)

    def get_position(self):
        return self.x, self.y, self.width, self.height

    def update_reward(self, reward):
        self.total_reward += reward
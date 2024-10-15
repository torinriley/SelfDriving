# car.py
import numpy as np
import cv2

class Car:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.heading = 0  # direction in radians
        self.total_reward = 0  # Track total rewards

    def move(self, steering_angle, speed):
        # Update the heading based on steering angle
        self.heading += steering_angle

        # Move the car forward in the direction of the heading
        self.x += speed * np.cos(self.heading)
        self.y += speed * np.sin(self.heading)

    def draw(self, frame):
        # Draw the car as a rectangle on the frame
        car_color = (255, 0, 0)  # Blue car
        cv2.rectangle(frame, 
                      (int(self.x), int(self.y)), 
                      (int(self.x + self.width), int(self.y + self.height)), 
                      car_color, 
                      -1)

    def get_position(self):
        return self.x, self.y, self.width, self.height

    def update_reward(self, reward):
        self.total_reward += reward
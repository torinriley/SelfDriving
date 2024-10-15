
import cv2
import numpy as np
from car import Car


canvas_width, canvas_height = 600, 400
lane_center = (150 + 450) // 2 
canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)


car = Car(x=200, y=300, width=40, height=20)

def draw_lanes(frame):
    lane_color = (255, 255, 255)  
    cv2.line(frame, (150, 0), (150, canvas_height), lane_color, 5)  
    cv2.line(frame, (450, 0), (450, canvas_height), lane_color, 5)  

def calculate_steering(car_x):
    lane_center = (150 + 450) // 2
    center_offset = lane_center - (car_x + car.width // 2)

    steering_angle = -center_offset * 0.002 
    return steering_angle

def check_lane(car_x):
    if car_x < 150 + 10 or car_x + car.width > 450 - 10:
        return -1  
    return 1 

def simulate():
    speed = 2 

    while True:
        
        frame = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)

        
        draw_lanes(frame)

        
        car_x, car_y, car_width, car_height = car.get_position()
        lane_reward = check_lane(car_x)
        car.update_reward(lane_reward)

        
        steering_angle = calculate_steering(car_x)

    
        car.move(steering_angle=steering_angle, speed=speed)

        car.draw(frame)

        cv2.putText(frame, f"Reward: {car.total_reward}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Self-Driving Car Simulation with P-Control', frame)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    simulate()
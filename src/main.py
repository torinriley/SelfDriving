import cv2
import numpy as np
from car import Car
import random

# Initialize the environment
canvas_width, canvas_height = 600, 400
lane_center = (150 + 450) // 2
canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)

# Create a car object
car = Car(x=200, y=300, width=40, height=20)

# List to store obstacles
obstacles = []

# Create random obstacles on the road
def create_obstacles(num_obstacles=5):
    for _ in range(num_obstacles):
        obstacle_x = random.randint(160, 420)  # Keep obstacles inside the lanes
        obstacle_y = random.randint(-canvas_height, 0)  # Start them off-screen
        obstacles.append((obstacle_x, obstacle_y, 50, 50))  # Obstacles are rectangles

# Draw obstacles on the frame
def draw_obstacles(frame):
    for i, (x, y, w, h) in enumerate(obstacles):
        obstacles[i] = (x, y + 2, w, h)  # Move the obstacle downward
        if y + h < canvas_height:  # Only draw obstacles that are visible
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), -1)  # Red obstacles

# Check if the car collides with an obstacle
def check_collision(car_x, car_y, car_width, car_height):
    for (x, y, w, h) in obstacles:
        if (car_x < x + w and car_x + car_width > x and
                car_y < y + h and car_y + car_height > y):
            return True  # Collision detected
    return False

def draw_lanes(frame):
    lane_color = (255, 255, 255)
    cv2.line(frame, (150, 0), (150, canvas_height), lane_color, 5)  # Left lane
    cv2.line(frame, (450, 0), (450, canvas_height), lane_color, 5)  # Right lane

def calculate_steering(car_x, car_y):
    lane_center = (150 + 450) // 2
    center_offset_x = lane_center - (car_x + car.width // 2)

    steering_angle_x = -center_offset_x * 0.002
    return steering_angle_x

def check_lane(car_x):
    if car_x < 150 + 10 or car_x + car.width > 450 - 10:
        return -1  # Penalize for going out of lanes
    return 1  # Reward for staying in lanes

def simulate():
    speed = 2  # Speed of the car

    create_obstacles()  # Create obstacles before simulation starts

    while True:
        frame = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)
        draw_lanes(frame)
        draw_obstacles(frame)

        # Get car's current position
        car_x, car_y, car_width, car_height = car.get_position()

        # Check for collisions and penalize if a collision occurs
        if check_collision(car_x, car_y, car_width, car_height):
            car.update_reward(-10)  # Deduct points for hitting an obstacle

        # Reward for staying within lanes
        lane_reward = check_lane(car_x)
        car.update_reward(lane_reward)

        # Calculate steering angle
        steering_angle_x = calculate_steering(car_x, car_y)

        # Move the car
        car.move(steering_angle=steering_angle_x, speed=speed)

        # Draw the car
        car.draw(frame)

        # Display the reward
        cv2.putText(frame, f"Reward: {car.total_reward}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('Self-Driving Car Simulation with Obstacles', frame)

        # Exit when 'q' is pressed
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    simulate()
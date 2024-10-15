# main.py
import cv2
import numpy as np
from car import Car

# Initialize the environment (a black canvas)
canvas_width, canvas_height = 600, 400
lane_center = (150 + 450) // 2  # Center of the lane
canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)

# Create a car object
car = Car(x=200, y=300, width=40, height=20)

def draw_lanes(frame):
    # Draw two lane boundaries
    lane_color = (255, 255, 255)  # White lanes
    cv2.line(frame, (150, 0), (150, canvas_height), lane_color, 5)  # Left lane
    cv2.line(frame, (450, 0), (450, canvas_height), lane_color, 5)  # Right lane

def calculate_steering(car_x):
    # Calculate how far the car is from the lane center
    lane_center = (150 + 450) // 2
    center_offset = lane_center - (car_x + car.width // 2)

    # Proportional controller: The farther away from the center, the more the car should steer
    steering_angle = -center_offset * 0.002  # Adjust the multiplier for sensitivity
    return steering_angle

def check_lane(car_x):
    # Ensure the car stays between the two lanes (150px to 450px)
    if car_x < 150 + 10 or car_x + car.width > 450 - 10:
        return -1  # Penalize for getting too close to the lane boundary
    return 1  # Reward for staying within lanes

def simulate():
    speed = 2  # Speed of the car

    while True:
        # Reset the canvas
        frame = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)

        # Draw lanes
        draw_lanes(frame)

        # Get car's current position and reward for lane keeping
        car_x, car_y, car_width, car_height = car.get_position()
        lane_reward = check_lane(car_x)
        car.update_reward(lane_reward)

        # Calculate steering angle using a proportional controller
        steering_angle = calculate_steering(car_x)

        # Move the car with the calculated steering angle
        car.move(steering_angle=steering_angle, speed=speed)

        # Draw the car on the canvas
        car.draw(frame)

        # Show reward info
        cv2.putText(frame, f"Reward: {car.total_reward}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the canvas
        cv2.imshow('Self-Driving Car Simulation with P-Control', frame)

        # Exit when 'q' is pressed
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    simulate()
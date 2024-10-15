cmake_minimum_required(VERSION 3.10)
project(SelfDrivingCar)


find_package(OpenCV REQUIRED)


add_executable(car_simulation src/main.cpp src/car.cpp)


target_include_directories(car_simulation PRIVATE ${OpenCV_INCLUDE_DIRS})
target_link_libraries(car_simulation ${OpenCV_LIBS})
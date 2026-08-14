from abc import ABC, abstractmethod
from functools import wraps
import logging
logging.basicConfig(level=logging.INFO)

def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        logging.info(f"Finished {func.__name__}")
        return result
    return wrapper

class InsufficientBatteryError(Exception):
    def __init__(self, robot_name, required, available):
        self.robot_name = robot_name
        self.required = required
        self.available = available
        super().__init__(
            f"{self.robot_name} needs {self.required}% battery for this task but only has {self.available}%"
        )
        
class Robot(ABC):
    manufacturer = "PhilTech"
    population = 0
    fleet = []

    def __init__(self, name, battery=100):
        self.name = name
        self.battery = battery
        Robot.population += 1
        Robot.fleet.append(self)
    
    def use_battery(self, amount):
        if amount > self.battery:
            raise InsufficientBatteryError(self.name, amount, self.battery)
        self.battery -= amount
        
    @property
    def battery(self):
        return self._battery

    @battery.setter
    def battery(self, value):
        if value < 0:
            value = 0
        if value > 100:
            value = 100
        self._battery = value
        
    @abstractmethod
    def perform_task(self):
        pass
      
    def __str__(self):
        return f"{self.name}: {self.battery}% battery"

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, battery={self.battery!r})"

class BasicRobot(Robot):
    def perform_task(self):
        return f"{self.name} is doing a basic task"
        
r1 = BasicRobot("Robot1", battery=5)
r2 = BasicRobot("Robot2", battery=-200)
r3 = BasicRobot("Robot3")
r3.battery = 150

print(r1.name, r1.battery)
print(r2.name, r2.battery)
print(r3.battery)
print(r3)
print([r3])
print(f"Population: {Robot.population}")
print(f"Manufacturer: {Robot.manufacturer}")
print(f"{r3.name} Manufacturer: {r3.manufacturer}")
print(r3.perform_task())

print("\n--------------------\n")

class CleaningRobot(Robot):
    def __init__(self, name, battery=100, dust_capacity=500):
        super().__init__(name, battery)
        self.dust_capacity = dust_capacity
        self.dust_collected = 0
    
    @log_action   
    def perform_task(self, amount=50):
        self.use_battery(10)
        self.dust_collected = min(self.dust_capacity, self.dust_collected + amount)
        return f"{self.name} cleaned {amount}g dust. Remaining battery: {self.battery}%"
    
    def __str__(self):
        return f"{self.name}: {self.battery}% battery (Dust: {self.dust_collected}g)"

cr1 = CleaningRobot("CleaningRobot1", dust_capacity=200)
print(cr1.name, cr1.dust_capacity)
print(cr1)
print(f"Population: {Robot.population}\n")

print(cr1.dust_collected)
print(cr1.perform_task(50))
print(cr1.dust_collected)

print("\n--------------------\n")

class DroneRobot(Robot):
    def __init__(self, name, battery=100, max_altitude=1000):
        super().__init__(name, battery)
        self.max_altitude = max_altitude
        self.current_altitude= 0
        
    def perform_task(self, altitude=100):
        self.use_battery(20)
        self.current_altitude = min(self.max_altitude, self.current_altitude + altitude)
        return f"{self.name} flew {altitude}m high. Remaining battery: {self.battery}%"
    
    def __str__(self):
        return f"{self.name}: {self.battery}% battery (Altitude: {self.current_altitude}m)"

dr1 = DroneRobot("DroneRobot1")
print(dr1.name, dr1.max_altitude)
print(dr1)
print(f"Population: {Robot.population}\n")

print(dr1.current_altitude)
print(dr1.perform_task(100))
print(dr1.current_altitude)

print("\n--------------------\n")

def fleet_report(robots):
    for r in robots:
        print(r)

print("FLEET REPORT (ALL):")       
fleet_report(Robot.fleet)

specific_fleet = [r2, cr1, dr1]
print("\nFLEET REPORT (SPECIFIC LIST):")     
fleet_report(specific_fleet)

print("\n--------------------\n")

def run_task_safely(robot, **kwargs):
    try:
        result = robot.perform_task(**kwargs)
    except InsufficientBatteryError as e:
        logging.error(e)
    else:
        print(result)
    finally:
        print(f"[{robot.name}] Current battery level: {robot.battery}%\n")
        
cr2 = CleaningRobot("CleaningRobot2", 50)
print("SAMPLE SUCCESS:")
run_task_safely(cr2, amount=100)

dr2 = DroneRobot("DroneRobot2", 10)
print("SAMPLE FAIL:")
run_task_safely(dr2, altitude=200)

print("--------------------\n")

print("SAMPLE DECORATOR:")
print(f"Name: {CleaningRobot.perform_task.__name__}")
cr3 = CleaningRobot("CleaningRobot3", battery=70)
result = cr3.perform_task(50)
print(f"Result: {result}")

print("\n--------------------\n")
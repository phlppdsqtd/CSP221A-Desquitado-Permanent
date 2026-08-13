from abc import ABC, abstractmethod

class Robot(ABC):
    manufacturer = "PhilTech"
    population = 0
    
    def __init__(self, name, battery=100):
        self.name = name
        self.battery = battery
        Robot.population += 1
        
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
        return f"{self.name} ({self.battery}% battery)"

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, battery={self.battery!r})"

class BasicRobot(Robot):
    def perform_task(self):
        return f"{self.name} is doing a basic task"
        
r1 = BasicRobot("Robot1")
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
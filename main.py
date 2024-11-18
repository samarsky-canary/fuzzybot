import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Define the fuzzy variables
temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'temperature')
humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')
fan_speed = ctrl.Consequent(np.arange(0, 101, 1), 'fan_speed')

# Define the membership functions for temperature
temperature['cold'] = fuzz.trimf(temperature.universe, [0, 0, 20])
temperature['warm'] = fuzz.trimf(temperature.universe, [10, 25, 40])
temperature['hot'] = fuzz.trimf(temperature.universe, [30, 40, 40])

# Define the membership functions for humidity
humidity['low'] = fuzz.trimf(humidity.universe, [0, 0, 50])
humidity['medium'] = fuzz.trimf(humidity.universe, [30, 50, 70])
humidity['high'] = fuzz.trimf(humidity.universe, [50, 100, 100])

# Define the membership functions for fan speed
fan_speed['low'] = fuzz.trimf(fan_speed.universe, [0, 0, 50])
fan_speed['medium'] = fuzz.trimf(fan_speed.universe, [30, 50, 70])
fan_speed['high'] = fuzz.trimf(fan_speed.universe, [50, 100, 100])

# Define the fuzzy rules
rule1 = ctrl.Rule(temperature['cold'] & humidity['low'], fan_speed['low'])
rule2 = ctrl.Rule(temperature['cold'] & humidity['medium'], fan_speed['low'])
rule3 = ctrl.Rule(temperature['cold'] & humidity['high'], fan_speed['medium'])
rule4 = ctrl.Rule(temperature['warm'] & humidity['low'], fan_speed['low'])
rule5 = ctrl.Rule(temperature['warm'] & humidity['medium'], fan_speed['medium'])
rule6 = ctrl.Rule(temperature['warm'] & humidity['high'], fan_speed['high'])
rule7 = ctrl.Rule(temperature['hot'] & humidity['low'], fan_speed['medium'])
rule8 = ctrl.Rule(temperature['hot'] & humidity['medium'], fan_speed['high'])
rule9 = ctrl.Rule(temperature['hot'] & humidity['high'], fan_speed['high'])

# Create the control system
fan_speed_control = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
fan_speed_simulation = ctrl.ControlSystemSimulation(fan_speed_control)

# Set input values for temperature and humidity
fan_speed_simulation.input['temperature'] = 16
fan_speed_simulation.input['humidity'] = 40

# Compute the output
fan_speed_simulation.compute()

# Print the result
print(f"Fan Speed: {fan_speed_simulation.output['fan_speed']}")

# Visualize the result
temperature.view(sim=fan_speed_simulation)
humidity.view(sim=fan_speed_simulation)
fan_speed.view(sim=fan_speed_simulation)
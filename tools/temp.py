import numpy as np
import matplotlib.pyplot as plt

# Define temperature range
Tmin = -40  # Minimum temperature in Celsius
Tmax = 125  # Maximum temperature in Celsius

# Generate temperature points
temps = np.linspace(Tmin, Tmax, 1000)

# Create plot
plt.figure(figsize=(10, 6))
plt.plot(temps, temps, 'b-', label='Temperature')
plt.xlabel('Temperature (°C)')
plt.ylabel('Value')
plt.title('Temperature Range')
plt.grid(True)
plt.legend()
plt.show()
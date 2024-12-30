import matplotlib.pyplot as plt
import numpy as np

# Parameters
max_speed = 10.0
acceleration = 0.1
target_position = 10.0
initial_speed = 5.0  # Starting speed set to 5

# Calculate time points with finer resolution
dt = 0.1
time_points = np.arange(0, 100, dt)

# Initialize arrays
positions = []
speeds = []
current_speed = initial_speed  # Set initial speed to 5
current_pos = 0

# Generate trajectory with acceleration and deceleration
for t in time_points:
    distance_to_stop = current_speed**2 / (2 * acceleration)
    distance_remaining = target_position - current_pos
    
    if distance_remaining > distance_to_stop:
        if current_speed < max_speed:
            current_speed = min(current_speed + acceleration * dt, max_speed)
    else:
        current_speed = max(current_speed - acceleration * dt, 0)
    
    current_pos += current_speed * dt
    
    positions.append(current_pos)
    speeds.append(current_speed)
    
    if current_pos >= target_position and current_speed == 0:
        break

# Trim arrays to actual movement time
time_points = time_points[:len(positions)]

# Plot results
plt.subplot(2, 1, 1)
plt.plot(time_points, positions)
plt.xlabel('Time')
plt.ylabel('Position')
plt.title('Single Joint Trajectory')

plt.subplot(2, 1, 2)
plt.plot(time_points, speeds)
plt.xlabel('Time')
plt.ylabel('Speed')

plt.tight_layout()
plt.show()

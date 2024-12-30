import csv
import matplotlib.pyplot as plt
import numpy as np

# Read data from CSV
with open('output_actual_velocity.csv', 'r') as file:
    reader = csv.reader(file)
    data = list(next(reader))  # Read first row into list

# Get sine and cosine data
sine_data = [498*1*(float(data[i])) for i in range(0, len(data), 2)]
cosine_data = [500*1.2*(float(data[i])+0.005) for i in range(1, len(data), 2)]

# Calculate phase using numpy arctan2
phase_data = np.arctan2(sine_data, cosine_data)

# Define the range for plotting
start_index = 0
end_index = 8192


#2933  3041
# Create x-axis values 
x = list(range(start_index,end_index))
phase_data_slice = 57*phase_data[start_index:end_index]
sine_data_slice = sine_data[start_index:end_index]
cosine_data_slice = cosine_data[start_index:end_index]


y_value = 3.1415926  # Example y-value
# Define the slope and intercept for the diagonal line
m = y_value/(end_index -start_index )  # Example slope
c = 0     # Example y-intercept

# Calculate y values for the diagonal line
diagonal_line = [ 57*( (m * xi + c)) for xi in range(0,(end_index -start_index))]

# Plot phase data in purple
#plt.plot(x, phase_data_slice, 'm-', label='Phase')  # 'm' specifies purple/magenta color
plt.plot(x, sine_data_slice, color='#FFA07A', label='Sine')    # Light salmon
plt.plot(x, cosine_data_slice, color='#ADD8E6', label='Cosine') # Light blue
#plt.plot(x, diagonal_line, color='#E6E6FA', label='Horizontal Line')  # Light lavender
#plt.plot(x, phase_data_slice-diagonal_line, 'g', label='erro')  # 'm' specifies purple/magenta color

plt.title('Phase Angle')
plt.xlabel('Sample Index')
plt.ylabel('Phase (radians)')
plt.grid(True)
plt.legend()
plt.show()

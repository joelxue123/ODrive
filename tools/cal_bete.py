import numpy as np
import matplotlib.pyplot as plt

def calculate_and_plot_ntc():
    # Known resistance points
    R25 = 100000  # 100kΩ at 25°C
    R85 = 10660   # 10.66kΩ at 85°C
    
    # Convert to Kelvin
    T25 = 273.15 + 25
    T85 = 273.15 + 85
    
    # Calculate Beta
    B = np.log(R25/R85) / (1/T25 - 1/T85)
    B1 = B + 1000
    # Temperature range for plot
    temps = np.linspace(-40, 125, 1000)
    T_kelvin = temps + 273.15
    
    # Calculate resistance curve
    R_curve = R25 * np.exp(B * (1/T_kelvin - 1/T25))
    R_curve1 = R25 * np.exp(B1 * (1/T_kelvin - 1/T25))
    # Plot
    plt.figure(figsize=(10, 6))
    plt.semilogy(temps, R_curve, 'b-', label=f'B25/85={B:.0f}K')
    plt.semilogy(temps, R_curve1, 'r-', label=f'B25/85={B1:.0f}K')
    plt.plot([25, 85], [R25, R85], 'ro', label='Reference Points')
    plt.grid(True)
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Resistance (Ω)')
    plt.legend()
    plt.title('NTC Thermistor Characteristic')
    plt.show()
    
    print(f"Beta (25/85): {B:.0f}K")
    return B

B = calculate_and_plot_ntc()
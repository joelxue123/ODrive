from odrive.utils import calculate_thermistor_coeffs
import matplotlib.pyplot as plt


def calculate_thermistor_coeffs1(degree, Rload, R_25, Beta, Tmin, Tmax, thermistor_bottom = False, plot = False):
    import numpy as np
    T_25 = 25 + 273.15 #Kelvin
    temps = np.linspace(Tmin, Tmax, 1000)
    tempsK = temps + 273.15

    # https://en.wikipedia.org/wiki/Thermistor#B_or_%CE%B2_parameter_equation
    r_inf = R_25 * np.exp(-Beta/T_25)
    R_temps = r_inf * np.exp(Beta/tempsK)
    if thermistor_bottom:
        V = R_temps / (Rload + R_temps)
    else:
        V = Rload / (Rload + R_temps)

    fit = np.polyfit(V, temps, degree)
    p1 = np.poly1d(fit)
    fit_temps = p1(V)

    if plot:
        import matplotlib.pyplot as plt
        print(fit)
        plt.plot(V, temps, label='actual')
        plt.plot(V, fit_temps, label='fit')
        plt.xlabel('normalized voltage')
        plt.ylabel('Temp [C]')
        plt.legend(loc=0)
        plt.show()

    return p1
def test_calculate_thermistor_coeffs():
    # Test parameters
    degree = 3
    Rload = 3300
    R_25 = 10000
    Beta = 3380
    Tmin = 0
    Tmax = 100
    thermistor_bottom = False
    plot = True

    # Run the function
    coeffs = calculate_thermistor_coeffs1(degree, Rload, R_25, Beta, Tmin, Tmax, thermistor_bottom,plot)

    # Print the coefficients
    print("Thermistor coefficients:")
    for i, coeff in enumerate(coeffs):
        print(f"Coefficient {i}: {coeff}")

    # If plot is True, the function will generate a plot
    # We'll show it here
    if plot:
        plt.show()

    return coeffs

if __name__ == "__main__":
    test_calculate_thermistor_coeffs()

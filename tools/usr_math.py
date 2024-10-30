# Function to divide two numbers
def divide(a, b):
    if b == 0:
        return "Division by zero is not allowed"
    try:
        return a / b
    except ZeroDivisionError:
        return "Division by zero is not allowed"
    except TypeError:
        return "Invalid input, please provide numeric values for a and b"
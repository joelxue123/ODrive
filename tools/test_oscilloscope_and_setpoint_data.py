def test_oscilloscope_and_setpoint_data():
    # Sample data for testing
    oscilloscope_data = [1.0, 2.0, 3.0, 4.0, 5.0]
    setpoint_data = [0.5, 1.5, 2.5, 3.5, 4.5]

    print("Testing oscilloscope and setpoint data:")
    for osc_item, set_item in zip(oscilloscope_data, setpoint_data):
        print(f"Oscilloscope: {osc_item}, Setpoint: {set_item}")

    # You can add assertions here to verify expected output
    assert len(oscilloscope_data) == len(setpoint_data), "Data lists should have the same length"

if __name__ == "__main__":
    test_oscilloscope_and_setpoint_data()

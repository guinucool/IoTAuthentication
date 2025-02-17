from controller import Controller

# Controller for a smart thermometer (TEMP, HUMIDITY)

thermo = Controller()
thermo.create_int_sensor(-120, 120)
thermo.create_float_sensor(0, 100)

# Controller for a smart assistant (COMMANDS)

assist = Controller()
assist.create_str_sensor(10)

# Controller for a random device (ALL)

rand = Controller()
rand.create_int_sensor(0, 100)
rand.create_float_sensor(0, 50)
rand.create_bool_sensor()
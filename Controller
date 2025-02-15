import random
from message import Message

class Controller:

    def __init__(self, sensors, comm_module):
            """
            Initializes the Controller class.

            :param sensors: A dictionary of sensor objects.
            :param actuator: An actuator object to control <- will not use one
            :param comm_module: A communication module object for data exchange <- need the code from raph
            """
            self.num_sensors = 8
            self.sensors = sensors  # Dictionary of sensor objects
            self.comm_module = comm_module  # Communication module object
            #self.state = "IDLE"  # Default system state

    def read_sensors(self):
         """ Simulates sensor data by generating random integer values. """
         return {f"sensor_{i+1}": random.randint(0, 100) for i in range(self.num_sensors)}

    def send_data(self, sensor_data):
        """ Sends sensor data to the communication module. """
        self.comm_module.send(sensor_data)  # Assume comm_module has a .transmit() method

    def receive_commands(self):
        """ Receives external commands from the communication module. """
        command = self.comm_module.receive()  # Assume comm_module has a .receive() method
        if command:
            self.send_data(self,self.read_sensors)

    def run(self):
        """ Main loop to handle sensor reading, processing, actuator control, and communication. """
        while True:
            sensor_data = self.read_sensors()
            self.send_data(sensor_data)
            self.receive_commands()

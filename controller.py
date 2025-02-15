from copy import deepcopy
import random

class Controller:
    '''
    A class that emulates an IoT device controller generating data for its sensors.

    Attributes:
        __sensors (list): The list of available sensors in the controller.
        __state (int): The state of the IoT device.

    For the state the following dictionary will be followed:

    0 - FUNCTIONAL
    1 - LOW POWER (BATTERY)
    2 - MALFUNCTION
    3 - SENSOR MALFUNCTION

    Each sensor will have the following structure:

    dict {
        'type' = 'INT' | 'FLOAT' | 'STRING' | 'BOOLEAN'
        'range' = (lower_bound, upper_bound) (INT | FLOAT)
        'length' = size (STRING)
    }
    '''

    def __init__(self, sv_addr: str, sv_port: int, sensors: list = None):
            '''
            Initializes a Controller object.

            Args:
                sv_addr (str): The address of the server.
                sv_port (int): The port of the server.
                sensors (list) = None: A preset list of sensors in the correct format.
            '''

            self.__sensors = list()
            self.__state = 0

            # In case a preset list as been given
            if (sensors is not None):
                self.__sensors = deepcopy(sensors)

    def create_int_sensor(self, lower_bound: int = None, upper_bound: int = None) -> None:
        '''
        Creates a integer type sensor that generates integers between the lower and upper bound (if applicable).

        Args:
            lower_bound (int) = None: The lower bound.
            upper_bound (int) = None: The upper bound.

        Returns:
            None: The generated sensor will be added to the list.
        '''
        pass

    def create_float_sensor(self, lower_bound: float = None, upper_bound: float = None) -> None:
        '''
        Creates a float type sensor that generates floats between the lower and upper bound (if applicable).

        Args:
            lower_bound (float) = None: The lower bound.
            upper_bound (float) = None: The upper bound.

        Returns:
            None: The generated sensor will be added to the list.
        '''
        pass

    def create_str_sensor(self, length: int) -> None:
        '''
        Creates a string type sensor that generates strings of a certain length.

        Args:
            length (int): The length of the generated strings.

        Returns:
            None: The generated sensor will be added to the list.
        '''
        pass

    def read_sensors(self, fail: list = None) -> list:
        '''
        Generates simulated data that would be readings from all the sensors.

        Args:
            fail (list): The list of sensor indexes that will fail.

        Returns:
            list: The list of sensor readings in the same order as the sensors.
        '''
        pass

    def change_state(self) -> None:
        '''
        Changes the state of the device randomly.

        Returns:
            None: The state of the device is changed.
        '''
        pass

    def gen_fail_list(self) -> list:
        '''
        Generates the list of failing sensors randomly.

        Returns:
            list: The list of random indexes of sensors to fail (might be empty).
        '''

    def read_device_bytes(self, fail: list = None) -> bytes:
        '''
        Generates simulated data that the device would output from all the sensors and it self.

        Args:
            fail (list): The list of sensor indexes that will fail.

        Returns:
            bytes: The readings in the bytes format.
        '''
        pass

    def bytes_to_infomartion(self, data: bytes) -> tuple[int, list]:
        '''
        Given binary information generate the device readings.

        Args:
            data (bytes): The readings in binary mode.

        Returns:
            tuple[int, list]: The device state and the list of readings.
        '''
        pass

    # Antiga
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

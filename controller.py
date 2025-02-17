from copy import deepcopy
import random
import struct
import string

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

    def __init__(self, sensors: list = None):
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

    def create_int_sensor(self, lower_bound: int, upper_bound: int) -> None:
        '''
        Creates a integer type sensor that generates integers between the lower and upper bound (if applicable).

        Args:
            lower_bound (int): The lower bound.
            upper_bound (int): The upper bound.

        Returns:
            None: The generated sensor will be added to the list.
        '''

        self.__sensors.append({'type': 'INT', 'range': (lower_bound, upper_bound)})

    def create_float_sensor(self, lower_bound: float, upper_bound: float) -> None:
        '''
        Creates a float type sensor that generates floats between the lower and upper bound (if applicable).

        Args:
            lower_bound (float): The lower bound.
            upper_bound (float): The upper bound.

        Returns:
            None: The generated sensor will be added to the list.
        '''

        self.__sensors.append({'type': 'FLOAT', 'range': (lower_bound, upper_bound)})

    def create_str_sensor(self, length: int) -> None:
        '''
        Creates a string type sensor that generates strings of a certain length.

        Args:
            length (int): The length of the generated strings.

        Returns:
            None: The generated sensor will be added to the list.
        '''

        self.__sensors.append({'type': 'STRING', 'length': length})

    def create_bool_sensor(self) -> None:
        '''
        Creates a boolean type sensor that generates boolean values.

        Returns:
            None: The generated sensor will be added to the list.
        '''

        self.__sensors.append({'type': 'BOOLEAN'})

    def read_sensors(self, fail: list = None) -> list:
        '''
        Generates simulated data that would be readings from all the sensors.

        Args:
            fail (list): The list of sensor indexes that will fail.

        Returns:
            list: The list of sensor readings in the same order as the sensors.
        '''

        # Defines the failing list as none if not given

        if fail is None:
            fail = []

        # Generate sensor data for each sensor

        data = []

        for i, sensor in enumerate(self.__sensors):

            # Checks if sensor is failing
            
            if i in fail:

                data.append(None) 

            else:

                sensor_type = sensor['type']
                
                if sensor_type == "INT":

                    data.append(random.randint(sensor['range'][0], sensor['range'][1]))

                elif sensor_type == "FLOAT":

                    data.append(round(random.uniform(sensor['range'][0], sensor['range'][1]), 2))

                elif sensor_type == "STRING":

                    data.append(''.join(random.choices(string.ascii_letters + string.digits, k = sensor['length'])))

                elif sensor_type == "BOOLEAN":

                    data.append(random.choice([True, False]))

        return data

    def change_state(self) -> None:
        '''
        Changes the state of the device randomly.

        Returns:
            None: The state of the device is changed.
        '''

        self.__state = random.choice([0, 1, 2, 3])

    def gen_fail_list(self) -> list:
        '''
        Generates the list of failing sensors randomly.

        Returns:
            list: The list of random indexes of sensors to fail (might be empty).
        '''

        num_sensors = len(self.__sensors)
        
        # In a range from 0 to num_sensors randomize how many sensors will fail

        num_failures = random.randint(0, num_sensors)

        # Randomly select sensor indexes to fail

        fail_list = random.sample(range(num_sensors), num_failures)

        return fail_list

    def read_device_bytes(self, fail: list = None) -> bytes:
        '''
        Generates simulated data that the device would output from all the sensors and it self.

        Args:
            fail (list): The list of sensor indexes that will fail.

        Returns:
            bytes: The readings in the bytes format.
        '''

        # Generate the data

        sensor_data = self.read_sensors(fail)  
        state_data = self.__state  
        
        byte_data = bytes()  
        
        # Convert device state to bytes 

        byte_data += state_data.to_bytes(4, 'little')

        # Convert readings to bytes
        
        for reading in sensor_data:

            if isinstance(reading, int):
                
                byte_data += reading.to_bytes(4, 'little')

            elif isinstance(reading, float):

                byte_data += (struct.pack("f", reading)) 

            elif isinstance(reading, str):

                byte_data += reading.encode("utf-8")  

            elif isinstance(reading, bool):

                byte_data += (struct.pack("?", reading)) 
        
        return byte_data

    def bytes_to_information(self, data: bytes) -> tuple[int, list]:
        '''
        Given binary information generate the device readings.

        Args:
            data (bytes): The readings in binary mode.

        Returns:
            tuple[int, list]: The device state and the list of readings.
        '''

        # Get the device state and the starting index

        state = int.from_bytes(data[0:4])
        byte_index = 4

        # Get the readings of the device

        readings = []

        for sensor in self.__sensors:

            sensor_type = sensor['type']
                
            if sensor_type == "INT":

                readings.append(data[byte_index:byte_index+4])

                byte_index += 4

            elif sensor_type == "FLOAT":

                readings.append(struct.unpack('f', data[byte_index:byte_index+4]))

                byte_index += 8

            elif sensor_type == "STRING":

                readings.append(data[byte_index:byte_index+sensor['length']].decode("utf-8"))

                byte_index += sensor['length']

            elif sensor_type == "BOOLEAN":

                readings.append(struct.unpack('?', data[byte_index:byte_index+1]))

                byte_index += 1

        return state, readings
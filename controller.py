from copy import deepcopy
import random
import struct

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

        if lower_bound is None or upper_bound is None:
            raise ValueError("> Both lower_bound and upper_bound must be defined for an integer sensor")
        if not isinstance(lower_bound, int) or not isinstance(upper_bound, int):
            raise TypeError("> Bounds must be integers!")
        if lower_bound > upper_bound:
            raise ValueError("> Lower bound cannot be greater than upper bound!")
        
        sensor = {
            'type': 'INT',
            'range': (lower_bound, upper_bound),
            'length': None 
        }

        self.__sensors.append(sensor)

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
        if lower_bound is None or upper_bound is None:
            raise ValueError("> Both lower_bound and upper_bound must be defined for an integer sensor")
        if not isinstance(lower_bound, float) or not isinstance(upper_bound, float):
            raise TypeError("> Bounds must be floats!")
        if lower_bound > upper_bound:
            raise ValueError("> Lower bound cannot be greater than upper bound!")
        
        sensor = {
            'type': 'FLOAT',
            'range': (lower_bound, upper_bound),
            'length': None 
        }

        self.__sensors.append(sensor)

        pass


    def create_str_sensor(self, length: int) -> None:
        '''
        Creates a string type sensor that generates strings of a certain length.

        Args:
            length (int): The length of the generated strings.

        Returns:
            None: The generated sensor will be added to the list.
        '''
        if length is None:
            raise ValueError("> The length must be defined for a string sensor")
        if not isinstance(length, str):
            raise TypeError("> Length must be string!")
        
        sensor = {
            'type': 'STRING',
            'range': None,
            'length': 25 
        }

        self.__sensors.append(sensor)

        pass

    def read_sensors(self, fail: list = None) -> list:
        '''
        Generates simulated data that would be readings from all the sensors.

        Args:
            fail (list): The list of sensor indexes that will fail.

        Returns:
            list: The list of sensor readings in the same order as the sensors.
        '''
        if fail is None:
            fail = []

        num_sensors = len(self.__sensors)
        sensor_data = []

        for i in range(num_sensors):
            if i in fail:
                sensor_data.append(None) 
            else:
                sensor_type = random.choice(["INT", "FLOAT", "STRING", "BOOLEAN"])
                
                if sensor_type == "INT":
                    sensor_data.append(random.randint(0, 100))
                elif sensor_type == "FLOAT":
                    sensor_data.append(round(random.uniform(-20.0, 94.5), 2))
                elif sensor_type == "STRING":
                    sensor_data.append(f"Sensor_{i}")
                elif sensor_type == "BOOLEAN":
                    sensor_data.append(random.choice([True, False]))

        return sensor_data


    def change_state(self) -> None:
        '''
        Changes the state of the device randomly.

        Returns:
            None: The state of the device is changed.
        '''
        self.__state = random.choice([0, 1, 2, 3])
        
        pass

    def gen_fail_list(self) -> list:
        '''
        Generates the list of failing sensors randomly.

        Returns:
            list: The list of random indexes of sensors to fail (might be empty).
        '''

        #Return and empty list if the number of sensors of the device is 0

        num_sensors = len(self.__sensors)
        if num_sensors == 0:
            return []
        
        #In a range from 0 to num_sensors randomize how many sensors will fail

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
        sensor_data = self.read_sensors(fail)  
        state_data = self.__state  
        
        byte_data = bytearray()  
        
        # Convert device state to bytes 

        byte_data.extend(struct.pack("B", state_data))  
        
        for sensor in sensor_data:
            if isinstance(sensor, int):  
                byte_data.extend(struct.pack("i", sensor))  
            elif isinstance(sensor, float):
                byte_data.extend(struct.pack("f", sensor)) 
            elif isinstance(sensor, str):
                encoded_str = sensor.encode("utf-8")  
                byte_data.extend(struct.pack(f"{len(encoded_str)}s", encoded_str))  
            elif isinstance(sensor, bool):
                byte_data.extend(struct.pack("?", sensor)) 
            else:
                raise TypeError(f"Unsupported sensor data type: {type(sensor)}")
        
        return bytes(byte_data)

        

    def bytes_to_information(self, data: bytes) -> tuple[int, list]:
        '''
        Given binary information generate the device readings.

        Args:
            data (bytes): The readings in binary mode.

        Returns:
            tuple[int, list]: The device state and the list of readings.
        '''
        if not data:
            raise ValueError("> No data was received")

        byte_index = 0
        device_state = struct.unpack_from("B", data, byte_index)[0]
        byte_index += struct.calcsize("B")

        readings = []
        
        while byte_index < len(data):
            remaining_bytes = len(data) - byte_index

            if remaining_bytes >= 4:  
                try:
                    int_value = struct.unpack_from("i", data, byte_index)[0]
                    readings.append(int_value)
                    byte_index += struct.calcsize("i")
                    continue
                except struct.error:
                    pass

                try:
                    float_value = struct.unpack_from("f", data, byte_index)[0]
                    readings.append(float_value)
                    byte_index += struct.calcsize("f")
                    continue
                except struct.error:
                    pass


            if remaining_bytes >= 1:
                try:
                    bool_value = struct.unpack_from("?", data, byte_index)[0]
                    readings.append(bool_value)
                    byte_index += struct.calcsize("?")
                    continue
                except struct.error:
                    pass


            str_value = data[byte_index:].decode("utf-8")
            readings.append(str_value)
            break  

        return device_state, readings

    # Antiga
    def read_sensors(self):
         """ Simulates sensor data by generating random integer values. """
         return {f"sensor_{i+1}": random.randint(0, 100) for i in range(self.num_sensors)}

    def send_data(self, sensor_data):
        """ Sends sensor data to the communication module. """
        self.comm_module.send(sensor_data)  

    def receive_commands(self):
        """ Receives external commands from the communication module. """
        command = self.comm_module.receive() 
        if command:
            self.send_data(self,self.read_sensors)

    def run(self):
        """ Main loop to handle sensor reading, processing, actuator control, and communication. """
        while True:
            sensor_data = self.read_sensors()
            self.send_data(sensor_data)
            self.receive_commands()


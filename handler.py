from message import Message
from time import time
from threading import Lock
from authenticator import InvalidCommParameters, Authenticator, KEY_LENGTH
from crypto import decrypt
from challenge import Challenge, CHALLENGE_SIZE

class Handler:
    '''
    A class representing the server handler, that manages the server information.

    Attributes:
        __devices (dict): The dictionary of devices the server recognizes.
        __database (list): The list of information the server stores about the devices.
        __host (socket): The hosting socket that accepts incoming connections.
    '''

    def __init__(self, devices: dict, sv_addr: str, sv_port: int):
        '''
        Initializes the Handler object.

        Args:
            devices (dict): The dictionary of know devices.
            sv_addr (str): The address of the server.
            sv_port (int): The port of the server.
        '''

        self.__database = list()
        self.__database_lock = Lock()
        self.__devices = devices
        # RAPH XDDXDXD

    def __add_entry_db(self, device_id: int, session_id: int, state: int, sensors: list) -> None:
        '''
        Adds an entry to the device information database.

        Args:
            device_id (int): The identifier of the device.
            session_id (int): The identifier of the session.
            state (int): The state of the device.
            sensors (list): The list of information from the sensors.
        
        Returns:
            None: The entry is added to the database.
        '''
        
        # Calculate the current timestamp

        timestamp = time()

        # Add the entry to the database

        entry = {
            'device_id': device_id,
            'session_id': session_id,
            'state': state,
            'sensors': sensors,
            'time': timestamp
        }

        with self.__database_lock:

            self.__database.append(entry)

    def show_db(self, device_id: int = None, session_id: int = None) -> None:
        '''
        Shows the database entries depending on the filters.

        Args:
            device_id (int): The identifier of device to filter.
            session_id (int): The identifier of session to filter.

        Returns:
            None: Prints the database information.
        '''
        
        with self.__database_lock:

            for entry in self.__database:

                if (device_id is not None and entry['device_id'] != device_id):
                    continue

                if (session_id is not None and entry['session_id'] != session_id):
                    continue

                print(f'dev_id: {entry['device_id']} | session: {entry['session_id']} | state: {entry['state']} | time: {entry['time']}')

                readings = ''

                for reading in entry['sensors']:

                    readings += str(reading) + ' '

                print(readings)

    def run_server(self) -> None:
        pass

    def handle_authentication(self, msg: Message) -> None:
        '''
        Handles the authentication process.

        Args:
            msg (Message): The message that generated the auth request.

        Returns:
            None: Handles the authentication.

        Throws:
            InvalidTag: If decryption fails due to authentication failure.
            InvalidCommParameters: If communication of the handshake has invalid parameters.
        '''

        # Check if device has running session

        if (self.__devices[msg.get_deviceId()]['auth'] is not None):
            raise InvalidCommParameters()
        
        # Create authenticator for this device

        self.__devices[msg.get_deviceId()]['auth'] = Authenticator(msg.get_deviceId(), False, msg.get_sessionId())

        # Create a challenge and send it to the device

        k1, ch1 = self.__devices[msg.get_deviceId()]['auth'].generate_challenge(False)

        m2 = self.__devices[msg.get_deviceId()]['auth'].handshake(False, challenge = ch1)

        # Send m2 # Throw exception if fail

        # Retreive the message challenge from the device and solve it

        # Receive m3 # Throw exception if fail

        if not self.__devices[msg.get_deviceId()]['auth'].check_handshake(m3):
            raise InvalidCommParameters()
        
        data = decrypt(m3.get_data(), k1)

        ch2 = Challenge.from_bytes(data[CHALLENGE_SIZE+KEY_LENGTH:])

        # Check the correctness of the solution to the challenge

        if not ch1.verify(data[0:CHALLENGE_SIZE]):
            raise InvalidCommParameters()

        t1 = data[CHALLENGE_SIZE:CHALLENGE_SIZE + KEY_LENGTH]

        k2 = self.__devices[msg.get_deviceId()]['auth'].solve_challenge(ch2, t1)

        m4 = self.__devices[msg.get_deviceId()]['auth'].handshake(True, k2, ch2.get_chal())

        # Associate the gotten session key from device

        self.__devices[msg.get_deviceId()]['auth'].feed_key(t1)

        # Send m4 # Throw exception if fail

    def handle_information(self, msg: Message) -> None:
        '''
        Handles messages that contain readings from the sensors of a device.

        Args:
            msg (Message): The message.

        Returns:
            None: Properly handles the message.

        Raises:
            InvalidCommParameters: If decryption fails due to authentication failure.
            InvalidTag: If decryption fails due to authentication failure.
        '''
        
        # Fetchs the data from the authenticated message

        data = self.__devices[msg.get_deviceId()]['auth'].decrypt(msg)

        # Converts the data to readings

        state, sensors = self.__devices[msg.get_deviceId()]['controller'].bytes_to_infomartion(data) # NEEDS TO RAISE EXCEPTION

        # Adds entry to the database

        self.__add_entry_db(msg.get_deviceId(), msg.get_sessionId(), state, sensors)

    def handle_conn(self) -> None:
        pass
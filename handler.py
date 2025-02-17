from message import Message
from time import time
from threading import Lock, Thread
from authenticator import InvalidCommParameters, Authenticator, KEY_LENGTH, TIME_TO_LIVE
from crypto import decrypt
from challenge import Challenge, CHALLENGE_SIZE
from socket import socket, AF_INET, SOCK_STREAM
from cryptography.exceptions import InvalidTag

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
        self.__host = socket(AF_INET, SOCK_STREAM)
        self.__host.bind((sv_addr, sv_port))
        self.__clients = []

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
        
        self.__host.listen(5)

        try:

            while (True):

                client_socket, _ = self.__host.accept()

                self.__clients.append(client_socket)

                Thread(target=self.__handle_conn, args=(client_socket,)).start()

        except Exception:

            pass

    def __handle_authentication(self, msg: Message, client: socket) -> None:
        '''
        Handles the authentication process.

        Args:
            msg (Message): The message that generated the auth request.
            client (Socket): The communication socket with the client.

        Returns:
            None: Handles the authentication.

        Throws:
            InvalidTag: If decryption fails due to authentication failure.
            InvalidCommParameters: If communication of the handshake has invalid parameters.
            ConnectionResetError: In case communication fails.
            BrokenPipeError: In case communication fails.
        '''

        # Check if device has running session

        if (self.__devices[msg.get_deviceId()]['auth'] is not None):
            raise InvalidCommParameters()
        
        # Create authenticator for this device

        self.__devices[msg.get_deviceId()]['auth'] = Authenticator(msg.get_deviceId(), False, msg.get_sessionId())

        # Create a challenge and send it to the device

        k1, ch1 = self.__devices[msg.get_deviceId()]['auth'].generate_challenge(False)

        m2 = self.__devices[msg.get_deviceId()]['auth'].handshake(False, challenge = ch1)

        m2.write_bytes(client)

        # Retreive the message challenge from the device and solve it

        m3 = Message.read_bytes(client)

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

        m4.write_bytes(client)

    def __handle_information(self, msg: Message) -> None:
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

        # Checks if the current device session finished

        if self.__devices[msg.get_deviceId()]['auth'].time_lived() == TIME_TO_LIVE:

            self.__devices[msg.get_deviceId()]['auth'].reset()

    def __handle_conn(self, client: socket) -> None:
        
        try:

            while True:

                # Reads the message sent from client

                msg = Message.read_bytes(client)

                # Interprets the message received

                if msg.get_type() == b'0':

                    self.__handle_authentication(msg)

                elif msg.get_type() == b'1':
                    
                    self.__handle_information(msg)

                else:

                    raise InvalidCommParameters()

        except (ConnectionResetError, BrokenPipeError, InvalidCommParameters, InvalidTag):

            pass

        finally:

            # Removes the finished connection

            client.close()
            self.__clients.remove(client)

    def close(self) -> None:

        self.__host.close()

        for client in self.__clients:
            client.close()

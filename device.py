from authenticator import InvalidCommParameters, Authenticator, KEY_LENGTH, TIME_TO_LIVE
from controller import Controller
from copy import deepcopy
from socket import socket, AF_INET, SOCK_STREAM
from message import Message
from challenge import Challenge, CHALLENGE_SIZE
from crypto import decrypt
from time import sleep

class Device:
    '''
    A class that emulates the functioning IoT device controller.

    Attributes:
        __controller (controller): The sensors and state controller.
        __server (communicator): The connection socket to the server.
    '''

    def __init__(self, sv_addr: str, sv_port: int, device_id: int, controller: Controller):
            '''
            Initializes a Device object.

            Args:
                sv_addr (str): The address of the server.
                sv_port (int): The port of the server.
                device_it (int): The identifier of the device.
                controller (controller): The controller of the IoT device state and sensors.
            '''

            self.__deviceId = device_id
            self.__server = socket(AF_INET, SOCK_STREAM)
            self.__server.connect((sv_addr, sv_port))
            self.__authenticator = None
            self.__controller = deepcopy(controller)

    def __send_sv(self, data: bytes) -> None:
        '''
        Sends information to the server.

        Args:
            data (bytes): Information to be sent to the server.

        Returns:
            None: The information is sent to the server
        '''
        
        msg = self.__authenticator.encrypt(data)

        msg.write_bytes(self.__server)
        
    def __recv_sv(self) -> bytes:
        '''
        Receives information from the server.

        Returns:
            bytes: The information received
        '''

        msg = Message.write_bytes(self.__server)

        return self.__authenticator.decrypt(msg)

    def __authenticate(self) -> None:
        '''
        Authenticates the server and itself, agreeing on a shared key.

        Returns:
            None: The authentication is sucessful and the key is agreed.

        Raises:
            InvalidTag: If decryption fails due to authentication failure.
            InvalidCommParameters: If communication of the handshake has invalid parameters.
            ConnectionResetError: In case communication fails.
            BrokenPipeError: In case communication fails.
        '''

        # Reset or initialize the authenticator
        
        if self.__authenticator is None:
             
            self.__authenticator = Authenticator(self.__deviceId, True)

        else:
             
            self.__authenticator.reset()

        # Create the handshake to send to the server

        m1 = self.__authenticator.handshake(False)

        m1.write_bytes(self.__server)

        # Receive and solve challenge from server

        m2 = Message.read_bytes(self.__server)

        ch1 = Challenge.from_bytes(m2.get_data())

        k1 = self.__authenticator.solve_challenge(ch1)

        # Create challenge for server

        k2, ch2 = self.__authenticator.generate_challenge(True, ch1.get_set())

        m3 = self.__authenticator.handshake(True, k1, ch1.get_chal(), ch2)

        m3.write_bytes(self.__server)

        # Receive solution from server

        m4 = Message.read_bytes(self.__server)

        self.__authenticator.check_handshake(m4)

        data = decrypt(m4.get_data(), k2)

        if not ch2.verify(data[0:CHALLENGE_SIZE]):
            raise InvalidCommParameters()

        self.__authenticator.feed_key(data[CHALLENGE_SIZE:CHALLENGE_SIZE + KEY_LENGTH])

    def run(self) -> None:
        '''
        Runs one single execution of the functioning loop.

        Returns:
            None: The execution is runned.
        '''
    

        try:

            while True:

                # Authenticate the device

                if self.__authenticator is None or self.__authenticator.time_lived() == TIME_TO_LIVE:

                    self.__authenticate()

                # Generate the sensor data

                sleep(3)

                self.__controller.change_state()

                data = self.__controller.read_device_bytes(None)

                # Send sensor data to the server

                self.__send_sv(data)

        except Exception:

            print('Lost connection to the server!')

        finally:
            
            self.close()

    def close(self) -> None:
        '''
        Closes the IoT device functioning.

        Returns:
            None: Finalizes the device functioning.
        '''

        self.__server.close()
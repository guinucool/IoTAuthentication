from authenticator import Authenticator
from controller import Controller
from copy import deepcopy
from communications import IOTDeviceCommunicator

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

            self.__server = IOTDeviceCommunicator(sv_addr, sv_port)
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
        self.__server.send(data)
        print(f"Sent {data} to server")
        
    def __recv_sv(self) -> bytes:
        '''
        Receives information from the server.

        Returns:
            bytes: The information received
        '''
        data = self.__server.recv()
        print(f"Received {data} from server")
        return data


    def __authenticate(self) -> None:
        '''
        Authenticates the server and itself, agreeing on a shared key.

        Returns:
            None: The authentication is sucessful and the key is agreed.
        '''
        pass

    def run(self) -> None:
        '''
        Runs one single execution of the functioning loop.

        Returns:
            None: The execution is runned.
        '''
        pass
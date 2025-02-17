from socket import socket

class Message:
    '''
    A class representing a message to be exchanged in communications.

    Attributes:
        __deviceId (int): The identifier of the device that sent the message.
        __sessionId (int): The identifier associated with the session where the message is being exchanged.
        __type (bytes): The byte to identify the purpose of the message.
        __data (bytes): The data that will be transmited with this message.
    '''

    def __init__(self, device_id: int, session_id: int, type: bytes, data: bytes):
        '''
        Initializes a Message object.
        
        Args:
            device_id (int): The identifier of the device.
            session_id (int): The identifier associated with the session.
            type (bytes): The purpose of the message.
            data (bytes): The data to be transmitted.
        '''
        self.__deviceId = device_id
        self.__sessionId = session_id
        self.__type = type
        self.__data = data

    def get_deviceId(self) -> int:
        '''
        Returns the device identifier.
        
        Returns:
            int: The device identifier.
        '''
        return self.__deviceId

    def get_sessionId(self) -> int:
        '''
        Returns the session identifier.
        
        Returns:
            int: The session identifier.
        '''
        return self.__sessionId
    
    def get_type(self) -> bytes:
        '''
        Returns the type purpose.
        
        Returns:
            bytes: The type purpose.
        '''
        return self.__type
    
    def get_data(self) -> bytes:
        '''
        Returns the message data.
        
        Returns:
            bytes: The data of the message.
        '''
        return self.__data
    
    def get_dataLength(self) -> int:
        '''
        Returns the length of the message data.
        
        Returns:
            int: The length of the data.
        '''
        return len(self.__data)
    
    def write_bytes(self, conn: socket) -> None:
        '''
        Writes the message into the connection socket.

        Returns:
            None: The data is written in the socket.

        Raises:
            ConnectionResetError: In case communication fails.
            BrokenPipeError: In case communication fails.
        '''

        # Write the header

        conn.sendall(self.__deviceId.to_bytes(4, 'little'))
        conn.sendall(self.__sessionId.to_bytes(4, 'little'))
        conn.sendall(self.__type)

        # Write the data

        conn.sendall(self.get_dataLength().to_bytes(4, 'little'))
        conn.sendall(self.__data)

    @classmethod
    def read_bytes(cls, conn: socket):
        '''
        Reads a message from a connection socket.

        Raises:
            ConnectionResetError: In case communication fails.
            BrokenPipeError: In case communication fails.
        '''
    
        # Read the header

        device_id = int.from_bytes(conn.recv(4), 'little')
        session_id = int.from_bytes(conn.recv(4), 'little')
        type = conn.recv(1)

        # Read the data

        length = int.from_bytes(conn.recv(4), 'little')
        data = conn.recv(length)

        # Create the message object

        return Message(device_id, session_id, type, data)
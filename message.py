class Message:
    '''
    A class representing a message to be exchanged in communications.

    Attributes:
        __sessionId (int): The identifier associated with the session where the message is being exchanged
        __data (bytes): The data that will be transmited with this message
    '''

    def __init__(self, session_id: int, data: bytes):
        '''
        Initializes a Message object.
        
        Args:
            session_id (int): The identifier associated with the session.
            data (bytes): The data to be transmitted.
        '''
        self.__sessionId = session_id
        self.__data = data

    def get_sessionId(self) -> int:
        '''
        Returns the session identifier.
        
        Returns:
            int: The session identifier.
        '''
        return self.__sessionId
    
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
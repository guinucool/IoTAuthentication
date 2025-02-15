from message import Message


class Handler:
    def __init__(handler, DB, request, device_id, session_id, sensors, timestamp):
        handler.DB = DB
        handler.request = request
        handler.device_id = device_id
        handler.session_id = session_id
        handler.sensors = sensors
        handler.timestamp = timestamp


    def handleMessage(handler):
        '''
        Handles the received message. This message can be an Authentication message or an Information msg
        Depending on the received message a determined action will occur
        '''
        if self.request.get("type") == "authentication":
            return self.handle_authentication()
        elif self.request.get("type") == "information":
            return self.handle_information()
        else:
            return {"status": "error", "message": "Invalid message type"}
        

    def handle_authentication(self):
        '''
        (?)
        '''


    def handle_information(self):
        '''
        (?)
        '''
        

    def __check_session_id(handler, session_id: int) -> bool:
        '''
        Checks if the given identifier is the one supposed to be received in a message.

        Args:
            device_id (int): The identifier to check.

        Returns:
            bool: The result of checking.
        '''


    def __check_device_id(handler, device_id: int) -> bool:
        '''
        Checks if the given identifier is the one supposed to be received in a message.

        Args:
            session_id (int): The identifier to check.

        Returns:
            bool: The result of checking.
        '''

    def __store_data(handler):
        '''
        Stores sensor data in the database.
        '''


    class DB:
        def __init__(self):
            '''
                Initializes the DataBase Object.

                Args:
                    devices (int): The identifier of the device the authenticator keeps track of.
                    sessions (int): The identifier of the session the authenticator keeps track of.
                    sensors(?)
            '''
           
        
        


        
        def 

        

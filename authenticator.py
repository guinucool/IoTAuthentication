from crypto import encrypt, decrypt, hmac, generate_key
from utils import write_file_bytes, read_file_bytes, xor, bytes_list_to_bytes
from challenge import Challenge
from message import Message

PATH_DV_VAULTS = 'dvVaults/'
PATH_SV_VAULTS = 'svVaults/'
PATH_DV_KEYS = 'dvKeys/'

KEY_LENGTH = 32 # In bytes
TIME_TO_LIVE = 9 # In messages

class InvalidCommParameters(Exception):
    pass

class Authenticator:
    '''
    A class representing the authenticator, which is responsible of ensuring the authentication of message exchange.

    Attributes:
        __deviceId (int): The unique identifier of the IoT device.
        __vault (list): The vault of keys available of the session being monitored.
        __vaultKey (bytes): The key to the encrypted vault.
        __sessionId (int): The identifier that identifies the session is being monitored.
        __sessionKey (bytes): The generated session key.
        __sessionData (list): The list of data exchanged during the session.
    '''

    def __init__(self, device_id: int, device: bool, session_id: int = 0):
        '''
        Initializes the Authenticator Object.

        Args:
            device_id (int): The identifier of the device the authenticator keeps track of.
            device (bool): Checks if the authenticator is from a device or a server.
            session_id (int): The identifier of the session the authenticator keeps track of.
        '''

        # Attributes to be kept in memory

        self.__deviceId = device_id
        self.__vault = list()
        self.__vaultKey = None

        if (device):
            self.__vaultKey = read_file_bytes(PATH_DV_KEYS + str(self.__deviceId))

        self.__read_vault()

        # Session attributes
        self.__sessionId = session_id
        self.__sessionKey = generate_key(KEY_LENGTH)
        self.__sessionData = list()

    def __read_vault(self) -> None:
        '''
        Reads and stores the vault keys of a certain device identifier.

        Returns:
            None -> The values are stored inside the attributes.
        '''

        # Fetch the keys from the vault file
        
        if self.__vaultKey is None:

            path = PATH_SV_VAULTS + str(self.__deviceId)

            vault = read_file_bytes(path)

        else:

            path = PATH_DV_VAULTS + str(self.__deviceId)

            encrypted = read_file_bytes(path)

            # Decrypt the read vault

            vault = decrypt(encrypted, self.__vaultKey)

        # Read the keys from the vault

        n_keys = len(vault) // KEY_LENGTH

        self.__vault = [vault[i * KEY_LENGTH: (i + 1) * KEY_LENGTH] for i in range(n_keys)]

    def __write_vault(self) -> None:
        '''
        Writes and stores the current keys in the vault.

        Returns:
            None -> The values are stored in the vault.
        '''

        # Choose a path and prepare the information to be written in the file
        
        if self.__vaultKey is None:

            path = PATH_SV_VAULTS + str(self.__deviceId)

            vault = bytes()

            for key in self.__vault:

                vault += key

        else:

            path = PATH_DV_VAULTS + str(self.__deviceId)

            tmp = bytes()

            for key in self.__vault:

                tmp += key

            # Encrypt the information

            vault = encrypt(tmp, self.__vaultKey)

        # Write the vault into the desired file

        write_file_bytes(vault, path)

    def __check_device_id(self, device_id: int) -> bool:
        '''
        Checks if the given identifier is the one supposed to be received in a message.

        Args:
            device_id (int): The identifier to check.

        Returns:
            bool: The result of checking.
        '''

        return (self.__vaultKey is None and device_id == self.__deviceId) or (device_id == 0 and self.__vaultKey is not None)
    
    def __check_session_id(self, session_id: int) -> bool:
        '''
        Checks if the given identifier is the one supposed to be received in a message.

        Args:
            session_id (int): The identifier to check.

        Returns:
            bool: The result of checking.
        '''

        return session_id == self.__sessionId

    def generate_challenge(self, t_key: bool, restriction: list = None) -> tuple[bytes, Challenge]:
        '''
        Generates a challenge to be solved based on the current vault.

        Args:
            t_key (bool): Decides if the challenge will take into consideration the session key.
            restriction (list) = None: Decides if the challenge has a restriction.

        Returns:
            tuple[bytes, Challenge]: The challenge to be sent and the respective solution.
        '''
        
        # Generates a challenge

        challenge = Challenge(len(self.__vault), restriction)

        # Solve the challenge and append the t_key (if appliable)

        solution = challenge.solve(self.__vault)

        if t_key:

            solution = xor(solution, self.__sessionKey)

        # Return the challenge and solution

        return (solution, challenge)

    def solve_challenge(self, challenge: Challenge, t_key: bytes = None) -> bytes:
        '''
        Solves a challenge based on the current vault.

        Args:
            challenge (Challenge): The challenge to solve.
            t_key (bytes) = None: The session key to xor.

        Returns:
            bytes: The solution to the given challenge.
        '''

        # Solve the challenge with the given parameters
        
        solution = challenge.solve(self.__vault)

        if t_key is not None:

            solution = xor(solution, t_key)

        return solution

    def handshake(self, t_key: bool, key: bytes = None, answer: bytes = None, challenge: Challenge = None) -> Message:
        '''
        Creates an handshake message with the given parameters and current session attributes.

        Args:
            t_key (bool): If the session key should or not be appended.
            key (bytes) = None: Encryption key.
            answer (bytes) = None: The answer to a challenge.
            challenge (Challenge) = None: A challenge to be solved.

        Returns:
            Message: The created handshake message.
        '''

        # Create a data placeholder

        data = bytes()

        # Append the answer (if appliable)

        if answer is not None:

            data += answer

        # Append the session key (if appliable)

        if t_key:

            data += self.__sessionKey

        # Append the challenge (if appliable)

        if challenge is not None:

            data += challenge.to_bytes()

        # Encrypt the information (if appliable)

        if key is not None:

            data = encrypt(data, key)

        # Build the message frame

        return Message(self.__deviceId, self.__sessionId, b'0', data)
    
    def check_handshake(self, hd_msg: Message) -> bool:
        '''
        Checks if the attributes of a handshake message are valid.

        Args:
            hd_msg (Messsage): The handshake message.

        Returns:
            bool: The correctness of the handshake message.
        '''

        return self.__check_device_id(hd_msg.get_deviceId()) and self.__check_session_id(hd_msg.get_sessionId()) and hd_msg.get_type() == b'0'
    
    def feed_key(self, t_key: bytes) -> None:
        '''
        Feeds the received key to the current session key.

        Args:
            t_key (bytes): The key received.

        Returns:
            None: The key gets updated.
        '''

        self.__sessionKey = xor(self.__sessionKey, t_key)

    def encrypt(self, data: bytes) -> Message:
        '''
        Encrypts and authenticates a message to be sent.

        Args:
            data (bytes): The content of the message to be sent.

        Returns:
            Message: The structured message, ready to be sent.
        '''

        # Add the data to the data exchanged list

        self.__sessionData.append(data)

        # Encrypt the data and create the message

        enc = encrypt(data, self.__sessionKey)

        return Message(self.__deviceId, self.__sessionId, b'1', enc)

    def decrypt(self, msg: Message) -> bytes:
        '''
        Decrypts and checks the authenticy of a message received.

        Args:
            msg (Message): The message received.

        Returns:
            bytes: The plain data contained in the message.

        Raises:
            InvalidTag: If decryption fails due to authentication failure.
        '''

        # Check message values

        if not (self.__check_device_id(msg.get_deviceId()) and self.__check_session_id(msg.get_sessionId()) and msg.get_type() == b'1'):
            raise InvalidCommParameters()

        # Decrypt the data received from the message

        data = decrypt(msg.get_data(), self.__sessionKey)

        # Add the data to the data list and return it

        self.__sessionData.append(data)

        return data
    
    def time_lived(self) -> int:
        '''
        Calculates the time this session has been alive in terms of messages exchanged.

        Returns:
            int: Number of messages exchanged.
        '''

        return len(self.__sessionData)
    
    def reset(self) -> None:
        '''
        Resets the authenticator for a new session.

        Returns:
            None: The authenticator gets reset.
        '''

        # Convert the data into a 32 bytes stream

        stream = bytes_list_to_bytes(self.__sessionData)
        key = stream

        if len(key) < 32:

            key += stream

        key = key[0:KEY_LENGTH]

        # Convert the current vault into a bytes stream

        vault = bytes_list_to_bytes(self.__vault)

        # Hash the current vault

        hash = hmac(vault, key)

        # Update the vault

        for key in self.__vault:

            key = xor(key, hash)

        self.__write_vault()

        # Reset the session

        self.__sessionId += 1
        self.__sessionKey = generate_key(KEY_LENGTH)
        self.__sessionData = list()
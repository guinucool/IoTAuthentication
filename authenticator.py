from crypto import encrypt, decrypt, hmac, generate_key
from utils import write_file_bytes, read_file_bytes

PATH_DV_VAULTS = 'dvVaults/'
PATH_SV_VAULTS = 'svVaults/'
PATH_DV_KEYS = 'dvKeys/'

KEY_LENGTH = 32 # In bytes

class Authenticator:
    '''
    A class representing the authenticator, which is responsible of ensuring the authentication of message exchange.

    Attributes:
        __deviceId (int): The unique identifier of the IoT device.
        __sessionId (int): The identifier that identifies the session is being monitored.
        __vault (list): The vault of keys available of the session being monitored.
        __vaultKey (bytes): The key to the encrypted vault.
        __authKey (bytes): The generated key for authentication.
        __sessionKey (bytes): The generated session key.
        __r (int): The random number generated to be used as the challenge.
    '''

    def __init__(self):
        pass

    def __readVault(self) -> None:
        '''
        Reads and stores the vault keys of a certain device identifier.

        Returns:
            None -> The values are stored inside the attributes.
        '''

        # Fetch the keys from the vault file
        
        if self.__key is None:

            path = PATH_SV_VAULTS + self.__deviceId

            vault = read_file_bytes(path)

        else:

            path = PATH_DV_VAULTS + self.__deviceId

            encrypted = read_file_bytes(path)

            # Decrypt the read vault

            vault = decrypt(encrypted[12:], self.__vaultKey, encrypted[0:12])

        # Read the keys from the vault

        n_keys = len(vault) // KEY_LENGTH

        self.__vault = [vault[i * KEY_LENGTH: (i + 1) * KEY_LENGTH] for i in range(n_keys)]

    def __writeVault(self) -> None:
        '''
        Writes and stores the current keys in the vault.

        Returns:
            None -> The values are stored in the vault.
        '''

        # Choose a path and prepare the information to be written in the file
        
        if self.__key is None:

            path = PATH_SV_VAULTS + self.__deviceId

            vault = bytes()

            for key in self.__vault:

                vault += key

        else:

            path = PATH_DV_VAULTS + self.__deviceId

            tmp = bytes()

            for key in self.__vault:

                tmp += key

            # Encrypt the information

            vault = encrypt(tmp, self.__vaultKey)

        # Write the vault into the desired file

        write_file_bytes(vault, path)
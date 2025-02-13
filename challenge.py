from utils import xor
import os, random

CHALLENGE_SIZE = 12

class Challenge:
    '''
    A class representing an authentication challenge.

    Attributes:
        __keySet (list): The set of keys for the challenge.
        __chal (bytes): The numeric challenge.
    '''

    def __init__(self, n_keys: int, restriction: list = None):
        '''
        Initializes the challenge.

        Args:
            n_keys (int): Number of keys in the vault associated.
            restriction (list) = None: A set that this challenge can't be equal to.
        '''

        self.__keySet = list()
        self.__chal = os.urandom(CHALLENGE_SIZE)

        self.__generate_set(n_keys, restriction)


    def __generate_set(self, n_keys: int, restriction: list = None) -> None:
        '''
        Generates the keyset for the challenge.

        Args:
            n_keys (int): Number of keys in the vault associated.
            restriction (list) = None: A set that this challenge can't be equal to.

        Returns:
            None: The set is associated with the challenge.
        '''
        
        # Generate the set size

        set_size = random.randint(1, n_keys)

        # Generate the key set

        for i in range(set_size):

            self.__keySet.append(random.randint(0, n_keys - 1))

        # Check if the set collides with the restriction
        
        if restriction is not None and self.__keySet == restriction:

            self.__keySet = list()

            self.__generate_set()

    def get_set(self) -> list:
        '''
        Returns the set of keys.

        Returns:
            list: The set of keys.
        '''
        
        return self.__keySet

    def get_chal(self) -> bytes:
        '''
        Returns the challenge number.

        Returns:
            bytes: The challenge number.
        '''
        
        return self.__Chal

    def solve(self, vault: list) -> bytes:
        '''
        Solves the challenge with the associated vault.

        Args:
            vault (list): The associated vault.

        Returns:
            bytes: The solution to the challenge.
        '''
        
        # XOR all the chosen keys of the vault

        key = vault[self.__keySet[0]]

        for i in self.__keySet[1:]:

            key = xor(key, vault[i])

        return key

    def verify(self, chal: bytes) -> bool:
        '''
        Checks if the solution to the challenge is correct.

        Args:
            chal (bytes): The solution.

        Returns:
            bool: The confirmation of correctness.
        '''
        
        return self.__chal == chal
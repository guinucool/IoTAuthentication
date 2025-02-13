def read_file_bytes(path: str) -> bytes:
    '''
    Reads the bynary information of a file given its path.

    Args:
        path (str): The path of the file desired for reading.

    Return:
        bytes: The data read from the file.
    '''

    # Read the binary information from the file descriptor

    file = open(path, 'rb')

    data = file.read()

    file.close()

    return data

def write_file_bytes(data: bytes, path: str) -> None:
    '''
    Writes bynary information to a file given its path.

    Args:
        data (bytes): The binary information for writing.
        path (str): The path of the file desired for writing.

    Return:
        None: The data is written on the file.
    '''

    # Read the binary information from the file descriptor

    file = open(path, 'wb')

    file.write(data)

    file.close()

def xor(a: bytes, b: bytes) -> bytes:
    '''
    Does the XOR operation on the given data, assuming they have the same length

    Args:
        a (bytes): First data.
        b (bytes): Second data.
    '''

    xor = []

    for i in range(len(a)):

        xor.append(a[i] ^ b[i])

    return bytes(xor)

def bytes_list_to_bytes(data: list) -> bytes:
    '''
    Converts a list of bytes into a single bytes object.

    Args:
        data (list): The list of bytes.

    Returns:
        bytes: The converted list.
    '''

    final = bytes()

    for info in data:

        final += info

    return final
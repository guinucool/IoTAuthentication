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
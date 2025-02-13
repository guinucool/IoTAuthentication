from utils import write_file_bytes, read_file_bytes, bytes_list_to_bytes
from crypto import generate_keys, generate_key, encrypt
import random

VAULT_SIZE = 128
KEY_SIZE = 32

PATH_DV_VAULTS = 'dvVaults/'
PATH_SV_VAULTS = 'svVaults/'
PATH_DV_KEYS = 'dvKeys/'

# The running script to generate an IoT device configuration (server and device wise)

# Generate a device id

dev_id = random.randint(1, 10000)

# Generate the vault and the device key

vault = generate_keys(VAULT_SIZE, KEY_SIZE)
key = generate_key(KEY_SIZE)

data = bytes_list_to_bytes(vault)

# Write the information to be used

write_file_bytes(data, PATH_SV_VAULTS + str(dev_id))
write_file_bytes(key, PATH_DV_KEYS + str(dev_id))
write_file_bytes(encrypt(data, key), PATH_DV_VAULTS + str(dev_id))
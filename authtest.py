from authenticator import Authenticator, KEY_LENGTH
from challenge import Challenge, CHALLENGE_SIZE
from message import Message
from crypto import decrypt

dv = Authenticator(1058, True) # No error

msg = dv.handshake(False) # No error

# Check if device has running session

sv = Authenticator(msg.get_deviceId(), False, msg.get_sessionId()) # No error

key, csv = sv.generate_challenge(False) # No error

m2 = sv.handshake(False, challenge = csv) # No error

# Check if received message is in expected format (type = 0, only challenge, from device_id = 0 and from current session)

rchsv = Challenge.from_bytes(m2.get_data()) # Check if information is convertable to bytes and is a real challenge

k1 = dv.solve_challenge(rchsv) # No error

dvkey, cdv = dv.generate_challenge(True, rchsv.get_set()) # No error

m3 = dv.handshake(True, k1, rchsv.get_chal(), cdv) # No error

# Check if received message is in expected format (type = 0, from device_id and from current session)

data = decrypt(m3.get_data(), key) # Check if decryption is authentic

# Check if CHALLENGE AND KEY are correct size

solving = Challenge.from_bytes(data[CHALLENGE_SIZE+KEY_LENGTH:]) # Check if information is convertable to bytes and is a real challenge

# Check if CHALLENGE is correct
if csv.verify(data[0:CHALLENGE_SIZE]):
    print("Verified")

t1 = data[CHALLENGE_SIZE:CHALLENGE_SIZE + KEY_LENGTH]

k2 = sv.solve_challenge(solving, t1)

m4 = sv.handshake(True, k2, solving.get_chal())

sv.feed_key(t1)

# Check if received message is in expected format (type = 0, from device_id = 0 and from current session)

data2 = decrypt(m4.get_data(), dvkey) # Check if decryption is authentic

# Check if CHALLENGE AND KEY are correct size

# Check if CHALLENGE is correct
print(cdv.verify(data2[0:CHALLENGE_SIZE]))

dv.feed_key(data2[CHALLENGE_SIZE:CHALLENGE_SIZE + KEY_LENGTH])


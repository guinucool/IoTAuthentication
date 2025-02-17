from handler import Handler
from config_dv import thermo, assist
from threading import Thread

# Start server

sv = Handler({1058: {'auth': None, 'controller': thermo}, 5953: {'auth': None, 'controller': assist}}, 'localhost', 9080)

sv_th = Thread(target=sv.run_server)
sv_th.start()

# Control terminal

while True:

    # Filters for device and session id

    did = None
    sid = None

    # Prompt for filtering

    exit = input('Exit? ')

    device_id = input('Device Id: ')

    session_id = input('Session Id: ')

    # Check for program exit

    if exit == 'Y':

        break

    # Conversion of the filtering

    if device_id.isdigit() and len(device_id) > 0:

        did = int(device_id)

    if session_id.isdigit() and len(session_id) > 0:

        sid = int(session_id)

    # Show the database with the filters

    sv.show_db(did, sid)

# Close server

sv.close()
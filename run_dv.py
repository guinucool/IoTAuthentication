from device import Device
from config_dv import thermo, assist
from threading import Thread

t_dv = Device('localhost', 9080, 1058, thermo)
a_dv = Device('localhost', 9080, 5953, assist)

t_th = Thread(target=t_dv.run)
a_th = Thread(target=a_dv.run)

t_th.start()
a_th.start()

try:

    while True:
        pass

except KeyboardInterrupt:

    t_dv.close()
    a_dv.close()

finally:

    t_th.join()
    a_th.join()
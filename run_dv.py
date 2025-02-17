from device import Device
from config_dv import thermo, assist, rand
from threading import Thread

t_dv = Device('localhost', 9096, 1058, thermo)
#a_dv = Device('localhost', 9093, 5953, assist)
#r_dv = Device('localhost', 9093, 6718, rand)

t_th = Thread(target=t_dv.run)
#a_th = Thread(target=a_dv.run)
#r_th = Thread(target=r_dv.run)

t_th.start()
#a_th.start()
#r_th.start()

try:

    while True:
        pass

except KeyboardInterrupt:

    t_dv.close()
    #a_dv.close()
    #r_dv.close()

finally:

    t_th.join()
    #a_th.join()
    #r_th.join()
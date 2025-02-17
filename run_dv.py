from device import Device
from config_dv import thermo, assist, rand
from threading import Thread

t_dv = Device('localhost', 9090, 1058, thermo)
a_dv = Device('localhost', 9090, 5953, assist)
r_dv = Device('localhost', 9090, 6718, rand)

#MUDAR ID AUTHENTICATOR SV

t_th = Thread(target=t_dv.run())
a_th = Thread(target=a_dv.run())
r_th = Thread(target=r_dv.run())

t_th.start()
a_th.start()
r_th.start()

t_th.join()
a_th.join()
r_th.join()
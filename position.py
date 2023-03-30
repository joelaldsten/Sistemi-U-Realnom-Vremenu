import cflib.crazyflie
import cflib.positioning.position_hl_commander
from cflib.utils import uri_helper
import time

cf = Crazyflie(rw_cache='./cache')
link_uri = uri_helper.uri_from_env(default='usb://0')
cf.open_link(link_uri)
pos = PositionHlCommander(cf)

while True:
    print(pos.get_position())
    time.sleep(0.1)

import time

from .sensors.pa1010d import PA1010D

class Latlong:

    def run(self):
        gps = PA1010D()

        while True:
            result = gps.update()
            if result:
                print("""
T: {timestamp}
N: {latitude}
E: {longitude}
Alt: {altitude}
Sats: {num_sats}
Qual: {gps_qual}
Speed: {speed_over_ground}
Fix Type: {mode_fix_type}
PDOP: {pdop}
VDOP: {vdop}
HDOP: {hdop}
""".format(**gps.data))
            time.sleep(1.0)
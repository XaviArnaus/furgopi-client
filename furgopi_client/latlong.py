import time

from .entities.gps_entity import GpsEntity
from .sensors.pa1010d import PA1010D

class Latlong:

    LOOP_SLEEP = 1.0
    gps = None  

    def __init__(self) -> None:
        self.gps = PA1010D()

    def loop(self):
        while True:
            self.run()
            time.sleep(self.LOOP_SLEEP)

    def run(self):
        
        datapoint = self.get_data()
        print(datapoint.to_string())
                
    def get_data(self):
        result = self.gps.update()
        if result:
            return GpsEntity.from_dict({
                "timestamp": result.timestamp,
                "latitude": result.latitude,
                "longitude": result.longitude,
                "altitude": result.altitude,
                "num_sats": result.num_sats,
                "gps_qual": result.gps_qual,
                "speed_over_ground": result.speed_over_ground,
                "mode_fix_type": result.mode_fix_type,
                "pdop": result.pdop,
                "vdop": result.vdop,
                "hdop": result.hdop
            })
        else:
            return None
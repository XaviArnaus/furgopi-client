from .entities.gps_entity import GpsEntity
from .sensors.pa1010d import PA1010D

class GpsRunner:

    gps = None  

    def __init__(self) -> None:
        self.gps = PA1010D()

    def run(self) -> GpsEntity:
        result = self.gps.update()
        if result:
            return GpsEntity.from_dict(self.gps.data)
        else:
            return None
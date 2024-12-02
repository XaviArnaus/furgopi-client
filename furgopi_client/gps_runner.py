from datetime import datetime, timezone

from .entities.gps_entity import GpsEntity
from .sensors.pa1010d import PA1010D

class GpsRunner:

    gps = None  

    def __init__(self) -> None:
        self.gps = PA1010D()

    def run(self) -> GpsEntity:
        result = self.gps.update()
        if result:
            data = self.gps.data
            today = datetime.now(tz=timezone.utc)
            faking_datetime = f"{today.year}-{today.month}-{today.day} {data['timestamp']}"
            data = {
		**data,
                **{"timestamp": datetime.strptime(faking_datetime, "%Y-%m-%d %H:%M:%S%z").astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}
            }
            return GpsEntity.from_dict(data)
        else:
            return None

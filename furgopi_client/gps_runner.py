from datetime import datetime, timezone
from pyxavi.terminal_color import TerminalColor

from .entities.gps_entity import GpsEntity
from .sensors.pa1010d import PA1010D

class GpsRunner:

    gps = None  

    def __init__(self) -> None:
        try:
            self.gps = PA1010D()
        except FileNotFoundError:
            print(TerminalColor.RED_BRIGHT + "No GPS sensor" + TerminalColor.END)

    def run(self) -> GpsEntity:
        if self.gps is None:
            return None
        try:
            result = self.gps.update()
        except OSError:
            return None

        if result:
            data = self.gps.data
            if data['timestamp'] is None:
                return None
            today = datetime.now(tz=timezone.utc)
            faking_datetime = f"{today.year}-{today.month}-{today.day} {data['timestamp']}"
            data = {
		**data,
                **{"timestamp": datetime.strptime(faking_datetime, "%Y-%m-%d %H:%M:%S%z").astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}
            }
            return GpsEntity.from_dict(data)
        else:
            return None

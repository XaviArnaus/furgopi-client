from datetime import datetime

from .entities.temp_entity import TempEntity
from .sensors.ds18b20 import DS18B20

class TemperatureRunner:

	devices = None

	def __init__(self) -> None:
		self.devices = DS18B20()

	def run(self) -> list|TempEntity:

		count = self.devices.device_count()
		names = self.devices.device_names()

		result = []
		for idx in range(0, count):
			result.append(TempEntity(
				timestamp=datetime.utcnow(),
				celsius_value=self.devices.tempC(idx),
				device_id=names[idx] if len(names) >= idx+1 else f"UNKNOWN {idx}"
			))

		if len(result) == 1:
			return result[0]
		elif len(result) == 0:
			return None
		else:
			return result

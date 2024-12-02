from .base_entity import BaseEntity

class TempEntity(BaseEntity):

    DEGREE_SIGN = u'\xb0'

    timestamp = None,
    celsius_value = None,
    device_id = None,

    def __init__(
            self,
            timestamp = None,
            celsius_value = None,
            device_id = None,
            ) -> None:
        
        self.timestamp = timestamp
        self.celsius_value = celsius_value
        self.device_id = device_id

        super().__init__()
    
    @property
    def name(self):
        return self.device_id

    def to_string(self):
        return f"timestamp: {self.timestamp}\n" +\
                f"celsius_value: {self.celsius_value}{self.DEGREE_SIGN}C\n" +\
                f"device_id: {self.device_id}\n"
    
    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "celsius_value": self.celsius_value,
            "device_id": self.device_id
        }

    @staticmethod
    def from_dict(dictionary: dict):
        return TempEntity(
            timestamp = dictionary["timestamp"] if "timestamp" in dictionary else None,
            celsius_value = dictionary["celsius_value"] if "celsius_value" in dictionary else None,
            device_id = dictionary["device_id"] if "device_id" in dictionary else None,
        )

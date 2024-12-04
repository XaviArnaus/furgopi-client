from .base_entity import BaseEntity

class GpsEntity(BaseEntity):

    NAME = "GPS"

    timestamp = None,
    latitude = None,
    longitude = None,
    altitude = None,
    num_sats = None,
    gps_qual = None,
    lat_dir = None,
    lon_dir = None,
    geo_sep = None,
    pdop = None,
    hdop = None,
    vdop = None,
    speed_over_ground = None,
    mode_fix_type = None

    def __init__(
            self,
            timestamp = None,
            latitude = None,
            longitude = None,
            altitude = None,
            num_sats = None,
            gps_qual = None,
            lat_dir = None,
            lon_dir = None,
            geo_sep = None,
            pdop = None,
            hdop = None,
            vdop = None,
            speed_over_ground = None,
            mode_fix_type = None,
            ) -> None:
        
        self.timestamp = timestamp
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.num_sats = num_sats
        self.gps_qual = gps_qual
        self.assign_sign_to_latitude_from_direction(lat_dir)
        self.assign_sign_to_longitude_from_direction(lon_dir)
        self.geo_sep = geo_sep
        self.pdop = pdop
        self.hdop = hdop
        self.vdop = vdop
        self.speed_over_ground = speed_over_ground
        self.mode_fix_type = mode_fix_type

        super().__init__()
    
    @property
    def name(self):
        return self.NAME
    
    def assign_sign_to_latitude_from_direction(self, lat_dir: str):
        if (lat_dir.lower() == "s"):
            self.latitude = self.latitude * -1
    
    def assign_sign_to_longitude_from_direction(self, lon_dir: str):
        if (lon_dir.lower() == "w"):
            self.longitude = self.longitude * -1

    def to_string(self):
        return f"timestamp: {self.timestamp}\n" +\
                f"name: {self.name}\n" +\
                f"latitude: {self.latitude}\n" +\
                f"longitude: {self.longitude}\n" +\
                f"altitude: {self.altitude}\n" +\
                f"num_sats: {self.num_sats}\n" +\
                f"gps_qual: {self.gps_qual}\n" +\
                f"geo_sep: {self.geo_sep}\n" +\
                f"speed_over_ground: {self.speed_over_ground}\n" +\
                f"mode_fix_type: {self.mode_fix_type}\n" +\
                f"pdop: {self.pdop}\n" +\
                f"vdop: {self.vdop}\n" +\
                f"hdop: {self.hdop}\n"
    
    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "altitude": self.altitude,
            "num_sats": self.num_sats,
            "gps_qual": self.gps_qual,
            "geo_sep": self.geo_sep,
            "pdop": self.pdop,
            "hdop": self.hdop,
            "vdop": self.vdop,
            "speed_over_ground": self.speed_over_ground,
            "mode_fix_type": self.mode_fix_type
        }

    @staticmethod
    def from_dict(dictionary: dict):
        return GpsEntity(
            timestamp = dictionary["timestamp"] if "timestamp" in dictionary else None,
            latitude = dictionary["latitude"] if "latitude" in dictionary else None,
            longitude = dictionary["longitude"] if "longitude" in dictionary else None,
            altitude = dictionary["altitude"] if "altitude" in dictionary else None,
            num_sats = dictionary["num_sats"] if "num_sats" in dictionary else None,
            gps_qual = dictionary["gps_qual"] if "gps_qual" in dictionary else None,
            lat_dir = dictionary["lat_dir"] if "lat_dir" in dictionary\
                        else "s" if "latitude" in dictionary and dictionary["latitude"] < 0 else "n",
            lon_dir = dictionary["lon_dir"] if "lon_dir" in dictionary\
                        else "w" if "longitude" in dictionary and dictionary["longitude"] < 0 else "e",
            geo_sep = dictionary["geo_sep"] if "geo_sep" in dictionary else None,
            pdop = dictionary["pdop"] if "pdop" in dictionary else None,
            hdop = dictionary["hdop"] if "hdop" in dictionary else None,
            vdop = dictionary["vdop"] if "vdop" in dictionary else None,
            speed_over_ground = dictionary["speed_over_ground"] if "speed_over_ground" in dictionary else None,
            mode_fix_type = dictionary["mode_fix_type"] if "mode_fix_type" in dictionary else None
        )

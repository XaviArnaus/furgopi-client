import time
import sys
import os
from pathlib import Path

from pyxavi.terminal_color import TerminalColor
from pyxavi.debugger import full_stack
from pyxavi.config import Config

from furgopi_client.entities.base_entity import BaseEntity
from furgopi_client.temperature_runner import TemperatureRunner
from furgopi_client.gps_runner import GpsRunner

LOOP_SLEEP = 1.0
CONFIG_FILENAME = "config/main.yaml"
CSV_SEPARATOR = ";"

runners = {
    "gps": {
        "runner": GpsRunner(),
        "fields": {
            "timestamp": "timestamp",
            "latitude": "latitude",
            "longitude": "longitude",
            "altitude": "altitude",
            "speed_over_ground": "speed"
        }
    },
    "temperature": {
        "runner": TemperatureRunner(),
        "fields": {
            "timestamp": "timestamp",
            "celsius_value": "temperature"
        }
    }
}

def run():
    try:
        for sensor, params in runners.items():

            print("\n" + TerminalColor.BLUE_BRIGHT + f"Processing runner {sensor}" + TerminalColor.END)

            read = params["runner"].run()

            if read is None:
                print(f"No datapoint from the {sensor} sensor")
                continue
            elif isinstance(read, BaseEntity):
                read = [read]
            
            for datapoint in read:
                filename = f"{datapoint.name}.csv"
                _export_datapoint_to_csv(datapoint, params["fields"], filename)
                print(TerminalColor.BLUE_BRIGHT + f"Wrote filename {filename}" + TerminalColor.END)
            
        print("\n" + TerminalColor.GREEN_BRIGHT + "End" + TerminalColor.END + "\n")

    except RuntimeError as e:
        print(TerminalColor.RED_BRIGHT + str(e) + TerminalColor.END)
    except Exception:
        print(full_stack())

def loop():
    try:
        print("[press ctrl+c to end the loop]\n")
        while True:
            run()
            time.sleep(LOOP_SLEEP)
    except KeyboardInterrupt:
        print('good bye')
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)

def _export_datapoint_to_csv(datapoint: BaseEntity, fields_map: dict, filename: str):
    file_path = Path(Config(CONFIG_FILENAME).get("datapoints.path") + filename)

    # If the file does not exist, first of all write the header with the target fields
    if not file_path.exists():
        fields_list = [f"\"{field}\"" for field in fields_map.values()]
        with open(file_path, "w") as file:
            file.write(f"{CSV_SEPARATOR}".join(fields_list) + "\n")
    
    # Now write the current datapoint. Filter here only the wanted fields.
    line = []
    for key, value in datapoint.to_dict().items():
        if key in fields_map.keys():
            line.append(f"\"{value}\"")
    with open(file_path, "a") as file:
        file.write(f"{CSV_SEPARATOR}".join(line) + "\n")



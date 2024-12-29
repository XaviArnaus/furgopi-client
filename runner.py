import time
import sys
import os
import requests
from pathlib import Path
from datetime import datetime, timezone

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
            "name": "name",
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
            "name": "name",
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
                filename = f"{sensor}/{datapoint.name}.csv"
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

def send():
    try:
        for datapoint_folder in _get_datapoints_storage_folders():
            # Per convention, the datapoint folder is the sensor type, that is also the server endpoint route.
            target_filename = f"{datapoint_folder['name']}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}.csv"
            target_url = Config(CONFIG_FILENAME).get("server.url") + "/" + datapoint_folder['name']
        
            for datapoint_file in _get_datapoint_files_in_folder(Path(datapoint_folder['path'])):
                print("\n" + TerminalColor.BLUE_BRIGHT + f"Sending file {datapoint_file} to {target_url}" + TerminalColor.END)
                response = _send_file_by_post(
                    original_file=datapoint_file,
                    target_url=target_url,
                    target_filename=target_filename,
                )
                if response.status_code != 200:
                    print(TerminalColor.RED_BRIGHT)
                    print(f"Status Code: {response.status_code}")
                    print(f"Reason: {response.content}")
                    print(TerminalColor.END)
                else:
                    print(TerminalColor.BLUE_BRIGHT + f"File sent" + TerminalColor.END)
                    _delete_sent_file(original_file=datapoint_file)
                    print(TerminalColor.BLUE_BRIGHT + f"Local file {datapoint_file} deleted" + TerminalColor.END )
                    print("\n" + TerminalColor.GREEN_BRIGHT + "End" + TerminalColor.END + "\n")


    except Exception:
        print(full_stack())

def _get_datapoints_storage_folders() -> list:
    root_path_to_datapoints = Path(Config(CONFIG_FILENAME).get("datapoints.path"))
    return [ {"name": f.name, "path": f.path} for f in os.scandir(root_path_to_datapoints) if f.is_dir() ]

def _get_datapoint_files_in_folder(folder: Path) -> list:
    return folder.glob('*.csv')

def _send_file_by_post(original_file: Path, target_url: str, target_filename: str) -> requests.Response:
    # Don't define the headers to send a file. You'll need to set up the boundary.
    #   Requests can do it by itself.
    files = {
        'file': (target_filename, open(original_file, "rb"), "text/csv"),
    }
    return requests.post(target_url, files=files)

def _delete_sent_file(original_file: Path):
    original_file.unlink(missing_ok=True)

def _export_datapoint_to_csv(datapoint: BaseEntity, fields_map: dict, filename: str):
    file_path = Path(Config(CONFIG_FILENAME).get("datapoints.path") + filename)

    # The weakness here is that the order of the field names may be different
    #   to the order where the fields are placed inside the object, therefore
    #   the datapoints are read with fields in different order and then exported
    #   to the CSV nor matching the header.

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



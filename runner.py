import time
import sys
import os

from pyxavi.terminal_color import TerminalColor
from pyxavi.debugger import full_stack, dd

from furgopi_client.entities.base_entity import BaseEntity
from furgopi_client.temperature_runner import TemperatureRunner
from furgopi_client.gps_runner import GpsRunner

LOOP_SLEEP = 1.0

runners = {
    "gps": GpsRunner(),
    "temperature": TemperatureRunner()
}

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

def run():
    try:
        result = {}
        datapoints = _get_data()
        for name, datapoint in datapoints.items():
            if datapoint:
                if isinstance(datapoint, list):
                    for point in datapoint:
                        id = point.name
                        data = _prepare_dict_for_json(point)
                        result[id] = data
                else:     
                    id = datapoint.name
                    data = _prepare_dict_for_json(datapoint)
                    result[id] = data
            else:
                print(f"No datapoint from the {name} module")

        dd(result)
    except RuntimeError as e:
        print(TerminalColor.RED_BRIGHT + str(e) + TerminalColor.END)
    except Exception:
        print(full_stack())

def _get_data() -> dict:
    output = {}
    for name, runner in runners.items():
        output[name] = runner.run()

    return output

def _prepare_dict_for_json(datapoint: BaseEntity) -> dict:
    # Convert into a dict
    data = datapoint.to_dict()
    # Remove the name from the data
    del data.name

    return data


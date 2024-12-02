import time
import sys
import os

from pyxavi.terminal_color import TerminalColor
from pyxavi.debugger import full_stack

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
        datapoints = _get_data()
        for name, datapoint in datapoints.items():
            if datapoint:
                if isinstance(datapoint, list):
                    for point in datapoint:
                        print(f"{name}:\n")
                        print(point.to_string())
                else:     
                    print(f"{name}:\n")
                    print(datapoint.to_string())
            else:
                print(f"No datapoint from the {name} module")
    except RuntimeError as e:
        print(TerminalColor.RED_BRIGHT + str(e) + TerminalColor.END)
    except Exception:
        print(full_stack())

def _get_data() -> dict:
    output = {}
    for name, runner in runners.items():
        output[name] = runner.run()

    return output

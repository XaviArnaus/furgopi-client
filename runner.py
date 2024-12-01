from pyxavi.terminal_color import TerminalColor
from pyxavi.debugger import full_stack

from furgopi_client.temp import Temp
from furgopi_client.latlong import Latlong

def run():
    try:
        Temp().run()
        Latlong().run()
    except RuntimeError as e:
        print(TerminalColor.RED_BRIGHT + str(e) + TerminalColor.END)
    except Exception:
        print(full_stack())

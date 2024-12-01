from pyxavi.terminal_color import TerminalColor
from pyxavi.debugger import full_stack
from furgopi_client.temp import Temp

def run():
    try:
        Temp().run()
    except RuntimeError as e:
        print(TerminalColor.RED_BRIGHT + str(e) + TerminalColor.END)
    except Exception:
        print(full_stack())

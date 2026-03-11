from .rfid._main import RfidManager
from .controller import Controller
from app.core import DEVICES_PATH, EXAMPLE_PATH

rfid_manager = RfidManager(devices_path=DEVICES_PATH, example_path=EXAMPLE_PATH)
controller = Controller()

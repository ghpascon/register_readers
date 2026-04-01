from .rfid._main import RfidManager
from app.core import DEVICES_PATH, EXAMPLE_PATH

rfid_manager = RfidManager(devices_path=DEVICES_PATH, example_path=EXAMPLE_PATH)

from .controller import Controller  # noqa: E402

controller_manager = Controller()

import logging
from smartx_rfid.models.orders import ReadersType, Readers
from app.db import setup_database
from app.core import settings


class Controller:
	def __init__(self):
		self.db_manager = setup_database(settings.SMTX_DB)

	async def register_device(self, serial_number: str, hostname: str, device_class: str):
		try:
			with self.db_manager.get_session() as session:
				# Validate if class exists
				reader_type = session.query(ReadersType).filter_by(name=device_class).first()
				if not reader_type:
					return False, f"Device class '{device_class}' not found."
				# Check if device already exists
				existing_device = (
					session.query(Readers).filter_by(serial_number=serial_number).first()
				)
				if existing_device:
					return False, f"Device with serial number '{serial_number}' already exists."
				# Create new device
				new_device = Readers(
					serial_number=serial_number, hostname=hostname, reader_type_id=reader_type.id
				)
				session.add(new_device)
				return True, f'Device {serial_number} registered successfully'
		except Exception as e:
			logging.error(f'Error registering device {serial_number}: {e}')
			return False, f'Error registering device: {e}'

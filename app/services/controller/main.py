import logging
from smartx_rfid.models.orders import ReadersType, Readers
from app.db import setup_database
from app.core import settings
from app.services import rfid_manager


class Controller:
	def __init__(self):
		self.db_manager = setup_database(settings.SMTX_DB)

	async def register_device(self, serial_number: str, hostname: str, device_class: str):
		try:
			with self.db_manager.get_session() as session:
				# Validate if class exists
				reader_type = session.query(ReadersType).filter_by(name=device_class).first()
				if not reader_type:
					return {
						'registered': False,
						'message': f"Device class '{device_class}' not found",
						'print_label': False,
					}
				# Check if device already exists
				existing_device = (
					session.query(Readers).filter_by(serial_number=serial_number).first()
				)
				if existing_device:
					return {
						'registered': False,
						'message': f"Device with serial number '{serial_number}' already exists.",
						'print_label': True,
					}
				# Create new device
				new_device = Readers(
					serial_number=serial_number, hostname=hostname, reader_type_id=reader_type.id
				)
				session.add(new_device)
				return {
					'registered': True,
					'message': f'Device {serial_number} registered successfully',
					'print_label': True,
				}
		except Exception as e:
			logging.error(f'Error registering device {serial_number}: {e}')
			return False, f'Error registering device: {e}'

	def print_label(self, serial_number: str):
		zpl = settings.ZPL.format(serial=serial_number)
		logging.info(f'Printing label for {serial_number} with ZPL: {zpl}')
		return rfid_manager.devices.print('PRINTER', zpl)

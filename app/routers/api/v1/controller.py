from fastapi import APIRouter
from fastapi.responses import JSONResponse
from smartx_rfid.utils.path import get_prefix_from_path
from app.schemas.devices import RegisterDevice
from app.services import controller_manager

router_prefix = get_prefix_from_path(__file__)
router = APIRouter(prefix=router_prefix, tags=[router_prefix])


@router.post(
	'/register_device',
	summary='Register a new device',
	description='Register a new device with serial number, hostname, and device class.',
)
async def register_device(device_info: RegisterDevice):
	data = await controller_manager.register_device(**device_info.model_dump())
	registered = data.get('registered', False)
	detail = data.get('message', '')
	print_label = data.get('print_label', False)
	if print_label:
		success_label, data_label = controller_manager.print_label(device_info.serial_number)
		return JSONResponse(
			content={
				'registered': registered,
				'message': detail,
				'print_label': print_label,
				'label_printed': success_label,
				'label_data': data_label,
			},
			status_code=200,
		)
	return JSONResponse(content={'error': detail}, status_code=400)

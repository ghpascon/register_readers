from fastapi import APIRouter
from fastapi.responses import JSONResponse
from smartx_rfid.utils.path import get_prefix_from_path
from app.schemas.devices import RegisterDevice
from app.services import controller

router_prefix = get_prefix_from_path(__file__)
router = APIRouter(prefix=router_prefix, tags=[router_prefix])


@router.post(
	'/register_device',
	summary='Register a new device',
	description='Register a new device with serial number, hostname, and device class.',
)
async def register_device(device_info: RegisterDevice):
	success, data = await controller.register_device(**device_info.model_dump())
	if success:
		return JSONResponse(content=data, status_code=200)
	return JSONResponse(content={'error': data}, status_code=400)

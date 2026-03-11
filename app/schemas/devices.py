from pydantic import BaseModel, Field, ValidationInfo, field_validator


class RegisterDevice(BaseModel):
	serial_number: str = Field('smtx-12345678')
	hostname: str = Field('smtx-12345678')
	device_class: str = Field('X714')

	@field_validator('serial_number', 'hostname', 'device_class')
	def validate_fields(cls, v, info: ValidationInfo):
		v = v.strip().lower().replace('_iot', '')
		if len(v) == 0:
			raise ValueError(f'{info.field_name} cannot be empty')
		return v

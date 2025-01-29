from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.exceptions import InternalServerException
from ..models.device import Device


class DeviceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_device(self, device: Device) -> Device:
        """Create a new device."""
        self.session.add(device)
        await self.session.commit()
        await self.session.refresh(device)
        return device

    async def get_device_by_id(self, device_id: str) -> Device | None:
        """Retrieve a device by its ID. Returns None if the device is not found."""

        statement = select(Device).where(Device.device_id == device_id)

        try:
            result = await self.session.exec(statement)
            device = result.first()

            return device if device else None

        except Exception as e:
            print(e)
            raise InternalServerException(
                "An error occurred while retrieving the device") from e

    async def mark_device_as_trusted(self, device_id: str) -> None:
        """Mark a device as trusted."""
        device = await self.get_device_by_id(device_id)
        device.is_trusted = True
        await self.session.commit()

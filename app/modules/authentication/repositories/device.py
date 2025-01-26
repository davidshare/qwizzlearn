from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID
from app.core.exceptions import NotFoundException
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

    async def get_device_by_id(self, device_id: str) -> Device:
        """Retrieve a device by its ID."""
        statement = select(Device).where(Device.device_id == device_id)
        result = await self.session.exec(statement)
        device = result.first()
        if not device:
            raise NotFoundException("Device not found")
        return device

    async def mark_device_as_trusted(self, device_id: str) -> None:
        """Mark a device as trusted."""
        device = await self.get_device_by_id(device_id)
        device.is_trusted = True
        await self.session.commit()

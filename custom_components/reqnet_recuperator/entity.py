"""Base entity for REQNET Recuperator."""
from __future__ import annotations

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_HOST, DOMAIN
from .coordinator import ReqnetDataUpdateCoordinator


class ReqnetEntity(CoordinatorEntity[ReqnetDataUpdateCoordinator]):
    """Base class for all REQNET entities. Accepts both coordinator types since
    ReqnetMqttCoordinator subclasses ReqnetDataUpdateCoordinator."""
    """Base class for all REQNET entities."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: ReqnetDataUpdateCoordinator,
        entry: ConfigEntry,
        unique_id_suffix: str,
    ) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_{unique_id_suffix}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="REQNET Recuperator",
            manufacturer="REQNET / Inprax",
            model="Recuperator",
            configuration_url=f"http://{entry.data[CONF_HOST]}",
        )

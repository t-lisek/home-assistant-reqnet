"""REQNET Recuperator integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import ReqnetApiClient
from .const import (
    CONF_HOST,
    CONF_MAC,
    CONF_SCAN_INTERVAL,
    CONF_UPDATE_METHOD,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    UPDATE_METHOD_MQTT,
)
from .coordinator import ReqnetDataUpdateCoordinator
from .mqtt_coordinator import ReqnetMqttCoordinator

PLATFORMS = [Platform.SENSOR, Platform.SELECT, Platform.BUTTON]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up REQNET Recuperator from a config entry."""
    session = async_get_clientsession(hass)
    client = ReqnetApiClient(entry.data[CONF_HOST], session)

    if entry.data.get(CONF_UPDATE_METHOD) == UPDATE_METHOD_MQTT:
        mac = entry.data.get(CONF_MAC, "")
        coordinator = ReqnetMqttCoordinator(hass, client, mac)
        await coordinator.async_setup()
        try:
            await coordinator.async_config_entry_first_refresh()
        except Exception:
            await coordinator.async_teardown()
            raise
    else:
        scan_interval = entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        coordinator = ReqnetDataUpdateCoordinator(hass, client, scan_interval)
        await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    coordinator = hass.data.get(DOMAIN, {}).get(entry.entry_id)
    if isinstance(coordinator, ReqnetMqttCoordinator):
        await coordinator.async_teardown()

    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload the entry when options change."""
    await hass.config_entries.async_reload(entry.entry_id)

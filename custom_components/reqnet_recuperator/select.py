"""Select platform for REQNET Recuperator."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_call_later

from .api import ReqnetApiError
from .const import (
    BYPASS_CLOSED_AUTO,
    BYPASS_CLOSED_MANUAL,
    BYPASS_OPEN_AUTO,
    BYPASS_OPEN_MANUAL,
    BYPASS_SET_AUTO,
    BYPASS_SET_CLOSED,
    BYPASS_SET_OPEN,
    CONF_MANUAL_AIRFLOW_EXTRACT,
    CONF_MANUAL_AIRFLOW_SUPPLY,
    DEFAULT_MANUAL_AIRFLOW_EXTRACT,
    DEFAULT_MANUAL_AIRFLOW_SUPPLY,
    DOMAIN,
    MODE_AIRING,
    MODE_AUTO,
    MODE_CLEANING,
    MODE_FIREPLACE,
    MODE_HOLIDAY,
    MODE_MANUAL,
    SELECT_BYPASS_AUTO,
    SELECT_BYPASS_CLOSED,
    SELECT_BYPASS_OPEN,
    SELECT_MODE_AIRING,
    SELECT_MODE_AUTO,
    SELECT_MODE_CLEANING,
    SELECT_MODE_FIREPLACE,
    SELECT_MODE_HOLIDAY,
    SELECT_MODE_MANUAL,
)
from .coordinator import ReqnetDataUpdateCoordinator
from .entity import ReqnetEntity

_LOGGER = logging.getLogger(__name__)

_OPTIMISTIC_SETTLE_SECONDS = 2.5

_MODE_NUMBER_TO_OPTION: dict[int, str] = {
    MODE_AUTO: SELECT_MODE_AUTO,
    MODE_MANUAL: SELECT_MODE_MANUAL,
    MODE_FIREPLACE: SELECT_MODE_FIREPLACE,
    MODE_HOLIDAY: SELECT_MODE_HOLIDAY,
    MODE_AIRING: SELECT_MODE_AIRING,
    MODE_CLEANING: SELECT_MODE_CLEANING,
}

_BYPASS_STATE_TO_OPTION: dict[int, str] = {
    BYPASS_CLOSED_MANUAL: SELECT_BYPASS_CLOSED,
    BYPASS_OPEN_MANUAL: SELECT_BYPASS_OPEN,
    BYPASS_CLOSED_AUTO: SELECT_BYPASS_CLOSED,
    BYPASS_OPEN_AUTO: SELECT_BYPASS_OPEN,
}

_BYPASS_OPTION_TO_MODE: dict[str, int] = {
    SELECT_BYPASS_CLOSED: BYPASS_SET_CLOSED,
    SELECT_BYPASS_OPEN: BYPASS_SET_OPEN,
    SELECT_BYPASS_AUTO: BYPASS_SET_AUTO,
}


class OptimisticSelectMixin:
    """Manages optimistic state for select entities with a delayed real-state refresh."""

    _optimistic_option: str | None
    _cancel_optimistic: Any

    def _init_optimistic(self) -> None:
        self._optimistic_option = None
        self._cancel_optimistic = None

    def _set_optimistic(self, option: str) -> None:
        if self._cancel_optimistic:
            self._cancel_optimistic()
        self._optimistic_option = option
        self.async_write_ha_state()  # type: ignore[attr-defined]
        self._cancel_optimistic = async_call_later(
            self.hass,  # type: ignore[attr-defined]
            _OPTIMISTIC_SETTLE_SECONDS,
            self._clear_optimistic,
        )

    @callback
    def _clear_optimistic(self, _now: Any) -> None:
        self._optimistic_option = None
        self._cancel_optimistic = None
        self.hass.async_create_task(  # type: ignore[attr-defined]
            self.coordinator.async_request_refresh()  # type: ignore[attr-defined]
        )

    def _cancel_pending_optimistic(self) -> None:
        if self._cancel_optimistic:
            self._cancel_optimistic()
            self._cancel_optimistic = None


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: ReqnetDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            ReqnetModeSelect(coordinator, entry),
            ReqnetBypassSelect(coordinator, entry),
        ]
    )


class ReqnetModeSelect(OptimisticSelectMixin, ReqnetEntity, SelectEntity):
    """Controls the operating mode of the recuperator."""

    _attr_assumed_state = True
    _attr_translation_key = "mode_select"
    _attr_options = [
        SELECT_MODE_AUTO,
        SELECT_MODE_MANUAL,
        SELECT_MODE_FIREPLACE,
        SELECT_MODE_HOLIDAY,
        SELECT_MODE_AIRING,
        SELECT_MODE_CLEANING,
    ]
    _attr_icon = "mdi:cog-outline"

    def __init__(
        self,
        coordinator: ReqnetDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        ReqnetEntity.__init__(self, coordinator, entry, "mode_select")
        self._entry = entry
        self._init_optimistic()

    @property
    def current_option(self) -> str | None:
        if self._optimistic_option is not None:
            return self._optimistic_option
        return _MODE_NUMBER_TO_OPTION.get(self.coordinator.data.get("mode"))

    async def async_select_option(self, option: str) -> None:
        client = self.coordinator.client
        try:
            if option == SELECT_MODE_AUTO:
                await client.async_set_mode_auto()
            elif option == SELECT_MODE_MANUAL:
                supply = self._entry.options.get(
                    CONF_MANUAL_AIRFLOW_SUPPLY, DEFAULT_MANUAL_AIRFLOW_SUPPLY
                )
                extract = self._entry.options.get(
                    CONF_MANUAL_AIRFLOW_EXTRACT, DEFAULT_MANUAL_AIRFLOW_EXTRACT
                )
                await client.async_set_mode_manual(int(supply), int(extract))
            elif option == SELECT_MODE_FIREPLACE:
                await client.async_set_mode_fireplace()
            elif option == SELECT_MODE_HOLIDAY:
                await client.async_set_mode_holiday()
            elif option == SELECT_MODE_AIRING:
                await client.async_set_mode_airing()
            elif option == SELECT_MODE_CLEANING:
                await client.async_set_mode_cleaning()
        except ReqnetApiError as err:
            raise HomeAssistantError(str(err)) from err
        self._set_optimistic(option)

    @callback
    def _handle_coordinator_update(self) -> None:
        # Real data arriving while optimistic — discard forecast if device confirmed a mode
        if self._optimistic_option is not None:
            real_option = _MODE_NUMBER_TO_OPTION.get(self.coordinator.data.get("mode"))
            if real_option is not None:
                self._cancel_pending_optimistic()
                self._optimistic_option = None
        super()._handle_coordinator_update()

    async def async_will_remove_from_hass(self) -> None:
        self._cancel_pending_optimistic()


class ReqnetBypassSelect(OptimisticSelectMixin, ReqnetEntity, SelectEntity):
    """Controls the bypass valve mode."""

    _attr_assumed_state = True
    _attr_translation_key = "bypass_select"
    _attr_options = [SELECT_BYPASS_CLOSED, SELECT_BYPASS_OPEN, SELECT_BYPASS_AUTO]
    _attr_icon = "mdi:valve"

    def __init__(
        self,
        coordinator: ReqnetDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        ReqnetEntity.__init__(self, coordinator, entry, "bypass_select")
        self._init_optimistic()

    @property
    def current_option(self) -> str | None:
        if self._optimistic_option is not None:
            return self._optimistic_option
        return _BYPASS_STATE_TO_OPTION.get(self.coordinator.data.get("bypass_state"))

    async def async_select_option(self, option: str) -> None:
        try:
            await self.coordinator.client.async_set_bypass(_BYPASS_OPTION_TO_MODE[option])
        except ReqnetApiError as err:
            raise HomeAssistantError(str(err)) from err
        self._set_optimistic(option)

    async def async_will_remove_from_hass(self) -> None:
        self._cancel_pending_optimistic()

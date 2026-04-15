"""Button platform for REQNET Recuperator."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Coroutine

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_call_later

from .api import ReqnetApiClient, ReqnetApiError
from .const import DOMAIN
from .coordinator import ReqnetDataUpdateCoordinator
from .entity import ReqnetEntity

_OPTIMISTIC_SETTLE_SECONDS = 2.5


@dataclass(frozen=True, kw_only=True)
class ReqnetButtonEntityDescription(ButtonEntityDescription):
    """Extends ButtonEntityDescription with an API call factory."""

    api_call: Callable[[ReqnetApiClient], Coroutine[Any, Any, None]]
    # Mode number to set optimistically after press (None = no mode optimism)
    optimistic_mode: int | None = None


BUTTON_DESCRIPTIONS: tuple[ReqnetButtonEntityDescription, ...] = (
        ReqnetButtonEntityDescription(
            key="airing_15",
            translation_key="airing_15",
            icon="mdi:weather-windy",
            api_call=lambda c: c.async_set_mode_airing(15),
            optimistic_mode=4,
        ),
        ReqnetButtonEntityDescription(
            key="airing_30",
            translation_key="airing_30",
            icon="mdi:weather-windy",
            api_call=lambda c: c.async_set_mode_airing(30),
            optimistic_mode=4,
        ),
        ReqnetButtonEntityDescription(
            key="fireplace_5",
            translation_key="fireplace_5",
            icon="mdi:fireplace",
            api_call=lambda c: c.async_set_mode_fireplace(5),
            optimistic_mode=6,
        ),
        ReqnetButtonEntityDescription(
            key="cleaning_5",
            translation_key="cleaning_5",
            icon="mdi:air-filter",
            api_call=lambda c: c.async_set_mode_cleaning(5),
            optimistic_mode=5,
        ),
        ReqnetButtonEntityDescription(
            key="holiday_7",
            translation_key="holiday_7",
            icon="mdi:airplane-takeoff",
            api_call=lambda c: c.async_set_mode_holiday(7),
            optimistic_mode=3,
        ),
        ReqnetButtonEntityDescription(
            key="cancel_airing",
            translation_key="cancel_airing",
            icon="mdi:weather-windy",
            api_call=lambda c: c.async_cancel_airing(),
        ),
        ReqnetButtonEntityDescription(
            key="cancel_cleaning",
            translation_key="cancel_cleaning",
            icon="mdi:air-filter",
            api_call=lambda c: c.async_cancel_cleaning(),
        ),
        ReqnetButtonEntityDescription(
            key="cancel_fireplace",
            translation_key="cancel_fireplace",
            icon="mdi:fireplace-off",
            api_call=lambda c: c.async_cancel_fireplace(),
        ),
        ReqnetButtonEntityDescription(
            key="cancel_holiday",
            translation_key="cancel_holiday",
            icon="mdi:airplane-off",
            api_call=lambda c: c.async_cancel_holiday(),
        ),
        ReqnetButtonEntityDescription(
            key="replace_filters",
            translation_key="replace_filters",
            icon="mdi:air-filter",
            api_call=lambda c: c.async_replace_filters(),
        ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: ReqnetDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        ReqnetButton(coordinator, entry, description)
        for description in BUTTON_DESCRIPTIONS
    )


class ReqnetButton(ReqnetEntity, ButtonEntity):
    """A single REQNET action button."""

    entity_description: ReqnetButtonEntityDescription

    def __init__(
        self,
        coordinator: ReqnetDataUpdateCoordinator,
        entry: ConfigEntry,
        description: ReqnetButtonEntityDescription,
    ) -> None:
        super().__init__(coordinator, entry, description.key)
        self.entity_description = description

    async def async_press(self) -> None:
        try:
            await self.entity_description.api_call(self.coordinator.client)
        except ReqnetApiError as err:
            raise HomeAssistantError(str(err)) from err

        async_call_later(
            self.hass, _OPTIMISTIC_SETTLE_SECONDS, self._refresh
        )

    @callback
    def _refresh(self, _now: Any) -> None:
        self.hass.async_create_task(self.coordinator.async_request_refresh())

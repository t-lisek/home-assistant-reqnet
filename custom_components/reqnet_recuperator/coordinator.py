"""DataUpdateCoordinator for REQNET Recuperator (HTTP polling mode)."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import ReqnetApiClient, ReqnetApiError
from .const import (
    DOMAIN,
    IDX_AIRFLOW_EXTRACT,
    IDX_AIRFLOW_SUPPLY,
    IDX_BYPASS_STATE,
    IDX_CO2,
    IDX_DEVICE_STATUS,
    IDX_ERROR_CODE,
    IDX_FAN_EXTRACT,
    IDX_FAN_POWER_EXTRACT,
    IDX_FAN_POWER_SUPPLY,
    IDX_FAN_SUPPLY,
    IDX_FILTER_DAYS,
    IDX_HOLIDAY_DAYS_LEFT,
    IDX_HUMIDITY,
    IDX_MODE,
    IDX_PREHEATER,
    IDX_PRESSURE_EXTRACT,
    IDX_PRESSURE_SUPPLY,
    IDX_RESISTANCE_EXTRACT,
    IDX_RESISTANCE_SUPPLY,
    IDX_TEMP_EXHAUST,
    IDX_TEMP_EXTRACT,
    IDX_TEMP_INTAKE,
    IDX_TEMP_SUPPLY,
    IDX_TIME_REMAINING_MIN,
    IDX_TIME_REMAINING_SEC,
)

_LOGGER = logging.getLogger(__name__)


def parse_values(values: list) -> dict[str, Any]:
    """Normalize the raw Values[] array into a typed dict."""
    return {
        "device_status": int(values[IDX_DEVICE_STATUS]),
        "airflow_supply": float(values[IDX_AIRFLOW_SUPPLY]),
        "airflow_extract": float(values[IDX_AIRFLOW_EXTRACT]),
        "humidity": float(values[IDX_HUMIDITY]),
        "co2": int(values[IDX_CO2]),
        "mode": int(values[IDX_MODE]),
        "time_remaining_min": int(values[IDX_TIME_REMAINING_MIN]),
        "time_remaining_sec": int(values[IDX_TIME_REMAINING_SEC]),
        "holiday_days_left": int(values[IDX_HOLIDAY_DAYS_LEFT]),
        "bypass_state": int(values[IDX_BYPASS_STATE]),
        "error_code": int(values[IDX_ERROR_CODE]),
        "temp_intake": float(values[IDX_TEMP_INTAKE]),
        "temp_exhaust": float(values[IDX_TEMP_EXHAUST]),
        "temp_supply": float(values[IDX_TEMP_SUPPLY]),
        "temp_extract": float(values[IDX_TEMP_EXTRACT]),
        "resistance_supply": float(values[IDX_RESISTANCE_SUPPLY]),
        "resistance_extract": float(values[IDX_RESISTANCE_EXTRACT]),
        "fan_supply": float(values[IDX_FAN_SUPPLY]),
        "fan_extract": float(values[IDX_FAN_EXTRACT]),
        "preheater_active": int(values[IDX_PREHEATER]),
        "pressure_supply": float(values[IDX_PRESSURE_SUPPLY]),
        "pressure_extract": float(values[IDX_PRESSURE_EXTRACT]),
        "fan_power_supply": float(values[IDX_FAN_POWER_SUPPLY]),
        "fan_power_extract": float(values[IDX_FAN_POWER_EXTRACT]),
        "filter_days": int(values[IDX_FILTER_DAYS]),
    }


class ReqnetDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Polls the device via HTTP on a fixed interval."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: ReqnetApiClient,
        update_interval: int,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=update_interval),
        )
        self.client = client
        self._first_fetch_logged = False

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            raw = await self.client.async_get_current_work_parameters()
        except ReqnetApiError as err:
            raise UpdateFailed(str(err)) from err

        values = raw["Values"]

        if not self._first_fetch_logged:
            _LOGGER.debug("REQNET raw Values[]: %s", values)
            self._first_fetch_logged = True

        try:
            return parse_values(values)
        except (IndexError, TypeError, ValueError) as err:
            raise UpdateFailed(f"Failed to parse Values[]: {err}") from err

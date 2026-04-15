"""HTTP API client for REQNET Recuperator."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

import aiohttp

_LOGGER = logging.getLogger(__name__)

API_PATH = "/API/RunFunction"
REQUEST_TIMEOUT = 10


class ReqnetApiError(Exception):
    """Raised when communication with the device fails."""


class ReqnetApiClient:
    """Wraps all REQNET HTTP API calls."""

    def __init__(self, host: str, session: aiohttp.ClientSession) -> None:
        self._host = host
        self._session = session

    async def _async_request(self, params: dict[str, Any]) -> dict[str, Any]:
        url = f"http://{self._host}{API_PATH}"
        try:
            async with self._session.get(
                url,
                params=params,
                timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT),
            ) as resp:
                resp.raise_for_status()
                return await resp.json(content_type=None)
        except aiohttp.ClientResponseError as err:
            raise ReqnetApiError(f"HTTP {err.status}: {err.message}") from err
        except aiohttp.ClientError as err:
            raise ReqnetApiError(f"Connection error: {err}") from err
        except asyncio.TimeoutError as err:
            raise ReqnetApiError("Request timed out") from err
        except ValueError as err:
            raise ReqnetApiError(f"Invalid JSON response: {err}") from err

    # -------------------------------------------------------------------------
    # Read
    # -------------------------------------------------------------------------

    async def async_get_status_device(self) -> dict[str, Any]:
        """Return basic device info (used to verify device identity + get MAC)."""
        data = await self._async_request({"name": "StatusDevice"})
        if not data.get("StatusDeviceResult"):
            raise ReqnetApiError("StatusDevice returned failure result")
        return data

    async def async_get_current_work_parameters(self) -> dict[str, Any]:
        """Return current work parameters (full Values[] array)."""
        data = await self._async_request({"name": "CurrentWorkParameters"})
        if not data.get("CurrentWorkParametersResult"):
            raise ReqnetApiError("CurrentWorkParameters returned failure result")
        values = data.get("Values")
        if not isinstance(values, list) or len(values) < 84:
            raise ReqnetApiError(
                f"Unexpected Values array length: {len(values) if isinstance(values, list) else type(values)}"
            )
        return data

    # -------------------------------------------------------------------------
    # Mode control
    # -------------------------------------------------------------------------

    async def async_set_mode_auto(self) -> None:
        await self._async_request({"name": "AutomaticMode"})

    async def async_set_mode_manual(
        self, airflow_supply: int, airflow_extract: int
    ) -> None:
        await self._async_request(
            {
                "name": "ManualMode",
                "airflowvalue": airflow_supply,
                "valueofairextraction": airflow_extract,
            }
        )

    async def async_set_mode_fireplace(self, time: int = 5) -> None:
        await self._async_request({"name": "TurnOnFireplace", "time": time})

    async def async_set_mode_holiday(self, days: int = 7) -> None:
        await self._async_request({"name": "TurnOnHoliday", "days": days})

    async def async_set_mode_airing(self, time: int = 15) -> None:
        await self._async_request({"name": "TurnOnAiring", "time": time})

    async def async_set_mode_cleaning(self, time: int = 5) -> None:
        await self._async_request({"name": "TurnOnCleaning", "time": time})

    # -------------------------------------------------------------------------
    # Mode cancellation
    # -------------------------------------------------------------------------

    async def async_cancel_airing(self) -> None:
        await self._async_request({"name": "TurnOffAiring"})

    async def async_cancel_cleaning(self) -> None:
        await self._async_request({"name": "TurnOffCleaning"})

    async def async_cancel_fireplace(self) -> None:
        await self._async_request({"name": "TurnOffFireplace"})

    async def async_cancel_holiday(self) -> None:
        await self._async_request({"name": "TurnOffHoliday"})

    # -------------------------------------------------------------------------
    # Bypass control
    # -------------------------------------------------------------------------

    async def async_set_bypass(self, mode: int) -> None:
        """Set bypass mode: 0=closed, 1=open, 2=auto."""
        await self._async_request({"name": "SetByPassMode", "mode": mode})

    # -------------------------------------------------------------------------
    # Misc
    # -------------------------------------------------------------------------

    async def async_replace_filters(self) -> None:
        """Reset the filter replacement counter."""
        await self._async_request({"name": "ReplaceFilters"})

    async def async_configure_additional_broker(
        self,
        broker_host: str,
        broker_port: int,
        broker_user: str = "",
        broker_password: str = "",
    ) -> None:
        """Point the device at an additional MQTT broker."""
        await self._async_request(
            {
                "name": "ChangeAdditionalBrokerConfiguration",
                "MQTT_ADDITIONAL_BROKER_ADDRESS": broker_host,
                "MQTT_ADDITIONAL_BROKER_PORT": broker_port,
                "MQTT_ADDITIONAL_BROKER_USER": broker_user,
                "MQTT_ADDITIONAL_BROKER_PASSWORD": broker_password,
            }
        )

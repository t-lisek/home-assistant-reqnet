"""Config flow for REQNET Recuperator integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import (
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)

from .api import ReqnetApiClient, ReqnetApiError
from .const import (
    CONF_BROKER_HOST,
    CONF_BROKER_PASSWORD,
    CONF_BROKER_PORT,
    CONF_BROKER_USER,
    CONF_HOST,
    CONF_MAC,
    CONF_MANUAL_AIRFLOW_EXTRACT,
    CONF_MANUAL_AIRFLOW_SUPPLY,
    CONF_SCAN_INTERVAL,
    CONF_UPDATE_METHOD,
    DEFAULT_BROKER_PORT,
    DEFAULT_MANUAL_AIRFLOW_EXTRACT,
    DEFAULT_MANUAL_AIRFLOW_SUPPLY,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    UPDATE_METHOD_MQTT,
    UPDATE_METHOD_POLL,
)

_LOGGER = logging.getLogger(__name__)


class ReqnetConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle the setup config flow."""

    VERSION = 1

    def __init__(self) -> None:
        self._host: str = ""
        self._mac: str = ""
        self._update_method: str = UPDATE_METHOD_POLL

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> dict:
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST].strip()
            session = async_get_clientsession(self.hass)
            client = ReqnetApiClient(host, session)

            try:
                status = await client.async_get_status_device()
            except ReqnetApiError:
                errors["base"] = "cannot_connect"
            else:
                if not status.get("StatusDeviceResult"):
                    errors["base"] = "not_reqnet_device"
                else:
                    self._host = host
                    self._mac = status.get("MAC", "")
                    await self.async_set_unique_id(self._mac or host)
                    self._abort_if_unique_id_configured()
                    return await self.async_step_update_method()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): TextSelector(
                        TextSelectorConfig(type=TextSelectorType.TEXT)
                    ),
                }
            ),
            errors=errors,
        )

    async def async_step_update_method(
        self, user_input: dict[str, Any] | None = None
    ) -> dict:
        mqtt_available = "mqtt" in self.hass.config.components

        if not mqtt_available:
            return await self.async_step_poll_interval()

        if user_input is not None:
            self._update_method = user_input[CONF_UPDATE_METHOD]
            if self._update_method == UPDATE_METHOD_MQTT:
                return await self.async_step_mqtt_broker()
            return await self.async_step_poll_interval()

        return self.async_show_form(
            step_id="update_method",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_UPDATE_METHOD, default=UPDATE_METHOD_MQTT
                    ): SelectSelector(
                        SelectSelectorConfig(
                            options=[UPDATE_METHOD_MQTT, UPDATE_METHOD_POLL],
                            mode=SelectSelectorMode.LIST,
                            translation_key="update_method",
                        )
                    ),
                }
            ),
        )

    async def async_step_mqtt_broker(
        self, user_input: dict[str, Any] | None = None
    ) -> dict:
        errors: dict[str, str] = {}

        if user_input is not None:
            session = async_get_clientsession(self.hass)
            client = ReqnetApiClient(self._host, session)
            try:
                await client.async_configure_additional_broker(
                    broker_host=user_input[CONF_BROKER_HOST],
                    broker_port=int(user_input[CONF_BROKER_PORT]),
                    broker_user=user_input.get(CONF_BROKER_USER, ""),
                    broker_password=user_input.get(CONF_BROKER_PASSWORD, ""),
                )
            except ReqnetApiError:
                errors["base"] = "mqtt_configure_failed"
            else:
                return self._create_entry(
                    update_method=UPDATE_METHOD_MQTT,
                    broker_host=user_input[CONF_BROKER_HOST],
                    broker_port=int(user_input[CONF_BROKER_PORT]),
                    broker_user=user_input.get(CONF_BROKER_USER, ""),
                    broker_password=user_input.get(CONF_BROKER_PASSWORD, ""),
                )

        return self.async_show_form(
            step_id="mqtt_broker",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_BROKER_HOST): TextSelector(
                        TextSelectorConfig(type=TextSelectorType.TEXT)
                    ),
                    vol.Required(
                        CONF_BROKER_PORT, default=DEFAULT_BROKER_PORT
                    ): NumberSelector(
                        NumberSelectorConfig(min=1, max=65535, mode=NumberSelectorMode.BOX)
                    ),
                    vol.Optional(CONF_BROKER_USER): TextSelector(
                        TextSelectorConfig(type=TextSelectorType.TEXT)
                    ),
                    vol.Optional(CONF_BROKER_PASSWORD): TextSelector(
                        TextSelectorConfig(type=TextSelectorType.PASSWORD)
                    ),
                }
            ),
            errors=errors,
        )

    async def async_step_poll_interval(
        self, user_input: dict[str, Any] | None = None
    ) -> dict:
        if user_input is not None:
            return self._create_entry(
                update_method=UPDATE_METHOD_POLL,
                scan_interval=int(user_input[CONF_SCAN_INTERVAL]),
            )

        return self.async_show_form(
            step_id="poll_interval",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                    ): NumberSelector(
                        NumberSelectorConfig(
                            min=10, max=300, step=5, mode=NumberSelectorMode.SLIDER
                        )
                    ),
                }
            ),
        )

    def _create_entry(self, update_method: str, **kwargs: Any) -> dict:
        data: dict[str, Any] = {
            CONF_HOST: self._host,
            CONF_MAC: self._mac,
            CONF_UPDATE_METHOD: update_method,
            **kwargs,
        }
        return self.async_create_entry(
            title=f"REQNET Recuperator ({self._host})",
            data=data,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> ReqnetOptionsFlow:
        return ReqnetOptionsFlow(config_entry)


class ReqnetOptionsFlow(OptionsFlow):
    """Handle options — manual mode airflow values."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        self._config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> dict:
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        current = self._config_entry.options

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_MANUAL_AIRFLOW_SUPPLY,
                        default=current.get(
                            CONF_MANUAL_AIRFLOW_SUPPLY, DEFAULT_MANUAL_AIRFLOW_SUPPLY
                        ),
                    ): NumberSelector(
                        NumberSelectorConfig(
                            min=50, max=500, step=10, mode=NumberSelectorMode.SLIDER
                        )
                    ),
                    vol.Required(
                        CONF_MANUAL_AIRFLOW_EXTRACT,
                        default=current.get(
                            CONF_MANUAL_AIRFLOW_EXTRACT, DEFAULT_MANUAL_AIRFLOW_EXTRACT
                        ),
                    ): NumberSelector(
                        NumberSelectorConfig(
                            min=50, max=500, step=10, mode=NumberSelectorMode.SLIDER
                        )
                    ),
                }
            ),
        )

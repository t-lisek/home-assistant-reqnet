"""MQTT-based coordinator for REQNET Recuperator (push mode with HTTP polling fallback)."""
from __future__ import annotations

import json
import logging
from typing import Any

from homeassistant.components import mqtt
from homeassistant.core import HomeAssistant, callback

from .api import ReqnetApiClient
from .const import MQTT_SAFETY_POLL_INTERVAL
from .coordinator import ReqnetDataUpdateCoordinator, parse_values

_LOGGER = logging.getLogger(__name__)


class ReqnetMqttCoordinator(ReqnetDataUpdateCoordinator):
    """Receives push updates over MQTT; inherits HTTP polling as a safety-net fallback."""

    def __init__(self, hass: HomeAssistant, client: ReqnetApiClient, mac: str) -> None:
        super().__init__(hass, client, MQTT_SAFETY_POLL_INTERVAL)
        self._topic = f"{mac}/CurrentWorkParametersResult"
        self._unsubscribe_mqtt: Any = None

    async def async_setup(self) -> None:
        self._unsubscribe_mqtt = await mqtt.async_subscribe(
            self.hass, self._topic, self._handle_mqtt_message, qos=0
        )
        _LOGGER.debug("REQNET MQTT coordinator subscribed to %s", self._topic)

    async def async_teardown(self) -> None:
        if self._unsubscribe_mqtt:
            self._unsubscribe_mqtt()

    @callback
    def _handle_mqtt_message(self, message: mqtt.ReceiveMessage) -> None:
        try:
            raw = json.loads(message.payload)
            values = raw.get("Values")
            if not isinstance(values, list) or len(values) < 84:
                _LOGGER.warning("REQNET MQTT: unexpected payload structure")
                return
            if not self._first_fetch_logged:
                _LOGGER.debug("REQNET MQTT raw Values[]: %s", values)
                self._first_fetch_logged = True
            parsed = parse_values(values)
            if parsed == self.data:
                return
            self.async_set_updated_data(parsed)
        except (json.JSONDecodeError, ValueError, IndexError, TypeError) as err:
            _LOGGER.warning("REQNET MQTT: failed to parse message: %s", err)

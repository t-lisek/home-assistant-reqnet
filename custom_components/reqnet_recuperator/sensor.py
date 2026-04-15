"""Sensor platform for REQNET Recuperator."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONCENTRATION_PARTS_PER_MILLION,
    PERCENTAGE,
    UnitOfPressure,
    UnitOfTemperature,
    UnitOfVolumeFlowRate,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import ReqnetDataUpdateCoordinator
from .entity import ReqnetEntity


@dataclass(frozen=True, kw_only=True)
class ReqnetSensorEntityDescription(SensorEntityDescription):
    """Extends SensorEntityDescription with a coordinator data key (defaults to key)."""

    data_key: str = ""

    def __post_init__(self) -> None:
        if not self.data_key:
            object.__setattr__(self, "data_key", self.key)


SENSOR_DESCRIPTIONS: tuple[ReqnetSensorEntityDescription, ...] = (
    ReqnetSensorEntityDescription(
        key="temp_intake",
        translation_key="temp_intake",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    ReqnetSensorEntityDescription(
        key="temp_exhaust",
        translation_key="temp_exhaust",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    ReqnetSensorEntityDescription(
        key="temp_supply",
        translation_key="temp_supply",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    ReqnetSensorEntityDescription(
        key="temp_extract",
        translation_key="temp_extract",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    ReqnetSensorEntityDescription(
        key="humidity",
        translation_key="humidity",
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
    ),
    ReqnetSensorEntityDescription(
        key="co2",
        translation_key="co2",
        device_class=SensorDeviceClass.CO2,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
    ),
    ReqnetSensorEntityDescription(
        key="airflow_supply",
        translation_key="airflow_supply",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        icon="mdi:air-conditioner",
    ),
    ReqnetSensorEntityDescription(
        key="airflow_extract",
        translation_key="airflow_extract",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        icon="mdi:air-conditioner",
    ),
    ReqnetSensorEntityDescription(
        key="fan_supply",
        translation_key="fan_supply",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:fan",
    ),
    ReqnetSensorEntityDescription(
        key="fan_extract",
        translation_key="fan_extract",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:fan",
    ),
    ReqnetSensorEntityDescription(
        key="fan_power_supply",
        translation_key="fan_power_supply",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:fan",
    ),
    ReqnetSensorEntityDescription(
        key="fan_power_extract",
        translation_key="fan_power_extract",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:fan",
    ),
    ReqnetSensorEntityDescription(
        key="pressure_supply",
        translation_key="pressure_supply",
        device_class=SensorDeviceClass.PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPressure.PA,
    ),
    ReqnetSensorEntityDescription(
        key="pressure_extract",
        translation_key="pressure_extract",
        device_class=SensorDeviceClass.PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPressure.PA,
    ),
    ReqnetSensorEntityDescription(
        key="resistance_supply",
        translation_key="resistance_supply",
        device_class=SensorDeviceClass.PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPressure.PA,
    ),
    ReqnetSensorEntityDescription(
        key="resistance_extract",
        translation_key="resistance_extract",
        device_class=SensorDeviceClass.PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPressure.PA,
    ),
    ReqnetSensorEntityDescription(
        key="mode",
        translation_key="mode",
        icon="mdi:cog",
    ),
    ReqnetSensorEntityDescription(
        key="bypass_state",
        translation_key="bypass_state",
        icon="mdi:valve",
    ),
    ReqnetSensorEntityDescription(
        key="preheater_active",
        translation_key="preheater_active",
        icon="mdi:radiator",
    ),
    ReqnetSensorEntityDescription(
        key="filter_days",
        translation_key="filter_days",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="d",
        icon="mdi:air-filter",
    ),
    ReqnetSensorEntityDescription(
        key="time_remaining_min",
        translation_key="time_remaining_min",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="min",
        icon="mdi:timer",
    ),
    ReqnetSensorEntityDescription(
        key="holiday_days_left",
        translation_key="holiday_days_left",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="d",
        icon="mdi:airplane-takeoff",
    ),
    ReqnetSensorEntityDescription(
        key="error_code",
        translation_key="error_code",
        icon="mdi:alert-circle",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: ReqnetDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        ReqnetSensor(coordinator, entry, description)
        for description in SENSOR_DESCRIPTIONS
    )


class ReqnetSensor(ReqnetEntity, SensorEntity):
    """A single REQNET telemetry sensor."""

    entity_description: ReqnetSensorEntityDescription

    def __init__(
        self,
        coordinator: ReqnetDataUpdateCoordinator,
        entry: ConfigEntry,
        description: ReqnetSensorEntityDescription,
    ) -> None:
        super().__init__(coordinator, entry, description.key)
        self.entity_description = description

    @property
    def native_value(self) -> Any:
        return self.coordinator.data.get(self.entity_description.data_key)

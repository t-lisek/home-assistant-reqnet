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
    """Sensor description for REQNET entities."""


SENSOR_DESCRIPTIONS: tuple[ReqnetSensorEntityDescription, ...] = (
    ReqnetSensorEntityDescription(
        key="temp_intake",
        name="Intake Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    ReqnetSensorEntityDescription(
        key="temp_exhaust",
        name="Exhaust Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    ReqnetSensorEntityDescription(
        key="temp_supply",
        name="Supply Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    ReqnetSensorEntityDescription(
        key="temp_extract",
        name="Extract Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    ReqnetSensorEntityDescription(
        key="humidity",
        name="Humidity",
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
    ),
    ReqnetSensorEntityDescription(
        key="co2",
        name="CO2",
        device_class=SensorDeviceClass.CO2,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
    ),
    ReqnetSensorEntityDescription(
        key="airflow_supply",
        name="Supply Airflow",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        icon="mdi:air-conditioner",
    ),
    ReqnetSensorEntityDescription(
        key="airflow_extract",
        name="Extract Airflow",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        icon="mdi:air-conditioner",
    ),
    ReqnetSensorEntityDescription(
        key="fan_supply",
        name="Supply Fan Speed",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:fan",
    ),
    ReqnetSensorEntityDescription(
        key="fan_extract",
        name="Extract Fan Speed",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:fan",
    ),
    ReqnetSensorEntityDescription(
        key="fan_power_supply",
        name="Supply Fan Power",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:fan",
    ),
    ReqnetSensorEntityDescription(
        key="fan_power_extract",
        name="Extract Fan Power",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:fan",
    ),
    ReqnetSensorEntityDescription(
        key="pressure_supply",
        name="Supply Pressure",
        device_class=SensorDeviceClass.PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPressure.PA,
    ),
    ReqnetSensorEntityDescription(
        key="pressure_extract",
        name="Extract Pressure",
        device_class=SensorDeviceClass.PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPressure.PA,
    ),
    ReqnetSensorEntityDescription(
        key="resistance_supply",
        name="Supply Duct Resistance",
        device_class=SensorDeviceClass.PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPressure.PA,
    ),
    ReqnetSensorEntityDescription(
        key="resistance_extract",
        name="Extract Duct Resistance",
        device_class=SensorDeviceClass.PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPressure.PA,
    ),
    ReqnetSensorEntityDescription(
        key="mode",
        name="Operating Mode",
        icon="mdi:cog",
    ),
    ReqnetSensorEntityDescription(
        key="bypass_state",
        name="Bypass State",
        icon="mdi:valve",
    ),
    ReqnetSensorEntityDescription(
        key="preheater_active",
        name="Preheater",
        icon="mdi:radiator",
    ),
    ReqnetSensorEntityDescription(
        key="filter_days",
        name="Days to Filter Replacement",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="d",
        icon="mdi:air-filter",
    ),
    ReqnetSensorEntityDescription(
        key="time_remaining_min",
        name="Mode Time Remaining",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="min",
        icon="mdi:timer",
    ),
    ReqnetSensorEntityDescription(
        key="holiday_days_left",
        name="Holiday Days Remaining",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="d",
        icon="mdi:airplane-takeoff",
    ),
    ReqnetSensorEntityDescription(
        key="error_code",
        name="Error Code",
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
        return self.coordinator.data.get(self.entity_description.key)

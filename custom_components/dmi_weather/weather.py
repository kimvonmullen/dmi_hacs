"""Support for DMI Weather EDR."""
from __future__ import annotations

from homeassistant.components.weather import (
    ATTR_FORECAST_CONDITION,
    ATTR_FORECAST_NATIVE_PRECIPITATION,
    ATTR_FORECAST_NATIVE_TEMP,
    ATTR_FORECAST_NATIVE_TEMP_LOW,
    ATTR_FORECAST_TIME,
    ATTR_FORECAST_WIND_BEARING,
    ATTR_FORECAST_WIND_SPEED,
    Forecast,
    WeatherEntity,
    WeatherEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_NAME,
    UnitOfLength,
    UnitOfPrecipitationDepth,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import DMIWeatherCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the DMI Weather EDR weather platform."""
    coordinator: DMIWeatherCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    name = config_entry.data[CONF_NAME]
    async_add_entities([DMIWeatherEntity(coordinator, name)], False)


class DMIWeatherEntity(CoordinatorEntity[DMIWeatherCoordinator], WeatherEntity):
    """Representation of a DMI Weather entity."""

    _attr_attribution = "Data provided by Danish Meteorological Institute's (DMI) Open Data API"
    _attr_native_precipitation_unit = UnitOfPrecipitationDepth.MILLIMETERS
    _attr_native_pressure_unit = UnitOfPressure.HPA
    _attr_native_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_native_visibility_unit = UnitOfLength.KILOMETERS
    _attr_native_wind_speed_unit = UnitOfSpeed.METERS_PER_SECOND
    _attr_supported_features = WeatherEntityFeature.FORECAST_DAILY | WeatherEntityFeature.FORECAST_HOURLY

    def __init__(self, coordinator: DMIWeatherCoordinator, name: str) -> None:
        """Initialize the DMI Weather EDR entity."""
        super().__init__(coordinator)
        self._attr_name = name
        self._attr_unique_id = f"dmi_edr_{coordinator.api.latitude}_{coordinator.api.longitude}"

    @property
    def _current(self) -> dict:
        return self.coordinator.data.get("current", {}) if self.coordinator.data else {}

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success and bool(self._current)

    @property
    def condition(self) -> str | None:
        return self._current.get("weather_code")

    @property
    def native_temperature(self) -> float | None:
        return self._current.get("temperature")

    @property
    def native_pressure(self) -> float | None:
        return self._current.get("pressure")

    @property
    def native_wind_speed(self) -> float | None:
        return self._current.get("wind_speed")

    @property
    def wind_bearing(self) -> float | None:
        return self._current.get("wind_direction")

    @property
    def native_visibility(self) -> float | None:
        visibility = self._current.get("visibility")
        if visibility is not None:
            return visibility / 1000
        return None

    @property
    def humidity(self) -> float | None:
        return self._current.get("humidity")

    @property
    def native_wind_gust_speed(self) -> float | None:
        return self._current.get("wind_gust")

    @property
    def cloud_coverage(self) -> float | None:
        return self._current.get("cloud_cover")

    async def async_forecast_daily(self) -> list[Forecast] | None:
        """Return the daily forecast."""
        daily = self.coordinator.data.get("daily", []) if self.coordinator.data else []
        if not daily:
            return None

        forecast_list = []
        for forecast in daily:
            forecast_dict = {
                ATTR_FORECAST_TIME: forecast.get("time"),
                ATTR_FORECAST_NATIVE_TEMP: forecast.get("temperature_max"),
                ATTR_FORECAST_NATIVE_TEMP_LOW: forecast.get("temperature_min"),
                ATTR_FORECAST_NATIVE_PRECIPITATION: forecast.get("precipitation"),
                ATTR_FORECAST_WIND_SPEED: forecast.get("wind_speed"),
                ATTR_FORECAST_WIND_BEARING: forecast.get("wind_direction"),
            }
            weather_code = forecast.get("weather_code")
            if weather_code is not None:
                forecast_dict[ATTR_FORECAST_CONDITION] = weather_code
            forecast_list.append(Forecast(**forecast_dict))
        return forecast_list

    async def async_forecast_hourly(self) -> list[Forecast] | None:
        """Return the hourly forecast."""
        hourly = self.coordinator.data.get("hourly", []) if self.coordinator.data else []
        if not hourly:
            return None

        forecast_list = []
        for forecast in hourly:
            forecast_dict = {
                ATTR_FORECAST_TIME: forecast.get("time"),
                ATTR_FORECAST_NATIVE_TEMP: forecast.get("temperature"),
                ATTR_FORECAST_NATIVE_PRECIPITATION: forecast.get("precipitation"),
                ATTR_FORECAST_WIND_SPEED: forecast.get("wind_speed"),
                ATTR_FORECAST_WIND_BEARING: forecast.get("wind_direction"),
            }
            weather_code = forecast.get("weather_code")
            if weather_code is not None:
                forecast_dict[ATTR_FORECAST_CONDITION] = weather_code
            forecast_list.append(Forecast(**forecast_dict))
        return forecast_list

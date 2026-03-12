"""DataUpdateCoordinator for DMI Weather."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .dmi_api import DMIWeatherAPI

_LOGGER = logging.getLogger(__name__)


class DMIWeatherCoordinator(DataUpdateCoordinator):
    """Manages fetching DMI weather data on a schedule."""

    def __init__(self, hass: HomeAssistant, api: DMIWeatherAPI, update_interval_minutes: int) -> None:
        self.api = api
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=update_interval_minutes),
        )

    async def _async_update_data(self) -> dict:
        try:
            await self.api.update()
            return {
                "current": self.api.current_data,
                "hourly": self.api.hourly_forecast_data,
                "daily": self.api.daily_forecast_data,
            }
        except Exception as err:
            raise UpdateFailed(f"Error fetching DMI data: {err}") from err

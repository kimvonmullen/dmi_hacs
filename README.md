# DMI Weather Integration for Home Assistant

> **Based on** the original work by [@crusell](https://github.com/crusell): [DMI_HA_Plugin](https://github.com/crusell/DMI_HA_Plugin). This project continues development from that foundation with additional improvements and HACS support.

A fast and efficient Home Assistant integration for Danish Meteorological Institute (DMI) weather data using the EDR (Environmental Data Retrieval) API.

This integration provides:
- **Current weather conditions** with temperature, humidity, pressure, wind, and more
- **24-hour hourly forecasts** with detailed weather parameters
- **5-day daily forecasts** with high/low temperatures
- **Fast response times** (2-3 seconds vs 30+ seconds for GRIB-based solutions)
- **Efficient data transfer** (10KB JSON vs 7GB GRIB files)
- **Purpose-built** for weather data retrieval

## 🚀 Why EDR?

**EDR (Environmental Data Retrieval) is the perfect solution for Home Assistant weather integration:**

- ✅ **Fast**: 2-3 second response times
- ✅ **Efficient**: Only downloads the data you need (10KB vs 7GB)
- ✅ **Purpose-built**: Designed exactly for this use case
- ✅ **Standard**: Follows OGC EDR specification
- ✅ **Reliable**: Robust error handling and fallback mechanisms

**STAC/GRIB approaches are overkill** - they download entire weather model grids when you only need data for one location.

## Features

- **Current Weather**: Temperature, humidity, pressure, wind speed and direction, visibility
- **Daily Forecast**: 5-day weather forecast with min/max temperatures, precipitation, and wind conditions
- **Location-based**: Use GPS coordinates to get weather data for any location
- **API Key Support**: Updated to work with DMI's new authenticated API
- **Real-time Updates**: Automatically updates weather data

## Prerequisites

- **DMI API Key**: Get a free API key from [DMI Open Data Portal](https://dmiapi.govcloud.dk/#!/apis)
- Home Assistant (version 2023.8 or later recommended)
- Internet connection for API access

## Installation

### Method 1: Manual Installation (Recommended)

1. Download or clone this repository
2. Copy the `custom_components/dmi_weather` folder to your Home Assistant `config/custom_components/` directory
3. Restart Home Assistant
4. Go to **Settings** → **Devices & Services** → **Add Integration**
5. Search for "DMI Weather" and add it

### Method 2: HACS Installation

1. Add this repository to HACS as a custom repository
2. Install the integration through HACS
3. Restart Home Assistant
4. Add the integration through the UI

## Configuration

### Step 1: Get DMI API Key

1. Go to [DMI Open Data Portal](https://dmiapi.govcloud.dk/#!/apis)
2. Register for a free account
3. Request access to the EDR API
4. You'll receive an API key via email

**Test API Key**: `YOUR_API_KEY_HERE` (get your free key from DMI Open Data Portal)

### Step 2: Add Integration

1. In Home Assistant, go to **Settings** → **Devices & Services** → **Add Integration**
2. Search for "DMI Weather"
3. Click on **DMI Weather**

### Step 3: Enter Configuration

1. **Name**: A friendly name for your weather entity (e.g., "Rydebäck Weather")
2. **DMI API Key**: Enter your API key from DMI
3. **Latitude**: The latitude of your location (e.g., 55.9667 for Rydebäck, Sweden)
4. **Longitude**: The longitude of your location (e.g., 12.7667 for Rydebäck, Sweden)

### Example Configuration for Rydebäck, Sweden

- **Name**: Rydebäck Weather
- **Latitude**: 55.9667
- **Longitude**: 12.7667

## Usage

Once configured, the integration will create a weather entity that provides:

### Current Weather
- Temperature (in Celsius)
- Humidity (percentage)
- Pressure (hPa)
- Wind speed (m/s)
- Wind direction (degrees)
- Weather condition (clear, cloudy, rain, etc.)
- Visibility (km)

### Daily Forecast
- Maximum and minimum temperatures
- Precipitation amount
- Wind speed and direction
- Weather conditions

## Data Source

This integration uses the DMI HARMONIE DINI IG weather model, which provides:
- High-resolution weather forecasts
- Coverage for Denmark and surrounding areas
- Updates every 6 hours
- Data available for up to 5 days ahead

For more information about the DMI Open Data API, visit: https://opendatadocs.dmi.govcloud.dk/DMIOpenData

## Troubleshooting

### Common Issues

1. **API Key Required**: Make sure you have a valid DMI API key
2. **No data available**: 
   - Verify your coordinates are within the DMI coverage area
   - Check that your API key has proper permissions
   - Try different coordinates if available
3. **API errors**: 
   - Check your internet connection
   - Verify API key is correct
   - Check DMI API status

### Debug Logging

To enable debug logging, add the following to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.dmi_weather: debug
```

## Technical Details

- **API Endpoint**: DMI EDR API (`https://dmigw.govcloud.dk/v1/forecastedr`)
- **Authentication**: API key required (`X-Gravitee-Api-Key` header)
- **Data Collection**: HARMONIE DINI EPS means model
- **Update Frequency**: Every 15 minutes
- **Data Format**: CoverageJSON
- **Units**: Metric (Celsius, m/s, hPa, mm)
- **Response Time**: 2-3 seconds
- **Data Transfer**: ~10KB per request

## Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Submitting pull requests

## License

This project is licensed under the MIT License.

## Acknowledgments

- [@crusell](https://github.com/crusell) for the original [DMI_HA_Plugin](https://github.com/crusell/DMI_HA_Plugin) which this project is built upon
- Danish Meteorological Institute (DMI) for providing the Open Data API
- Home Assistant community for the excellent framework

## Status

Not working yet
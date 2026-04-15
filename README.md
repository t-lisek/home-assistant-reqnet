# REQNET Recuperator — Home Assistant Integration

> ⚠️ **Pre-release / Internal Testing**
> This integration is currently in early internal testing (v0.1.0). It has not been tested against a live device yet. Expect rough edges, entity naming changes, and potential breaking updates before a stable release. Do not use in production setups.

A Home Assistant custom integration for [REQNET](https://portal.inprax.pl) recuperator (heat recovery ventilation) units. Replaces a fragmented YAML configuration (REST sensors, template switches, rest_commands) with a single, maintainable Python integration using modern HA architecture.

---

## Features

- **23 telemetry sensors** — temperatures, airflow, fan speed, pressure, CO2, humidity, and more
- **Mode control** via a select entity (automatic, manual, fireplace, holiday, airing, cleaning)
- **Bypass control** via a select entity (closed, open, automatic)
- **10 action buttons** — timed modes, cancel actions, filter counter reset
- **Dual update mode** — MQTT push (instant updates) with HTTP polling fallback, or polling-only
- **Optimistic state** — UI updates immediately after commands; real state confirmed after ~2.5s
- Polish and English translations

---

## Requirements

- Home Assistant 2024.1 or newer
- REQNET recuperator on the local network with HTTP API accessible (default port 80)
- For MQTT mode: Mosquitto broker add-on (or any MQTT broker) configured in Home Assistant

---

## Installation

### Via HACS (recommended)

1. In Home Assistant, open **HACS → Integrations**
2. Click ⋮ → **Custom repositories**
3. Add `https://github.com/t-lisek/home-assistant-reqnet`, category: **Integration**
4. Find **REQNET Recuperator** and click **Download**
5. Restart Home Assistant

### Manual

1. Copy the `custom_components/reqnet_recuperator/` directory into your HA config directory under `custom_components/`
2. Restart Home Assistant

---

## Configuration

1. Go to **Settings → Integrations → Add Integration**
2. Search for **REQNET Recuperator**
3. Follow the setup steps:

**Step 1 — Device IP**
Enter the local IP address of your recuperator. The integration will verify it is reachable and identify the device.

**Step 2 — Update method** *(only shown if MQTT is configured in HA)*
- **MQTT** — the device pushes state updates instantly; HTTP polling runs every 5 minutes as a safety net
- **Polling** — the integration queries the device on a fixed interval (configurable, default 30s)

**Step 3 — MQTT broker details** *(MQTT mode only)*
Enter your HA MQTT broker address, port, and optional credentials. The integration configures the device to publish state to your broker.

**Step 3 — Polling interval** *(polling mode only)*
Set how often the device is queried (10–300 seconds).

### Options

After setup, click **Configure** on the integration to adjust:
- Supply airflow in manual mode (m³/h)
- Extract airflow in manual mode (m³/h)

---

## Entities

### Sensors

| Entity | Description | Unit |
|---|---|---|
| `sensor.reqnet_recuperator_temp_intake` | Outdoor intake air temperature | °C |
| `sensor.reqnet_recuperator_temp_exhaust` | Exhaust air temperature | °C |
| `sensor.reqnet_recuperator_temp_supply` | Supply air temperature (into room) | °C |
| `sensor.reqnet_recuperator_temp_extract` | Extract air temperature (from room) | °C |
| `sensor.reqnet_recuperator_humidity` | Relative humidity | % |
| `sensor.reqnet_recuperator_co2` | CO2 concentration | ppm |
| `sensor.reqnet_recuperator_airflow_supply` | Current supply airflow | m³/h |
| `sensor.reqnet_recuperator_airflow_extract` | Current extract airflow | m³/h |
| `sensor.reqnet_recuperator_fan_supply` | Supply fan speed | % |
| `sensor.reqnet_recuperator_fan_extract` | Extract fan speed | % |
| `sensor.reqnet_recuperator_fan_power_supply` | Supply fan motor power | — |
| `sensor.reqnet_recuperator_fan_power_extract` | Extract fan motor power | — |
| `sensor.reqnet_recuperator_pressure_supply` | Supply duct pressure | Pa |
| `sensor.reqnet_recuperator_pressure_extract` | Extract duct pressure | Pa |
| `sensor.reqnet_recuperator_resistance_supply` | Supply duct resistance | Pa |
| `sensor.reqnet_recuperator_resistance_extract` | Extract duct resistance | Pa |
| `sensor.reqnet_recuperator_mode` | Current operating mode (raw number) | — |
| `sensor.reqnet_recuperator_bypass_state` | Bypass state (0–3) | — |
| `sensor.reqnet_recuperator_preheater_active` | Preheater status | — |
| `sensor.reqnet_recuperator_filter_days` | Days until filter replacement | d |
| `sensor.reqnet_recuperator_time_remaining_min` | Timed mode: minutes remaining | min |
| `sensor.reqnet_recuperator_holiday_days_left` | Holiday mode: days remaining | d |
| `sensor.reqnet_recuperator_error_code` | Device error code (0 = no error) | — |

### Select entities

| Entity | Options |
|---|---|
| `select.reqnet_recuperator_mode` | `automatic`, `manual`, `fireplace`, `holiday`, `airing`, `cleaning` |
| `select.reqnet_recuperator_bypass` | `closed`, `open`, `automatic` |

### Buttons

| Entity | Action |
|---|---|
| `button.reqnet_recuperator_airing_15` | Start airing mode (15 min) |
| `button.reqnet_recuperator_airing_30` | Start airing mode (30 min) |
| `button.reqnet_recuperator_fireplace_5` | Start fireplace mode (5 min) |
| `button.reqnet_recuperator_cleaning_5` | Start cleaning mode (5 min) |
| `button.reqnet_recuperator_holiday_7` | Start holiday mode (7 days) |
| `button.reqnet_recuperator_cancel_airing` | Cancel active airing |
| `button.reqnet_recuperator_cancel_cleaning` | Cancel active cleaning |
| `button.reqnet_recuperator_cancel_fireplace` | Cancel active fireplace mode |
| `button.reqnet_recuperator_cancel_holiday` | Cancel active holiday mode |
| `button.reqnet_recuperator_replace_filters` | Reset filter replacement counter |

---

## Known Limitations

- **Not tested on a live device yet** — Values[] index mapping is based on official API documentation; real-world verification pending
- **Auto-discovery not supported** — device must be added by IP address
- **MQTT mode requires manual broker configuration** — no automatic broker detection
- **Timed mode durations are fixed** — airing 15/30 min, fireplace 5 min, etc.; configurable durations planned

---

## Roadmap

- [ ] Live device testing and Values[] index verification
- [ ] Configurable timed mode durations (options flow)
- [ ] `TurnOn` / `TurnOff` (standby) support
- [ ] Zeroconf/mDNS auto-discovery (if device supports it)
- [ ] GitHub Actions CI for HACS validation

---

## API Reference

Full REQNET API documentation scraped and available in [`docs/api-reference.md`](docs/api-reference.md) (not included in HACS release).

Official source: [portal.inprax.pl](https://portal.inprax.pl/REQNET/OpisyAPI_REQNET?ID_TYPU=9)

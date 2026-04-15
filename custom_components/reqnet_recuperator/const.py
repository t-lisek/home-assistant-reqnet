"""Constants for the REQNET Recuperator integration."""

DOMAIN = "reqnet_recuperator"

CONF_HOST = "host"
CONF_MAC = "mac"
CONF_UPDATE_METHOD = "update_method"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_BROKER_HOST = "broker_host"
CONF_BROKER_PORT = "broker_port"
CONF_BROKER_USER = "broker_user"
CONF_BROKER_PASSWORD = "broker_password"
CONF_MANUAL_AIRFLOW_SUPPLY = "manual_airflow_supply"
CONF_MANUAL_AIRFLOW_EXTRACT = "manual_airflow_extract"

UPDATE_METHOD_MQTT = "mqtt"
UPDATE_METHOD_POLL = "poll"

DEFAULT_SCAN_INTERVAL = 30
DEFAULT_BROKER_PORT = 1883
DEFAULT_MANUAL_AIRFLOW_SUPPLY = 300
DEFAULT_MANUAL_AIRFLOW_EXTRACT = 300

MQTT_SAFETY_POLL_INTERVAL = 300  # seconds — fallback poll in MQTT mode

# Operating mode numbers (Values[10])
MODE_FAST_HEATING = 1
MODE_FAST_COOLING = 2
MODE_HOLIDAY = 3
MODE_AIRING = 4
MODE_CLEANING = 5
MODE_FIREPLACE = 6
MODE_MANUAL = 8
MODE_AUTO = 9
MODE_EFFICIENCY_TEST = 10

# Bypass state as read from Values[39] — 4 states
BYPASS_CLOSED_MANUAL = 0
BYPASS_OPEN_MANUAL = 1
BYPASS_CLOSED_AUTO = 2
BYPASS_OPEN_AUTO = 3

# Bypass mode as sent to SetByPassMode — 3 states
BYPASS_SET_CLOSED = 0
BYPASS_SET_OPEN = 1
BYPASS_SET_AUTO = 2

# Select option strings — mode
SELECT_MODE_AUTO = "auto"
SELECT_MODE_MANUAL = "manual"
SELECT_MODE_FIREPLACE = "fireplace"
SELECT_MODE_HOLIDAY = "holiday"
SELECT_MODE_AIRING = "airing"
SELECT_MODE_CLEANING = "cleaning"

# Select option strings — bypass
SELECT_BYPASS_CLOSED = "closed"
SELECT_BYPASS_OPEN = "open"
SELECT_BYPASS_AUTO = "auto"

# Values[] array indices (0-based; API docs use 1-based numbering)
IDX_DEVICE_STATUS = 0       # 1=on, 0=off
IDX_MAX_AIRFLOW = 1         # max airflow m³/h
IDX_TEMP_ROOM = 2           # room temperature °C
IDX_AIRFLOW_SUPPLY = 3      # current supply airflow m³/h
IDX_AIRFLOW_EXTRACT = 4     # current extract airflow m³/h
IDX_HUMIDITY = 7            # relative humidity %
IDX_CO2 = 8                 # CO2 concentration ppm
IDX_MODE = 10               # operating mode number
IDX_TIME_REMAINING_MIN = 11 # timed mode: minutes remaining
IDX_TIME_REMAINING_SEC = 12 # timed mode: seconds remaining
IDX_HOLIDAY_DAYS_LEFT = 14  # holiday mode: days remaining
IDX_BYPASS_STATE = 39       # bypass state (0-3, see BYPASS_* constants)
IDX_ERROR_CODE = 40         # error code, 0 = no error
IDX_TEMP_INTAKE = 55        # outdoor intake air temp °C (czerpnia)
IDX_TEMP_EXHAUST = 56       # exhaust air temp °C (wyrzutnia)
IDX_TEMP_SUPPLY = 57        # supply air into room °C (nawiew)
IDX_TEMP_EXTRACT = 58       # extract air from room °C (wyciąg)
IDX_RESISTANCE_SUPPLY = 63  # supply duct resistance Pa
IDX_RESISTANCE_EXTRACT = 64 # extract duct resistance Pa
IDX_FAN_SUPPLY = 65         # supply fan speed % (1-100)
IDX_FAN_EXTRACT = 66        # extract fan speed % (1-100)
IDX_PREHEATER = 72          # preheater status: 1=active, 0=inactive
IDX_PRESSURE_SUPPLY = 75    # supply pressure Pa
IDX_PRESSURE_EXTRACT = 76   # extract pressure Pa
IDX_FAN_POWER_SUPPLY = 81   # supply fan motor power
IDX_FAN_POWER_EXTRACT = 82  # extract fan motor power
IDX_FILTER_DAYS = 83        # days until filter replacement

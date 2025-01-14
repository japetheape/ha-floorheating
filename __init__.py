"""The Floor Heating integration."""
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
import voluptuous as vol
from homeassistant.helpers import config_validation as cv

DOMAIN = "floor_heating"
PLATFORMS = [Platform.CLIMATE]

CONF_ZONES = "zones"
CONF_GROUPS = "groups"
CONF_TEMP_SENSOR = "temp_sensor"
CONF_OUTSIDE_TEMP_SENSOR = "outside_temp_sensor"
CONF_FLOW_TEMP_SENSOR = "flow_temp_sensor"
CONF_HEAT_PUMP_SWITCH = "heat_pump_switch"

ZONE_SCHEMA = vol.Schema({
    vol.Required(CONF_GROUPS): [cv.entity_id],
    vol.Required(CONF_TEMP_SENSOR): cv.entity_id,
})

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_OUTSIDE_TEMP_SENSOR): cv.entity_id,
        vol.Required(CONF_FLOW_TEMP_SENSOR): cv.entity_id,
        vol.Required(CONF_HEAT_PUMP_SWITCH): cv.entity_id,
        vol.Required(CONF_ZONES): {
            cv.string: ZONE_SCHEMA
        }
    })
}, extra=vol.ALLOW_EXTRA)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Floor Heating component."""
    if DOMAIN not in config:
        return True

    hass.data[DOMAIN] = {}
    hass.data[DOMAIN]["config"] = config[DOMAIN]  # Store complete config
    
    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN, context={"source": "import"}, data=config[DOMAIN]
        )
    )
    
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Floor Heating from a config entry."""
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    
    hass.data[DOMAIN][entry.entry_id] = entry.data
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
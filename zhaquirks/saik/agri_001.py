"""Saik Agri Device001 Quirks."""

from zigpy.quirks import CustomDevice, CustomCluster
from zigpy.zcl.clusters.homeautomation import ElectricalMeasurement
from zhaquirks.const import (
    DEVICE_TYPE,
    ENDPOINTS,
    INPUT_CLUSTERS,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PROFILE_ID,
)

class DCElectricalMeasurementCluster(CustomCluster, ElectricalMeasurement):
    """Custom cluster for DC voltage reporting."""
    DC_VOLTAGE_ATTR = 0x0100
    DC_CURRENT_ATTR = 0x0103
    DC_POWER_ATTR = 0x0106
    DC_VOLTAGE_MULTIPLIER_ATTR = 0x0200
    DC_VOLTAGE_DIVISOR_ATTR = 0x0201
    DC_CURRENT_MULTIPLIER_ATTR = 0x0202
    DC_CURRENT_DIVISOR_ATTR = 0x0203
    DC_POWER_MULTIPLIER_ATTR = 0x0204
    DC_POWER_DIVISOR_ATTR = 0x0205

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._voltage_multiplier = 1
        self._voltage_divisor = 1
        self._current_multiplier = 1
        self._current_divisor = 1
        self._power_multiplier = 1
        self._power_divisor = 1

    def _update_attribute(self, attrid, value):
        # Cache multiplier and divisor when updated
        if attrid == self.DC_VOLTAGE_MULTIPLIER_ATTR:
            self._voltage_multiplier = value
        elif attrid == self.DC_VOLTAGE_DIVISOR_ATTR:
            self._voltage_divisor = value
        elif attrid == self.DC_CURRENT_MULTIPLIER_ATTR:
            self._current_multiplier = value
        elif attrid == self.DC_CURRENT_DIVISOR_ATTR:
            self._current_divisor = value
        elif attrid == self.DC_POWER_MULTIPLIER_ATTR:
            self._power_multiplier = value
        elif attrid == self.DC_POWER_DIVISOR_ATTR:
            self._power_divisor = value
        elif attrid == self.DC_VOLTAGE_ATTR:
            multiplier = getattr(self, "_voltage_multiplier", 1)
            divisor = getattr(self, "_voltage_divisor", 1)
            scaled_voltage = (value * multiplier) / divisor if divisor else value
            # Expose as a new attribute for ZHA entity
            super()._update_attribute("scaled_voltage", scaled_voltage)
        elif attrid == self.DC_CURRENT_ATTR:
            multiplier = getattr(self, "_current_multiplier", 1)
            divisor = getattr(self, "_current_divisor", 1)
            scaled_current = (value * multiplier) / divisor if divisor else value
            # Expose as a new attribute for ZHA entity
            super()._update_attribute("scaled_current", scaled_current)
        elif attrid == self.DC_POWER_ATTR:
            multiplier = getattr(self, "_power_multiplier", 1)
            divisor = getattr(self, "_power_divisor", 1)
            scaled_power = (value * multiplier) / divisor if divisor else value
            # Expose as a new attribute for ZHA entity
            super()._update_attribute("scaled_power", scaled_power)
        super()._update_attribute(attrid, value)


class SaikAgriDev001(CustomDevice):
    """Custom device for your Zigbee device."""
    signature = {
        MODELS_INFO: [("Saik", "AgriDevice001")],
        ENDPOINTS: {
            1: {
                PROFILE_ID: 0x0104,   # ZHA profile
                DEVICE_TYPE: 0x0102,  # Device type for Agri device
                INPUT_CLUSTERS: [
                    0x0000,  # Basic
                    0x0001,  # Power Configuration
                    0x0003,
                    0x0004,  # Identify
                    0x0005,  # Groups
                    0x0006,  # Scenes
                    0x0008,  # On/Off
                    0x0300,  # Metering
                    0x0B04,  # ElectricalMeasurement
                ],
                OUTPUT_CLUSTERS: [],
            },
            242: {
                PROFILE_ID: 0xA1E0,
                DEVICE_TYPE: 0x0061,
                INPUT_CLUSTERS: [],
                OUTPUT_CLUSTERS: [
                    0x0021,
                ],
            }
        },
    }
    replacement = {
        ENDPOINTS: {
            1: {
                PROFILE_ID: 0x0104,
                DEVICE_TYPE: 0x0102,
                INPUT_CLUSTERS: [
                    0x0000,  # Basic
                    0x0001,  # Power Configuration
                    0x0003,
                    0x0004,  # Identify
                    0x0005,  # Groups
                    0x0006,  # Scenes
                    0x0008,  # On/Off
                    0x0300,  # Metering
                    DCElectricalMeasurementCluster,
                ],
                OUTPUT_CLUSTERS: [],
            },
            242: {
                PROFILE_ID: 0xA1E0,
                DEVICE_TYPE: 0x0061,
                INPUT_CLUSTERS: [],
                OUTPUT_CLUSTERS: [
                    0x0021,
                ],
            }
        },
    }
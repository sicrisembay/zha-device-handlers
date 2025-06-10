"""Saik Agri Device001 Quirks V2."""

from zigpy.quirks.v2 import QuirkBuilder, ReportingConfig
from zigpy.quirks.v2.homeassistant.sensor import SensorDeviceClass, SensorStateClass
from zigpy.zcl.clusters.homeautomation import ElectricalMeasurement


# Define the quirk for Saik Agri Device001
(
    QuirkBuilder("Saik", "AgriDevice001")
        .sensor(
            state_class=SensorStateClass.MEASUREMENT,      # State class for the sensor
            attribute_name="dc_voltage",                   # Attribute name from ElectricalMeasurement.AttributeDefs
            cluster_id=ElectricalMeasurement.cluster_id,   # 0x0B04
            device_class=SensorDeviceClass.VOLTAGE,        # Home Assistant device class
            unit="V",                                      # Unit for voltage
            divisor=1000,                                  # Example: if device reports in decivolts, adjust as needed
            suggested_display_precision=1000,              # Optional: display precision for the sensor
            fallback_name="DC Voltage",                    # Optional: fallback entity name
            unique_id_suffix="dc_voltage",
            primary=True,                                  # Optional: mark as primary entity
            reporting_config=ReportingConfig(
                min_interval=10,  # Minimum reporting interval in seconds
                max_interval=100,  # Maximum reporting interval in seconds
                reportable_change=10,  # Report change of 10 decivolts
            ),
        )
        .sensor(
            state_class=SensorStateClass.MEASUREMENT,
            attribute_name="dc_current",
            cluster_id=ElectricalMeasurement.cluster_id,
            device_class=SensorDeviceClass.CURRENT,
            unit="A",  # Unit for current
            divisor=1000,  # Example: if device reports in deciamps, adjust as needed
            suggested_display_precision=1000,  # Optional: display precision for the sensor
            fallback_name="DC Current",  # Optional: fallback entity name
            unique_id_suffix="dc_current",
            primary=False,  # Optional: mark as primary entity
            reporting_config=ReportingConfig(
                min_interval=10,  # Minimum reporting interval in seconds
                max_interval=100,  # Maximum reporting interval in seconds
                reportable_change=10,  # Report change of 10 deciamps
            ),
        )
        .sensor(
            state_class=SensorStateClass.MEASUREMENT,
            attribute_name="dc_power",                      # Attribute name from ElectricalMeasurement.AttributeDefs
            cluster_id=ElectricalMeasurement.cluster_id,
            device_class=SensorDeviceClass.POWER,           # Home Assistant device class for power
            unit="W",                                       # Unit for power
            divisor=1000,                                   # Adjust if your device reports in mW or other units
            suggested_display_precision=1000,               # Optional: display precision for the sensor
            fallback_name="DC Power",                       # Optional: fallback entity name
            unique_id_suffix="dc_power",
            primary=False,                                   # Optional: mark as primary entity
            reporting_config=ReportingConfig(
                min_interval=10,                            # Minimum reporting interval in seconds
                max_interval=100,                           # Maximum reporting interval in seconds
                reportable_change=1,                        # Report change of 1 watt
            ),
        )
        .add_to_registry()
)

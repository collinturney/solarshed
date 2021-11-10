#!/usr/bin/env python3

from cadence import MetricsClient
import json
import logging
import logging.handlers
from renogy import Controller, Attribute
import time

logger = logging.getLogger("Logger")
logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address = "/dev/log")
logger.addHandler(handler)

attrs = [
    Attribute.BATT_SOC,
    Attribute.BATT_VOLTS,
    Attribute.LOAD_WATTS,
    Attribute.PANEL_VOLTS,
    Attribute.PANEL_AMPS,
    Attribute.PANEL_WATTS,
    Attribute.DAY_CHARGE,
    Attribute.DAY_DISCHARGE,
    Attribute.DAY_GEN_POWER,
    Attribute.DAY_CON_POWER,
    Attribute.CONTROLLER_TEMP,
    Attribute.CHARGING_STATE
]

controller = Controller()
metrics = MetricsClient("http://127.0.0.1:5000")

prev_state = None

while True:
    values = controller.get_all(attrs)
    metrics.post("solarshed", values)

    state = values['charging_state']

    if state != prev_state:
        logger.info("Charging state is now {}".format(state))
    prev_state = state
    
    time.sleep(60)

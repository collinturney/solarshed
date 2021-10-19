#!/usr/bin/env python3

import argparse
from collections import namedtuple
from enum import Enum
import json
import minimalmodbus
import os
import serial
import sys
import time


class SystemType(Enum):
    CONTROLLER = 0
    INVERTER   = 1


class BatteryType(Enum):
    OPEN    = 1
    SEALED  = 2
    GEL     = 3
    LITHIUM = 4
    CUSTOM  = 5


class ChargingState(Enum):
    DEACTIVATED = 0
    ACTIVATED   = 1
    MPPT        = 2
    EQUALIZING  = 3
    BOOST       = 4
    FLOATING    = 5
    LIMITING    = 6


class Functions(object):
    def high_order(reg: int):
        return float((reg >> 8) & 0x00FF)

    def low_order(reg: int):
        return float(reg & 0x00FF)

    def controller_temp(reg: int):
        temp = (reg >> 8) & 0x7F
        sign = (reg >> 8) & 0x80
        return -(temp) if sign == 1 else temp

    def system_type(reg: int):
        return SystemType(int(Functions.low_order(reg))).name

    def battery_type(reg: int):
        return BatteryType(reg).name

    def charging_state(reg: int):
        return ChargingState(reg & 0x00FF).name


Register = namedtuple("Register", ["address", "scale", "units", "function"])


class Attribute(Register, Enum):
    SYS_MAX_VOLTS     = Register(0x00A,    1, "V", Functions.high_order)
    SYS_MAX_AMPS      = Register(0x00A,    1, "A", Functions.low_order)
    SYS_MAX_DISCHARGE = Register(0x00B,    1, "A", Functions.high_order)
    SYS_TYPE          = Register(0x00B,    1, "",  Functions.system_type)
    BATT_SOC          = Register(0x100,    1, "%", None)
    BATT_VOLTS        = Register(0x101,  0.1, "V", None)
    CHARGING_AMPS     = Register(0x102, 0.01, "A", None)
    CONTROLLER_TEMP   = Register(0x103,    1, "C", Functions.controller_temp)
    LOAD_WATTS        = Register(0x106,    1, "W", None)
    PANEL_VOLTS       = Register(0x107,  0.1, "V", None)
    PANEL_AMPS        = Register(0x108, 0.01, "A", None)
    PANEL_WATTS       = Register(0x109,    1, "W", None)
    BATT_MIN_VOLTS    = Register(0x10B,  0.1, "V", None)
    BATT_MAX_VOLTS    = Register(0x10C,  0.1, "V", None)
    DAY_CHARGE        = Register(0x10F,    1, "W", None)
    DAY_DISCHARGE     = Register(0x110,    1, "W", None)
    DAY_GEN_POWER     = Register(0x113,    1, "W", None)
    DAY_CON_POWER     = Register(0x114,    1, "W", None)
    UPTIME_DAYS       = Register(0x115,    1, "",  None)
    BATT_FULL_COUNT   = Register(0x117,    1, "",  None)
    CHARGING_STATE    = Register(0x120,    1, "",  Functions.charging_state)
    BATT_CAPACITY     = Register(0xE002,   1, "W", None)
    SYS_BATT_VOLTS    = Register(0xE003,   1, "V", Functions.high_order)
    RECON_BATT_VOLTS  = Register(0xE003,   1, "V", Functions.low_order)
    BATT_TYPE         = Register(0xE004,   1, "",  Functions.battery_type)
    OVER_VOLTS        = Register(0xE005, 0.1, "V", None)
    CHARGE_VOLTS      = Register(0xE006, 0.1, "V", None)
    EQUALIZE_VOLTS    = Register(0xE007, 0.1, "V", None)
    BOOST_VOLTS       = Register(0xE008, 0.1, "V", None)
    FLOAT_VOLTS       = Register(0xE009, 0.1, "V", None)
    BOOST_RECOV_VOLTS = Register(0xE00A, 0.1, "V", None)
    DISCH_RECOV_VOLTS = Register(0xE00B, 0.1, "V", None)
    UNDER_WARN_VOLT   = Register(0xE00C, 0.1, "V", None)
    OVER_DISCH_VOLTS  = Register(0xE00D, 0.1, "V", None)
    DISCH_WARN_VOLTS  = Register(0xE00E, 0.1, "V", None)
    BOOST_TIME        = Register(0xE012,   1, "",  None)


class Controller(object):

    def __init__(self, device='/dev/ttyUSB0', debug=False):
        self.renogy = minimalmodbus.Instrument(device, 1)
        self.renogy.serial.baudrate = 9600
        self.renogy.serial.bytesize = 8
        self.renogy.serial.parity = serial.PARITY_NONE
        self.renogy.serial.stopbits = 1
        self.renogy.serial.timeout = 2
        self.renogy.debug = debug

    def get(self, attr: Attribute):
        value = float(self.renogy.read_register(attr.address)) * attr.scale
        return attr.function(int(value)) if attr.function else round(value, 2)

    def get_all(self, attrs=Attribute):
        values = { attr.name.lower() : self.get(attr) for attr in attrs }
        values['timestamp'] = int(time.time())
        return values


def configure():
    parser = argparse.ArgumentParser(description='Renogy charge controller monitor')
    parser.add_argument('--device', '-d', default='/dev/ttyUSB0', help='Serial device')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose modbus output')
    return parser.parse_args()


def main():
    args = configure()
    controller = Controller(args.device, args.verbose)
    print(json.dumps(controller.get_all()))

    return 0


if __name__ == "__main__":
    ret = main()
    sys.exit(ret)

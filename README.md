# solarshed

## Renogy Wanderer RS232

### RJ12 Pinout

The 6 pins on the RJ12 connector are `TX | RX | GND | GND | PWR | PWR` from left to right. You should also be able to identify the orientation by measuring ~+5.65V from `TX` to `GND` and ~+15V from `PWR` to `GND`. Only `TX`, `RX`, and `GND` will need to be connected to the serial port for monitoring the charge controller.

| DB9 Pin | RJ12 Pin |
| --- | --- |
| 1 (DC) | - |
| 2 (RX) | 1 (TX) |
| 3 (TX) | 2 (RX) |
| 4 (DT) | - |
| 5 (GND) | 3 (GND) |
| 6 (DSR) | - |
| 7 (RTS) | - |
| 8 (CTS) | - |
| 9 (RI) | - |

### Renogy Modbus 

| Attribute | Address | Scale | Units | Notes |
| --- | --- | --- | --- | --- |
| SYS\_MAX\_VOLTS | 0x00A | 1 | V | High order byte |
| SYS\_MAX\_AMPS | 0x00A | 1 | A | Low order byte |
| SYS\_MAX\_DISCHARGE | 0x00B | 1 | A | High order byte |
| SYS\_TYPE | 0x00B | 1 |  | -
| BATT\_SOC | 0x100 | 1 | % | -
| BATT\_VOLTS | 0x101 | 0.1 | V | -
| CHARGING\_AMPS | 0x102 | 0.01 | A | -
| CONTROLLER\_TEMP | 0x103 | 1 | C | -
| LOAD\_WATTS | 0x106 | 1 | W | -
| PANEL\_VOLTS | 0x107 | 0.1 | V | -
| PANEL\_AMPS | 0x108 | 0.01 | A | -
| PANEL\_WATTS | 0x109 | 1 | W | -
| BATT\_MIN\_VOLTS | 0x10B | 0.1 | V | -
| BATT\_MAX\_VOLTS | 0x10C | 0.1 | V | -
| DAY\_CHARGE | 0x10F | 1 | W | -
| DAY\_DISCHARGE | 0x110 | 1 | W | -
| DAY\_GEN\_POWER | 0x113 | 1 | W | -
| DAY\_CON\_POWER | 0x114 | 1 | W | -
| UPTIME\_DAYS | 0x115 | 1 |  | -
| BATT\_FULL\_COUNT | 0x117 | 1 |  | -
| CHARGING\_STATE | 0x120 | 1 |  | -
| BATT\_CAPACITY | 0xE002 | 1 | W | -
| SYS\_BATT\_VOLTS | 0xE003 | 1 | V | -
| RECON\_BATT\_VOLTS | 0xE003 | 1 | V | -
| BATT\_TYPE | 0xE004 | 1 |  | -
| OVER\_VOLTS | 0xE005 | 0.1 | V | -
| CHARGE\_VOLTS | 0xE006 | 0.1 | V | -
| EQUALIZE\_VOLTS | 0xE007 | 0.1 | V | -
| BOOST\_VOLTS | 0xE008 | 0.1 | V | -
| FLOAT\_VOLTS | 0xE009 | 0.1 | V | -
| BOOST\_RECOV\_VOLTS | 0xE00A | 0.1 | V | -
| DISCH\_RECOV\_VOLTS | 0xE00B | 0.1 | V | -
| UNDER\_WARN\_VOLT | 0xE00C | 0.1 | V | -
| OVER\_DISCH\_VOLTS | 0xE00D | 0.1 | V | -
| DISCH\_WARN\_VOLTS | 0xE00E | 0.1 | V | -
| BOOST\_TIME | 0xE012 | 1 |  | -

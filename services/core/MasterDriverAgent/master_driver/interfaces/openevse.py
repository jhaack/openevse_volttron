
# Copyright (c) 2015, Battelle Memorial Institute
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are those
# of the authors and should not be interpreted as representing official policies,
# either expressed or implied, of the FreeBSD Project.
#
# This material was prepared as an account of work sponsored by an
# agency of the United States Government.  Neither the United States
# Government nor the United States Department of Energy, nor Battelle,
# nor any of their employees, nor any jurisdiction or organization
# that has cooperated in the development of these materials, makes
# any warranty, express or implied, or assumes any legal liability
# or responsibility for the accuracy, completeness, or usefulness or
# any information, apparatus, product, software, or process disclosed,
# or represents that its use would not infringe privately owned rights.
#
# Reference herein to any specific commercial product, process, or
# service by trade name, trademark, manufacturer, or otherwise does
# not necessarily constitute or imply its endorsement, recommendation,
# r favoring by the United States Government or any agency thereof,
# or Battelle Memorial Institute. The views and opinions of authors
# expressed herein do not necessarily state or reflect those of the
# United States Government or any agency thereof.
#
# PACIFIC NORTHWEST NATIONAL LABORATORY
# operated by BATTELLE for the UNITED STATES DEPARTMENT OF ENERGY
# under Contract DE-AC05-76RL01830

# Some functions also contributed by:
# The MIT License (MIT)
#
# Copyright (c) 2015 Sebastien Maccagnoni-Munch <seb+pyopenevse@maccagnoni.eu>


import random
import datetime
from math import sin, pi
import serial
import threading
import time

from master_driver.interfaces import BaseInterface, BaseRegister, BasicRevert
from volttron.platform.agent.utils import format_timestamp, parse_timestamp_string
from csv import DictReader
from StringIO import StringIO
import logging

_log = logging.getLogger(__name__)

def str_bool(value):
    if isinstance(value, int):
        return bool(value)
    else:
        return value.lower().strip() == 'true'

type_mapping = {"string": str,
                "int": int,
                "integer": int,
                "float": float,
                "bool": str_bool,
                "boolean": str_bool}

#Initializations taken from MIT license defined farther below
STANDARD_SERIAL_TIMEOUT = 0.5
RESET_SERIAL_TIMEOUT = 10
CORRECT_RESPONSE_PREFIXES = ('$OK', '$ST', '$NK')

class EvseError(Exception):
    pass

class EvseTimeoutError(EvseError):
    pass

class EvseStateChangeError(EvseError):
    pass

class EVSE_reg(BaseRegister):
    def __init__(self, read_only, pointName, units, read_command, write_command, reg_function, reg_type, default_value=None, description=''):
        super(EVSE_reg, self).__init__("byte", read_only, pointName, units, description='')
        self.reg_type = reg_type
        self.read_command = read_command
        self.write_command = write_command
        self.reg_function = reg_function

        if default_value == None:
            self.value = None
        else:
            try:
                # self.value = map(self.reg_type, default_value)
                self.value = self.reg_type(default_value)
            except ValueError:
                self.value = self.reg_type()

class Interface(BasicRevert, BaseInterface):
    def __init__(self, **kwargs):
        super(Interface, self).__init__(**kwargs)
        self.function_map = {}

        #Dictionaries for selecting register functions and bit flags
        self.set_functions = {"EVSE_Enable": self.evse_enable,
                         "Reset": self.reset,
                         "Sleep": self.sleep,
                         "Restart": self.restart_port,
                         "Datetime": self.evse_datetime_set,
                         "GFI": self.gfi_enable,
                         "Timer": self.timer_set}

        self.get_functions = {"Datetime": self.evse_datetime_get,
                         "Capacity": self.capacity,
                         "Service": self.service}

        self.setting_flags = {"L2": 0x0001,
                         "Diode": 0x0002,
                         "Vent": 0x0004,
                         "Ground": 0x0008,
                         "Relay": 0x0010,
                         "LA_Disabled": 0x0020,
                         "Autostart_Disabled": 0x0040,
                         "Serial_Debug": 0x0080,
                         "LCD": 0x0100,
                         "GFI": 0x0200,
                         "Temp": 0x0400}

    def configure(self, config_dict, registry_config_str):
        self.port=config_dict["serial_port"]
        self.baud_rate = config_dict.get("baud_rate", 115200)
        self.callback = config_dict.get("status_callback")
        self.status = None
        self.parse_config(registry_config_str)

        self.s = serial.Serial(port=self.port, baudrate=self.baud_rate,
                               timeout=STANDARD_SERIAL_TIMEOUT)

        #Initialize device
        try:
            #Collect device states
            state_register = self.get_register_by_function('State')
            self.get_point(state_register.point_name) #Get state to update state registers

            #Enable ammeter calibration
            ammeter_register = self.get_register_by_function('Ammeter')
            self._silent_request(ammeter_register.write_command, '1')

            #Disable echo
            echo_register = self.get_register_by_function('Echo')
            self._silent_request(echo_register.write_command, '0')
        except:
            raise EvseError

    def get_point(self, point_name):
        register = self.get_register_by_name(point_name)

        if register.read_command == 'Value':
            return register.value
        elif register.reg_function in self.get_functions:
            return self.get_functions[register.reg_function]()
        elif register.reg_function in self.setting_flags:
            return self.settings(register.point_name)
        else:
            request = register.read_command

            response = self._get_request(request)

            response = map(register.reg_type, response[1])

            if register.reg_function == 'State':
                self.state_change(point_name, response=response)

            return response

    def _set_point(self, point_name, value):
        register = self.get_register_by_name(point_name)
        if register.read_only:
            raise IOError("Trying to write to a point configured read only: " + point_name)

        #Several registers have special functions involved in processes
        if register.reg_function in self.set_functions:
            response = self.set_functions[register.reg_function](value)
        else:
            write_command = register.write_command
            if isinstance(value, list):
                request = write_command + ' ' + ' '.join(str(x) for x in value)
            elif isinstance(value, bool):
                request = write_command + ' ' + str(int(value))
            else:
                request = write_command + ' ' + str(value)
            response = self._set_request(request)[0]

        if isinstance(value, list):
            value = map(register.reg_type, value)
        else:
            value = register.reg_type(value)

        # If response shows confirmation, update value registers and states.
        if response in CORRECT_RESPONSE_PREFIXES[:2] and register.read_command == 'Value':

            if register.reg_function in ['Reset', 'EVSE_Enable', 'Color']:
                self.state_change(point_name, value=value)
            else:
                register.value = value

            return [response, register.value]

        # For registers read command goes to OpenEVSE control board, or if command failed, just report what was sent.
        else:
            return [response, value]

    def _scrape_all(self):
        result = {}
        write_registers = self.get_registers_by_type("byte", False)
        read_registers = self.get_registers_by_type("byte", True)
        for register in write_registers + read_registers:
            result[register.point_name] = self.get_point(register.point_name)
        return result
        return 0

    def parse_config(self, config_string):
        if config_string is None:
            return

        f = StringIO(config_string)

        configDict = DictReader(f)

        for regDef in configDict:

            read_only = regDef['Writable'].lower() != 'true'
            point_name = regDef['Volttron Point Name']
            description = regDef.get('Notes', '')
            units = regDef['Units']
            read_command = regDef['Read']
            write_command = regDef.get('Write', '')
            reg_function = regDef.get('Function', '')
            default_value = regDef.get('Starting Value', '').strip()
            if not default_value:
                default_value = None
            unit_type = regDef['Unit Type']
            reg_type = type_mapping.get(unit_type, str)

            register_type = EVSE_reg

            register = register_type(
                read_only,
                point_name,
                units,
                read_command,
                write_command,
                reg_function,
                reg_type,
                default_value=default_value,
                description=description)

            if default_value is not None:
                self.set_default(point_name, register.value)

            self.function_map[reg_function] = register
            self.insert_register(register)

    def get_register_by_function(self, function):
        return self.function_map[function]

    def state_change(self, point_name, response = None, value = None):
        """A function for all the conditionals associated with keeping track of state changes and registers"""

        register = self.get_register_by_name(point_name)

        #If a get_point on state is being called, update all state registers
        if register.reg_function == 'State':
            state = response[0]

            #Device is enabled and awake
            if state >= 0 and state <= 10:

                sleep_register = self.get_register_by_function('Sleep')

                sleep_register.value = False

                enable_register = self.get_register_by_function('EVSE_Enable')
                enable_register.value = True


            #Device is asleep
            elif state == 254:
                sleep_register = self.get_register_by_function('Sleep')
                sleep_register.value = True

                enable_register = self.get_register_by_function('EVSE_Enable')
                enable_register.value = True

            #Device is disabled
            elif state == 255:
                sleep_register = self.get_register_by_function('Sleep')
                sleep_register.value = False

                enable_register = self.get_register_by_function('EVSE_Enable')
                enable_register.value = False
            else:
                raise EvseStateChangeError

        #If a state change has been called, update other states (sleeping does not affect other states)
        elif register.reg_function in ['Reset', 'EVSE_Enable']:
            sleep_register = self.get_register_by_function('Sleep')
            sleep_register.value = False

            # If a reset has been successfully completed, return reset value to 0 and set state registers
            if register.reg_function == 'Reset':
                enable_register = self.get_register_by_function('EVSE_Enable')
                enable_register.value = True
                reset_register = self.get_register_by_function('Reset')
                reset_register.value = False
            else:
                enable_register = self.get_register_by_function('EVSE_Enable')
                enable_register.value = enable_register.reg_type(value)

        # If the set_point was to restart port, conclude restart by setting register to 0
        elif register.reg_function == 'Restart':
            restart_register = self.get_register_by_function('Restart')
            restart_register.value = restart_register.reg_type(False)

        # If the set_point was for color and the state is charging, the color will revert to teal (6)
        elif register.reg_function == 'Color':
            state_register = self.get_register_by_function('State')
            state = self._set_request(state_register.read_command)
            if state[1][0] == '3':
                register.value = 6
            else:
                register.value = map(register.reg_type, value)
        return

    def evse_enable(self, value):
        """Setting EVSE_Enable register"""

        value = bool(value)

        #To do: have a 0 set to evse_enable put device to sleep. Replace EVSE_sleep with a EVSE_disable point

        register = self.get_register_by_function('EVSE_Enable')

        if value:
            request = register.write_command[-2:]
        else:
            request = register.write_command[:2]

        return self._set_request(request)[0]


    def sleep(self, value):
        """Setting Sleep register"""

        value = bool(value)

        #Cannot wake up OpenEVSE using this register. Use EVSE_enable
        if not value:
            raise EvseError

        register = self.get_register_by_function('Sleep')
        request = register.write_command

        return self._set_request(request)[0]

    def restart_port(self, value):
        """Setting Restart register to restart the serial port"""

        value = bool(value)

        if not value:
            raise EvseError

        register = self.get_register_by_function('Restart')

        #Set register to 1 while restarting
        register.value = 1

        try:
            self.s.close()

            self.s = serial.Serial(port=self.port, baudrate=self.baud_rate,
                                   timeout=STANDARD_SERIAL_TIMEOUT)
            return '$OK'

        except:
            return '$NK'
            # raise EvseError

    def evse_datetime_set(self, value):
        """Getting datetime object"""

        register = self.get_register_by_function('Datetime')

        evse_datetime = parse_timestamp_string(value)

        #pluck numbers out of datetime object
        year = str(evse_datetime.year)[-2:]
        month = str(evse_datetime.month)
        day = str(evse_datetime.day)
        hour = str(evse_datetime.hour)
        minute = str(evse_datetime.minute)
        second = str(evse_datetime.second)

        return self._set_request(register.write_command, year, month, day, hour, minute, second)

    def gfi_enable(self, value):
        """There are two redundant GFI enable commands to send. Set them both as one."""

        value = str(int(value))

        register = self.get_register_by_function('GFI')

        confirm_1 = self._set_request(register.write_command[:2], value)[0]
        confirm_2 = self._set_request(register.write_command[-2:], value)[0]

        if confirm_1 == '$OK' and confirm_2 == '$OK':
            result = '$OK'
        else:
            result = '$NK'

        return result

    def timer_set(self, value):
        """Setting the charge timer"""

        register = self.get_register_by_function('Timer')

        start_hour = value[0][:2]
        start_minute = value[0][3:5]
        end_hour = value[1][:2]
        end_minute = value[1][3:5]

        return self._set_request(register.write_command, start_hour, start_minute, end_hour, end_minute)[0]


    def evse_datetime_get(self):
        """Getting datetime object"""

        register = self.get_register_by_function('Datetime')

        response = self._get_request(register.read_command)
        response = map(int, response[1]) #To do: update this to use string format to datetime function

        evse_time = datetime.datetime(response[0] + 2000, response[1], response[2], response[3], response[4],
                                      response[5])

        return format_timestamp(evse_time)

    def capacity(self):
        """Getting current capacity from settings"""
        register = self.get_register_by_function('Capacity')

        return self._get_request(register.read_command)[1][0]

    def service(self):
        """Getting the service level the charger is currently operating"""

        register = self.get_register_by_function('Service')

        settings = '0x' + self._get_request(register.read_command)[1][1]

        bit_flag_L2 = bool(int(settings, 16) & self.setting_flags['L2'])
        bit_flag_notA = bool(int(settings, 16) & self.setting_flags['LA_Disabled'])

        if bit_flag_notA:
            if bit_flag_L2:
                return '2'
            else:
                return '1'
        else:
            return 'A'

    def settings(self, point_name):
        """Function to retrieve device settings and locate desired bit. bit_flag shows if a setting has departed from default"""
        register = self.get_register_by_name(point_name)

        settings = '0x' + self._get_request(register.read_command)[1][1]
        bit_flag = bool(int(settings, 16) & self.setting_flags[register.reg_function])

        return not bit_flag

#Everything below this line has been taken and/or adapted from the following MIT license:

# The MIT License (MIT)
#
# Copyright (c) 2015 Sebastien Maccagnoni-Munch <seb+pyopenevse@maccagnoni.eu>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

    def _silent_request(self, *args):
        """Send a request, do not read its response"""

        command = '$' + ' '.join(args)

        checksum = 0
        for i in bytearray(command):
            checksum ^= i
        checksum = format(checksum, '02X')
        request = command + '^' + checksum + '\r'

        self.s.write(request)

    def _set_request(self, *args):
        """Send a requests, wait for its response. Designed for set_point"""

        self._silent_request(*args)
        return self._get_response()

    def _get_request(self, *args):
        """Send a requests, wait for its response, ignoring $ST and blank responses. designed for get_point"""

        self._silent_request(*args)

        response = ['$ST', []]
        attempts = 100

        # Ensure any state changes are resolved before allowing read points
        while response[0] == '$ST' or (response[0] == '$OK' and response[1] == []):
            response = self._get_response()
            if not (attempts):
                raise EvseStateChangeError
            attempts = attempts - 1

        return response

    def _get_response(self):
        """Get the response of a command."""

        response = self._read_line()

        if response[:3] in CORRECT_RESPONSE_PREFIXES:
            response = response.split()
            if response[0] == '$ST':
                response[1] = int('0x' + response[1],16)
            return (response[0], response[1:])

    def _read_line(self):
        """Read a line from the serial port."""
        line = ''
        while True:
            c = self.s.read()
            if c == '':
                raise EvseTimeoutError
            line += c
            if c == '\r':
                break
        return line

    def reset(self, value):
        """Reset the OpenEVSE"""

        value = bool(value)

        register = self.get_register_by_function('Reset')

        if not value:
            raise EvseError

        self._silent_request(register.write_command)

        #Set register to True while resetting
        register.value = True

        # Give the OpenEVSE at most RESET_SERIAL_TIMEOUT seconds to reboot
        self.s.timeout = RESET_SERIAL_TIMEOUT
        # Read the next received line, which should start with "ST"
        line = self._read_line()
        self.s.timeout = STANDARD_SERIAL_TIMEOUT

        if line[:3] in CORRECT_RESPONSE_PREFIXES[:2]:
            time.sleep(7)  # Let the OpenEVSE finish its boot sequence
            return '$OK'
        else:
            raise EvseError

    def __del__(self):
        """Destructor"""
        self.s.close()
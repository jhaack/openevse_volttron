from __future__ import absolute_import

import datetime
import logging
import sys
import serial
import threading
import time
#import openevse

from volttron.platform.vip.agent import Agent, Core
from volttron.platform.agent import utils
from volttron.platform.agent import openevse

utils.setup_logging()
_log = logging.getLogger(__name__)

STANDARD_SERIAL_TIMEOUT = 0.5
CORRECT_RESPONSE_PREFIXES = ('$OK', '$NK')

class EvseError(Exception):
    pass
class EvseTimeoutError(EvseError):
    pass


class TestAgent(Agent):
    def __init__(self, config_path, **kwargs):
        super(TestAgent, self).__init__(**kwargs)

        config = utils.load_config(config_path)
        self.agent_id = config['agentid']

        
    @Core.receiver("onstart")
    def starting(self, sender, **kwargs):

        # self.disable_start_tests()
        # self.enable_start_tests()
        self.state_sequence()
        # self.test_timer()
        # self.test_write()

        return

    def disable_start_tests(self):

        # Schedule time
        try:
            start = str(datetime.datetime.now())
            end = str(datetime.datetime.now() + datetime.timedelta(minutes=1))

            msg = [
                ['campus/ETB/OpenEVSE_Test1', start, end]
            ]
            result = self.vip.rpc.call(
                'platform.actuator',
                'request_new_schedule',
                self.agent_id,
                "some task",
                'LOW',
                msg).get(timeout=10)
            print("schedule result", result)
        except Exception as e:
            print ("Could not contact actuator. Is it running?")
            print(e)
            return

        # if result was success, perform actions
        if result['result'] == 'SUCCESS':

            # Get settings
            try:
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'get_point',
                    'campus/ETB/OpenEVSE_Test1/settings').get(timeout=10)
                print("Got result", result)
            except Exception as e:
                print ("Could not contact actuator. Is it running?")
                print(e)
                return

            # Clear tests
            try:
                point_name = 'diode_check_enable'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    '0').get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Expected to fail since there is no real device to set")
                print(e)

            try:
                point_name = 'GFI_self_test_enable'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    '0').get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Expected to fail since there is no real device to set")
                print(e)

            try:
                point_name = 'ground_check_enable'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    '0').get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Expected to fail since there is no real device to set")
                print(e)

            try:
                point_name = 'stuck_relay_check_enable'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    '0').get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Expected to fail since there is no real device to set")
                print(e)

            try:
                point_name = 'vent_required_enable'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    '0').get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Expected to fail since there is no real device to set")
                print(e)

            # Get settings
            try:
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'get_point',
                    'campus/ETB/OpenEVSE_Test1/settings').get(timeout=10)
                print("Got result", result)
            except Exception as e:
                print ("Could not contact actuator. Is it running?")
                print(e)
                return

            # Reset device
            try:
                point_name = 'EVSE_reset'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    '1').get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Expected to fail since there is no real device to set")
                print(e)

        # Canceling the scheduled actuator
        try:
            msg = [
                ['campus/ETB/OpenEVSE_Test1', start, end]
            ]
            result = self.vip.rpc.call(
                'platform.actuator',
                'request_cancel_schedule',
                self.agent_id,
                "some task").get(timeout=10)
            print("schedule cancel result", result)
        except Exception as e:
            print ("Could not contact actuator. Is it running?")
            print(e)
            return

        return

    def enable_start_tests(self):

        # Schedule time
        try:
            start = str(datetime.datetime.now())
            end = str(datetime.datetime.now() + datetime.timedelta(minutes=1))

            msg = [
                ['campus/ETB/OpenEVSE_Test1', start, end]
            ]
            result = self.vip.rpc.call(
                'platform.actuator',
                'request_new_schedule',
                self.agent_id,
                "some task",
                'LOW',
                msg).get(timeout=10)
            print("schedule result", result)
        except Exception as e:
            print ("Could not contact actuator. Is it running?")
            print(e)
            return

        # if result was success, perform actions
        if result['result'] == 'SUCCESS':

            # Get settings
            try:
                point_name = 'settings'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'get_point',
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name])).get(timeout=10)
                print("Got result", point_name, result)
            except Exception as e:
                print ("Could not contact actuator. Is it running?")
                print(e)
                return

            # Clear tests
            try:
                point_name = 'diode_check_enable'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    '1').get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Expected to fail since there is no real device to set")
                print(e)

            try:
                point_name = 'GFI_self_test_enable'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    '1').get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Expected to fail since there is no real device to set")
                print(e)

            try:
                point_name = 'ground_check_enable'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    '1').get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Expected to fail since there is no real device to set")
                print(e)

            try:
                point_name = 'stuck_relay_check_enable'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    '1').get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Expected to fail since there is no real device to set")
                print(e)

            try:
                point_name = 'vent_required_enable'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    '1').get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Expected to fail since there is no real device to set")
                print(e)

            # Get settings
            try:
                point_name = 'settings'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'get_point',
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name])).get(timeout=10)
                print("Got result", point_name, result)
            except Exception as e:
                print ("Could not contact actuator. Is it running?")
                print(e)
                return

            # Reset device
            try:
                point_name = 'EVSE_reset'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    '1').get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Expected to fail since there is no real device to set")
                print(e)

        # Canceling the scheduled actuator
        try:
            msg = [
                ['campus/ETB/OpenEVSE_Test1', start, end]
            ]
            result = self.vip.rpc.call(
                'platform.actuator',
                'request_cancel_schedule',
                self.agent_id,
                "some task").get(timeout=10)
            print("schedule cancel result", result)
        except Exception as e:
            print ("Could not contact actuator. Is it running?")
            print(e)
            return

        return

    def state_sequence(self):
        """Run through several states of device"""

        #Schedule time
        try:
            start = str(datetime.datetime.now())
            end = str(datetime.datetime.now() + datetime.timedelta(minutes=1))

            msg = [
                ['campus/ETB/OpenEVSE_Test1', start, end]
            ]
            result = self.vip.rpc.call(
                'platform.actuator',
                'request_new_schedule',
                self.agent_id,
                "some task",
                'LOW',
                msg).get(timeout=10)
            print("schedule result", result)
        except Exception as e:
            print ("Could not contact actuator. Is it running?")
            print(e)
            return

        # if result was success, perform actions
        if result['result'] == 'SUCCESS':

            # Get initial state
            try:
                point_name = 'state'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'get_point',
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name])).get(timeout=10)
                print("Got result", point_name, result)
            except Exception as e:
                print ("Could not contact actuator. Is it running?")
                print(e)
                return

            # Enable
            try:
                point_name = 'EVSE_enable'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    '1').get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Expected to fail since there is no real device to set")
                print(e)

            # Get state
            try:
                point_name = 'state'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'get_point',
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name])).get(timeout=10)
                print("Got result", point_name, result)
            except Exception as e:
                print ("Could not contact actuator. Is it running?")
                print(e)
                return

            time.sleep(3)

            # Sleep
            try:
                point_name = 'EVSE_sleep'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    '1').get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Expected to fail since there is no real device to set")
                print(e)

            # Get state
            try:
                point_name = 'state'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'get_point',
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name])).get(timeout=10)
                print("Got result", point_name, result)
            except Exception as e:
                print ("Could not contact actuator. Is it running?")
                print(e)
                return

            time.sleep(3)

            # Disable
            try:
                point_name = 'EVSE_enable'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    '0').get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Expected to fail since there is no real device to set")
                print(e)

            time.sleep(3)

            # Get state
            try:
                point_name = 'state'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'get_point',
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name])).get(timeout=10)
                print("Got result", point_name, result)
            except Exception as e:
                print ("Could not contact actuator. Is it running?")
                print(e)
                return

            time.sleep(3)

            # Reset device
            try:
                point_name = 'EVSE_reset'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    '1').get(timeout=20)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Expected to fail since there is no real device to set")
                print(e)

            time.sleep(5)

            # Get state
            try:
                point_name = 'state'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'get_point',
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name])).get(timeout=10)
                print("Got result", point_name, result)
            except Exception as e:
                print ("Could not contact actuator. Is it running?")
                print(e)
                return

        # Canceling the scheduled actuator
        try:
            msg = [
                ['campus/ETB/OpenEVSE_Test1', start, end]
            ]
            result = self.vip.rpc.call(
                'platform.actuator',
                'request_cancel_schedule',
                self.agent_id,
                "some task").get(timeout=10)
            print("schedule cancel result", result)
        except Exception as e:
            print ("Could not contact actuator. Is it running?")
            print(e)
            return

        return

    def test_timer(self):

        #Schedule time
        try:
            start = str(datetime.datetime.now())
            end = str(datetime.datetime.now() + datetime.timedelta(minutes=3))

            msg = [
                ['campus/ETB/OpenEVSE_Test1', start, end]
            ]
            result = self.vip.rpc.call(
                'platform.actuator',
                'request_new_schedule',
                self.agent_id,
                "some task1",
                'LOW',
                msg).get(timeout=10)
            print("schedule result", result)
        except Exception as e:
            print ("Could not contact actuator. Is it running?")
            print(e)
            return


        ##If schedule went through, set points on the device
        if result['result']=='SUCCESS':

            # Measure timer
            try:
                point_name = 'timer'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'get_point',
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name])).get(timeout=10)
                print("Got result", point_name, result)
            except Exception as e:
                print ("Could not contact actuator. Is it running?")
                print(e)
                return

            # Get current time
            try:
                point_name = 'clock'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'get_point',
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name])).get(timeout=10)
                print("Got result", point_name, result)
            except Exception as e:
                print ("Could not contact actuator. Is it running?")
                print(e)
                return

            #Use current time to set 2-minute timer starting in 1 minute
            hour = result[11:13]
            startminute = str(int(result[14:16])+1)
            endminute = str(int(result[14:16])+3)

            argument = ' '.join([hour,startminute,hour,endminute])

            # Set timer
            try:
                point_name = 'timer'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    argument).get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Expected to fail since there is no real device to set")
                print(e)

            # Put device to sleep
            try:
                point_name = 'EVSE_sleep'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    '1').get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Expected to fail since there is no real device to set")
                print(e)

            time.sleep(5)

            # Wait one minute for device to enter charge state
            time.sleep(60)

            # Attempt to put device to sleep
            try:
                point_name = 'EVSE_sleep'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    '1').get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Expected to fail since there is no real device to set")
                print(e)

            # Clear timer
            try:
                point_name = 'timer'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    '0 0 0 0').get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Expected to fail since there is no real device to set")
                print(e)

        # Canceling the scheduled actuator
        try:
            start = str(datetime.datetime.now())
            end = str(datetime.datetime.now() + datetime.timedelta(minutes=1))

            msg = [
                ['campus/ETB/OpenEVSE_Test1', start, end]
            ]
            result = self.vip.rpc.call(
                'platform.actuator',
                'request_cancel_schedule',
                self.agent_id,
                "some task1").get(timeout=10)
            print("schedule cancel result", result)
        except Exception as e:
            print ("Could not contact actuator. Is it running?")
            print(e)
            return

        return

    def test_write(self):

        #Schedule time
        try:
            start = str(datetime.datetime.now())
            end = str(datetime.datetime.now() + datetime.timedelta(minutes=1))

            msg = [
                ['campus/ETB/OpenEVSE_Test1', start, end]
            ]
            result = self.vip.rpc.call(
                'platform.actuator',
                'request_new_schedule',
                self.agent_id,
                "some task",
                'LOW',
                msg).get(timeout=10)
            print("schedule result", result)
        except Exception as e:
            print ("Could not contact actuator. Is it running?")
            print(e)
            return


        ##If schedule went through, set points on the device
        if result['result']=='SUCCESS':

            point_name = 'clock'

            # Measure point
            try:
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'get_point',
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name])).get(timeout=10)
                print("Got result", point_name, result)
            except Exception as e:
                print ("Could not contact actuator. Is it running?")
                print(e)
                return

            # Set point
            try:
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    '16 9 9 1 30 00').get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Expected to fail since there is no real device to set")
                print(e)

            time.sleep(5)

            # Measure point
            try:
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'get_point',
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name])).get(timeout=10)
                print("Got result", point_name, result)
            except Exception as e:
                print ("Could not contact actuator. Is it running?")
                print(e)
                return
        # Canceling the scheduled actuator
        try:
            msg = [
                ['campus/ETB/OpenEVSE_Test1', start, end]
            ]
            result = self.vip.rpc.call(
                'platform.actuator',
                'request_cancel_schedule',
                self.agent_id,
                "some task").get(timeout=10)
            print("schedule cancel result", result)
        except Exception as e:
            print ("Could not contact actuator. Is it running?")
            print(e)
            return

        return


def main(argv=sys.argv):     
    '''Main method called by the eggsecutable.'''
    try:
        utils.vip_main(TestAgent)
    except Exception as e:
        _log.exception(e)

if __name__ == '__main__':
    # Entry point for script
    sys.exit(main())
                     

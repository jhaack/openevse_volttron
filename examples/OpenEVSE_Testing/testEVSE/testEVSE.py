from __future__ import absolute_import

import datetime
import logging
import sys
import serial
import threading
import time

from volttron.platform.vip.agent import Agent, Core
from volttron.platform.agent.utils import format_timestamp, parse_timestamp_string
from volttron.platform.agent import utils
from volttron.platform.agent import openevse

utils.setup_logging()
_log = logging.getLogger(__name__)

CORRECT_RESPONSE_PREFIXES = ('$OK', '$NK')


class TestAgent(Agent):
    def __init__(self, config_path, **kwargs):
        super(TestAgent, self).__init__(**kwargs)

        config = utils.load_config(config_path)
        self.agent_id = config['agentid']

    @Core.receiver("onstart")
    def starting(self, sender, **kwargs):


        # self.EV_vary_current()
        # self.EV_respond_signal()
        # self.disable_start_tests() DO NOT USE WHEN EVSE PLUGGED IN. USE ONLY WHEN TESTING DISCONNECTED FROM WALL
        # self.enable_start_tests()
        # self.state_sequence()
        # self.test_timer()
        # self.test_write()


        return

    def EV_vary_current(self):

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

            # Put device to sleep
            try:
                point_name = 'EVSE_sleep'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    True).get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Expected to fail since there is no real device to set")
                print(e)

            # Set service level
            try:
                point_name = 'service_level'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    '2').get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Expected to fail since there is no real device to set")
                print(e)

            # Set current
            try:
                point_name = 'current_capacity'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    6).get(timeout=15)
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

        self.enable_start_tests()

        # Schedule time
        try:
            start = str(datetime.datetime.now())
            end = str(datetime.datetime.now() + datetime.timedelta(minutes=5))

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

            # Get current
            try:
                point_name = 'current_voltage'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'get_point',
                    ''.join(['campus/ETB/OpenEVSE_Test1/', point_name])).get(timeout=10)
                print("Got result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
                print(e)
                return

            time.sleep(15)

            # Increase current_capacity
            try:
                point_name = 'current_capacity'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/', point_name]),
                    12).get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
                print(e)

            # Get current
            try:
                point_name = 'current_voltage'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'get_point',
                    ''.join(['campus/ETB/OpenEVSE_Test1/', point_name])).get(timeout=10)
                print("Got result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
                print(e)
                return

            time.sleep(15)

            # Increase current_capacity
            try:
                point_name = 'current_capacity'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    18).get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
                print(e)

            # Get current
            try:
                point_name = 'current_voltage'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'get_point',
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name])).get(timeout=10)
                print("Got result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
                print(e)
                return

            time.sleep(15)

            # Increase current_capacity
            try:
                point_name = 'current_capacity'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/', point_name]),
                    24).get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
                print(e)

            # Get current
            try:
                point_name = 'current_voltage'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'get_point',
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name])).get(timeout=10)
                print("Got result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
                print(e)
                return

            time.sleep(15)

            # Put device to sleep
            try:
                point_name = 'EVSE_sleep'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/', point_name]),
                    True).get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
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

    def EV_respond_signal(self):

        # Schedule time
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

            # Put device to sleep
            try:
                point_name = 'EVSE_sleep'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    True).get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
                print(e)

            #Begin counter sequence
            for time_count in range(1, 70):

                if time_count == 30:

                    # Begin charging
                    try:
                        point_name = 'EVSE_enable'
                        result = self.vip.rpc.call(
                            'platform.actuator',
                            'set_point',
                            self.agent_id,
                            ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                            True).get(timeout=15)
                        print("Set result", point_name, result)
                    except Exception as e:
                        print ("Device Communication Failure")
                        print(e)

                elif time_count == 33 or time_count == 63:

                    # Show message received
                    try:
                        point_name = 'print_text'
                        result = self.vip.rpc.call(
                            'platform.actuator',
                            'set_point',
                            self.agent_id,
                            ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                            '0 0 TranxSigRcvd').get(timeout=15)
                        print("Set result", point_name, result)
                    except Exception as e:
                        print ("Device Communication Failure")
                        print(e)

                elif time_count == 60:

                    # Stop Charging
                    try:
                        point_name = 'EVSE_sleep'
                        result = self.vip.rpc.call(
                            'platform.actuator',
                            'set_point',
                            self.agent_id,
                            ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                            True).get(timeout=15)
                        print("Set result", point_name, result)
                    except Exception as e:
                        print ("Device Communication Failure")
                        print(e)

                time.sleep(1)

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
                point_name = 'settings'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'get_point',
                    ''.join(['campus/ETB/OpenEVSE_Test1/', point_name])).get(timeout=10)
                print("Got result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
                print(e)
                return

            # Clear tests
            try:
                point_name = 'diode_check_enable'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/', point_name]),
                    False).get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
                print(e)

            try:
                point_name = 'GFI_self_test_enable'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/', point_name]),
                    False).get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
                print(e)

            try:
                point_name = 'ground_check_enable'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/', point_name]),
                    False).get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
                print(e)

            try:
                point_name = 'stuck_relay_check_enable'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/', point_name]),
                    False).get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
                print(e)

            try:
                point_name = 'vent_required_enable'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/', point_name]),
                    False).get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
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
                print ("Device Communication Failure")
                print(e)
                return

            # Reset device
            try:
                point_name = 'EVSE_reset'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/', point_name]),
                    True).get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
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
                print ("Device Communication Failure")
                print(e)
                return

            # Enable tests
            try:
                point_name = 'diode_check_enable'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    True).get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
                print(e)

            try:
                point_name = 'GFI_self_test_enable'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    True).get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
                print(e)

            try:
                point_name = 'ground_check_enable'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    True).get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
                print(e)

            try:
                point_name = 'stuck_relay_check_enable'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    True).get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
                print(e)

            try:
                point_name = 'vent_required_enable'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    True).get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
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
                print ("Device Communication Failure")
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
                    True).get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
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
                print ("Device Communication Failure")
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
                    True).get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
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
                print ("Device Communication Failure")
                print(e)
                return

            time.sleep(5)

            # Sleep
            try:
                point_name = 'EVSE_sleep'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    True).get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
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
                print ("Device Communication Failure")
                print(e)
                return

            time.sleep(5)

            # Disable
            try:
                point_name = 'EVSE_enable'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    False).get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
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
                print ("Device Communication Failure")
                print(e)
                return

            time.sleep(5)

            # Reset device
            try:
                point_name = 'EVSE_reset'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    True).get(timeout=20)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
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
                print ("Device Communication Failure")
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

            # Measure timer
            try:
                point_name = 'timer'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'get_point',
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name])).get(timeout=10)
                print("Got result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
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
                print ("Device Communication Failure")
                print(e)
                return

            #Use current time to set 2-minute timer starting in 1 minute
            evse_datetime = parse_timestamp_string(result)

            hour = evse_datetime.hour
            startminute = evse_datetime.minute + 1
            endminute = evse_datetime.minute + 3

            timer1 = str(datetime.time(hour, startminute))
            timer2 = str(datetime.time(hour, endminute))

            # Set timer
            try:
                point_name = 'timer'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    [timer1, timer2]).get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
                print(e)

            # Put device to sleep
            try:
                point_name = 'EVSE_sleep'
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    1).get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
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
                print ("Device Communication Failure")
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
                print ("Device Communication Failure")
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
                "some task").get(timeout=10)
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
        if result['result'] == 'SUCCESS':

            point_name = 'clock'

            # Measure point
            try:
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'get_point',
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name])).get(timeout=10)
                print("Got result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
                print(e)
                return

            evse_datetime = format_timestamp(datetime.datetime.now())

            # Set point
            try:
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    ''.join(['campus/ETB/OpenEVSE_Test1/',point_name]),
                    evse_datetime).get(timeout=15)
                print("Set result", point_name, result)
            except Exception as e:
                print ("Device Communication Failure")
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
                print ("Device Communication Failure")
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
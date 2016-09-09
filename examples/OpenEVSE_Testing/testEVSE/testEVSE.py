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
        '''
        subscribes to the platform message bus on the heartbeat/listeneragent Topic
        '''
        print('TestAgent example agent start-up function')

        # Take a measurement from the device
        # try:
        #     result = self.vip.rpc.call(
        #         'platform.actuator',
        #         'get_point',
        #         'campus/ETB/OpenEVSE_Test1/EVSE_enable').get(timeout=10)
        #     print("Got result", result)
        # except Exception as e:
        #     print ("Could not contact actuator. Is it running?")
        #     print(e)
        #     return

        # Schedule a time slot with the device via the actuator
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

            try:
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    'campus/ETB/OpenEVSE_Test1/timer',
                    '0 0 0 0').get(timeout=15)
                print("Set result", result)
            except Exception as e:
                print ("Expected to fail since there is no real device to set")
                print(e)

            try:
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    'campus/ETB/OpenEVSE_Test1/EVSE_enable',
                    '1').get(timeout=15)
                print("Set result", result)
            except Exception as e:
                print ("Expected to fail since there is no real device to set")
                print(e)

            time.sleep(5)

            try:
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    'campus/ETB/OpenEVSE_Test1/ground_check_enable',
                    '0').get(timeout=15)
                print("Set result", result)
            except Exception as e:
                print ("Expected to fail since there is no real device to set")
                print(e)

            try:
                result = self.vip.rpc.call(
                    'platform.actuator',
                    'set_point',
                    self.agent_id,
                    'campus/ETB/OpenEVSE_Test1/EVSE_reset',
                    '1').get(timeout=15)
                print("Set result", result)
            except Exception as e:
                print ("Expected to fail since there is no real device to set")
                print(e)

            time.sleep(5)

            # try:
            #     result = self.vip.rpc.call(
            #         'platform.actuator',
            #         'set_point',
            #         self.agent_id,
            #         'campus/ETB/OpenEVSE_Test1/EVSE_sleep',
            #         '1').get(timeout=15)
            #     print("Set result", result)
            # except Exception as e:
            #     print ("Expected to fail since there is no real device to set")
            #     print(e)

        ##Canceling the scheduled actuator
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


        try:
            test_object = self.vip.rpc.call(
                'platform.actuator',
                'get_point',
                'campus/ETB/OpenEVSE_Test1/ground_check_enable').get(timeout=10)
            print("Got result", test_object)
        except Exception as e:
            print ("Could not contact actuator. Is it running?")
            print(e)
            return

        # try:
        #     result = self.vip.rpc.call(
        #         'platform.actuator',
        #         'get_point',
        #         'campus/ETB/OpenEVSE_Test1/backlight_color').get(timeout=10)
        #     print("Got result", result)
        # except Exception as e:
        #     print ("Could not contact actuator. Is it running?")
        #     print(e)
        #     return

def main(argv=sys.argv):     
    '''Main method called by the eggsecutable.'''
    try:
        utils.vip_main(TestAgent)
    except Exception as e:
        _log.exception(e)

if __name__ == '__main__':
    # Entry point for script
    sys.exit(main())
                     

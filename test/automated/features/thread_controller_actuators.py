# Copyright (c) 2020 Seagate Technology LLC and/or its Affiliates
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU Affero General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along
# with this program. If not, see <https://www.gnu.org/licenses/>. For any questions
# about this software or licensing, please email opensource@seagate.com or
# cortx-questions@seagate.com.

# -*- coding: utf-8 -*-
from lettuce import *

import time
import os
import json

# Add the top level directory to the sys.path to access classes
topdir = os.path.dirname(os.path.dirname(os.path.dirname \
            (os.path.dirname(os.path.abspath(__file__)))))
os.sys.path.insert(0, topdir)

from test.automated.rabbitmq.rabbitmq_ingress_processor_tests import RabbitMQingressProcessorTests
from framework.rabbitmq.rabbitmq_egress_processor import RabbitMQegressProcessor

@step(u'Given I send in the actuator message to restart raid sensor')
def given_i_send_in_the_actuator_message_to_restart_raid_sensor(step):
    # Clear the message queue buffer out
    while not world.sspl_modules[RabbitMQingressProcessorTests.name()]._is_my_msgQ_empty():
        world.sspl_modules[RabbitMQingressProcessorTests.name()]._read_my_msgQ()

    egressMsg = {
        "title": "SSPL Actuator Request",
        "description": "Seagate Storage Platform Library - Actuator Request",
        "username" : "JohnDoe",
        "signature" : "None",
        "time" : "2015-05-29 14:28:30.974749",
        "expires" : 500,

        "message" : {
            "sspl_ll_msg_header": {
                "schema_version": "1.0.0",
                "sspl_version": "1.0.0",
                "msg_version": "1.0.0"
            },
            "actuator_request_type": {
                "thread_controller": {
                    "module_name" : "RAIDsensor",
                    "thread_request": "restart"
                }
            }
        }
    }
    world.sspl_modules[RabbitMQegressProcessor.name()]._write_internal_msgQ(RabbitMQegressProcessor.name(), egressMsg)

@step(u"When SSPL restarts the thread for raid sensor msg handler")
def when_SSPL_LL_restarts_the_thread(step):
    print("SSPL restarts the threads for raid sensor msg handler")
    # TODO: Use an instance of JournalD sensor to monitor logs showing that SSPL performed the correct action

@step(u"Then I get the Restart Successful JSON response message")
def then_i_receive_Restart_Successful_JSON_response_message(step):
    """I get the JSON response msg with 'thread_response': 'Restart Successful' key value"""
    while not world.sspl_modules[RabbitMQingressProcessorTests.name()]._is_my_msgQ_empty():
        ingressMsg = world.sspl_modules[RabbitMQingressProcessorTests.name()]._read_my_msgQ()
        print("Received: %s" % ingressMsg)

        try:
            # Verify module name and thread response
            module_name = ingressMsg.get("actuator_response_type").get("thread_controller").get("module_name")
            print("module_name: %s" % module_name)
            assert module_name == "RAIDsensor"

            thread_response = ingressMsg.get("actuator_response_type").get("thread_controller").get("thread_response")
            print("thread_response: %s" % thread_response)
            assert thread_response == "Restart Successful"

            time.sleep(5)

            # Clear the message queue buffer out
            while not world.sspl_modules[RabbitMQingressProcessorTests.name()]._is_my_msgQ_empty():
                world.sspl_modules[RabbitMQingressProcessorTests.name()]._read_my_msgQ()
            print("Done")
            break
        except Exception as exception:
            print(exception)

@step(u'Given I send in the actuator message to stop raid sensor')
def given_i_send_in_the_actuator_message_to_stop_raid_sensor(step):
    egressMsg = {
        "title": "SSPL Actuator Request",
        "description": "Seagate Storage Platform Library - Actuator Request",
        "username" : "JohnDoe",
        "signature" : "None",
        "time" : "2015-05-29 14:28:30.974749",
        "expires" : 500,

        "message" : {
            "sspl_ll_msg_header": {
                "schema_version": "1.0.0",
                "sspl_version": "1.0.0",
                "msg_version": "1.0.0"
            },
            "actuator_request_type": {
                "thread_controller": {
                    "module_name" : "RAIDsensor",
                    "thread_request": "stop"
                }
            }
        }
    }
    world.sspl_modules[RabbitMQegressProcessor.name()]._write_internal_msgQ(RabbitMQegressProcessor.name(), egressMsg)

@step(u'When SSPL Stops the thread for raid sensor msg handler')
def when_sspl_ll_stops_the_thread_for_raid_sensor_msg_handler(step):
    print("SSPL Stops the thread for raid sensor msg handler")
    # TODO: Use an instance of JournalD sensor to monitor logs showing that SSPL performed the correct action

@step(u'Then I get the Stop Successful JSON response message')
def then_i_get_the_stop_successful_json_response_message(step):
    """I get the JSON response msg with 'thread_response': 'Stop Successful' key value"""
    time.sleep(2)
    module_name = None
    #import pdb
    #pdb.set_trace()
    while not world.sspl_modules[RabbitMQegressProcessor.name()]._is_my_msgQ_empty():
        ingressMsg = world.sspl_modules[RabbitMQegressProcessor.name()]._read_my_msgQ()
        time.sleep(10)
        print("Received: %s" % ingressMsg)

        try:

            # Verify module name and thread response
            module_name = ingressMsg.get("actuator_response_type").get("thread_controller").get("module_name")
            time.sleep(5)
            #name = module_name["RAIDsensor"]
            #print("module_name: %s" % name)

            thread_response = ingressMsg.get("actuator_response_type").get("thread_controller").get("thread_response")
            #response = module_name["Stop Successful"]
            time.sleep(4)
            #print("thread_response: %s" % response)
            break
        except Exception as exception:
            time.sleep(2)
            print(exception)

    assert(module_name is not None)
    assert(thread_response is not None)

@step(u'Given I send in the actuator message to start raid sensor')
def given_i_send_in_the_actuator_message_to_start_raid_sensor(step):
    egressMsg = {
        "title": "SSPL Actuator Request",
        "description": "Seagate Storage Platform Library - Actuator Request",
        "username" : "JohnDoe",
        "signature" : "None",
        "time" : "2015-05-29 14:28:30.974749",
        "expires" : 500,

        "message" : {
            "sspl_ll_msg_header": {
                "schema_version": "1.0.0",
                "sspl_version": "1.0.0",
                "msg_version": "1.0.0"
            },
            "actuator_request_type": {
                "thread_controller": {
                    "module_name" : "RAIDsensor",
                    "thread_request": "start"
                }
            }
        }
    }
    world.sspl_modules[RabbitMQegressProcessor.name()]._write_internal_msgQ(RabbitMQegressProcessor.name(), egressMsg)

@step(u'When SSPL Starts the thread for raid sensor msg handler')
def when_sspl_ll_starts_the_thread_for_raid_sensor_msg_handler(step):
    print("SSPL Starts the thread for raid sensor msg handler")
    # TODO: Use an instance of JournalD sensor to monitor logs showing that SSPL performed the correct action

@step(u'Then I get the Start Successful JSON response message')
def then_i_get_the_start_successful_json_response_message(step):
    """I get the JSON response msg with 'thread_response': 'Stop Successful' key value"""
    while not world.sspl_modules[RabbitMQingressProcessorTests.name()]._is_my_msgQ_empty():
        ingressMsg = world.sspl_modules[RabbitMQingressProcessorTests.name()]._read_my_msgQ()
        print("Received: %s" % ingressMsg)

        try:
            # Verify module name and thread response
            module_name = ingressMsg.get("actuator_response_type").get("thread_controller").get("module_name")
            print("module_name: %s" % module_name)
            assert module_name == "RAIDsensor"

            thread_response = ingressMsg.get("actuator_response_type").get("thread_controller").get("thread_response")
            print("thread_response: %s" % thread_response)
            assert thread_response == "Start Successful"

            time.sleep(5)

            # Clear the message queue buffer out
            while not world.sspl_modules[RabbitMQingressProcessorTests.name()]._is_my_msgQ_empty():
                world.sspl_modules[RabbitMQingressProcessorTests.name()]._read_my_msgQ()
            print("Done")
            break
        except Exception as exception:
            print(exception)

@step(u'Given I request to stop raid sensor and then I request a thread status')
def given_i_request_to_stop_raid_sensor_and_then_i_request_a_thread_status(step):
    egressMsg = {
        "title": "SSPL Actuator Request",
        "description": "Seagate Storage Platform Library - Actuator Request",
        "username" : "JohnDoe",
        "signature" : "None",
        "time" : "2015-05-29 14:28:30.974749",
        "expires" : 500,

        "message" : {
            "sspl_ll_msg_header": {
                "schema_version": "1.0.0",
                "sspl_version": "1.0.0",
                "msg_version": "1.0.0"
            },
            "actuator_request_type": {
                "thread_controller": {
                    "module_name" : "RAIDsensor",
                    "thread_request": "stop"
                }
            }
        }
    }
    world.sspl_modules[RabbitMQegressProcessor.name()]._write_internal_msgQ(RabbitMQegressProcessor.name(), egressMsg)

    # Request the status for the stopped thread
    egressMsg = {
        "title": "SSPL Actuator Request",
        "description": "Seagate Storage Platform Library - Actuator Request",
        "username" : "JohnDoe",
        "signature" : "None",
        "time" : "2015-05-29 14:28:30.974749",
        "expires" : 500,

        "message" : {
            "sspl_ll_msg_header": {
                "schema_version": "1.0.0",
                "sspl_version": "1.0.0",
                "msg_version": "1.0.0"
            },
            "actuator_request_type": {
                "thread_controller": {
                    "module_name" : "RAIDsensor",
                    "thread_request": "status"
                }
            }
        }
    }
    world.sspl_modules[RabbitMQegressProcessor.name()]._write_internal_msgQ(RabbitMQegressProcessor.name(), egressMsg)

@step(u'When SSPL Stops the raid sensor and receives a request for thread status')
def when_sspl_ll_stops_the_raid_sensor_and_receives_a_request_for_thread_status(step):
    print("SSPL Starts the thread for raid sensor msg handler")
    # TODO: Use an instance of JournalD sensor to monitor logs showing that SSPL performed the correct action

@step(u'Then I get the Stop Successful JSON message then I get the thread status message')
def then_i_get_the_stop_successful_json_message_then_i_get_the_thread_status_message(step):
    """I get the JSON response msg with 'thread_response': 'Stop Successful' key value"""

    while not world.sspl_modules[RabbitMQingressProcessorTests.name()]._is_my_msgQ_empty():
        ingressMsg = world.sspl_modules[RabbitMQingressProcessorTests.name()]._read_my_msgQ()
        print("Received: %s" % ingressMsg)

        try:
            # Verify module name and thread response
            module_name = ingressMsg.get("actuator_response_type").get("thread_controller").get("module_name")
            print("module_name: %s" % module_name)
            assert module_name == "RAIDsensor"

            thread_response = ingressMsg.get("actuator_response_type").get("thread_controller").get("thread_response")
            print("thread_response: %s" % thread_response)
            assert thread_response == "Stop Successful"

            ingressMsg = world.sspl_modules[RabbitMQingressProcessorTests.name()]._read_my_msgQ()
            print("Received: %s" % ingressMsg)

            # Verify module name and thread response
            module_name = ingressMsg.get("actuator_response_type").get("thread_controller").get("module_name")
            print("module_name: %s" % module_name)
            assert module_name == "RAIDsensor"

            thread_response = ingressMsg.get("actuator_response_type").get("thread_controller").get("thread_response")
            print("thread_response: %s" % thread_response)
            assert thread_response == "Status: Halted"
            print("Done")
            break
        except Exception as exception:
            print(exception)

@step(u'Given I request to start raid sensor and then I request a thread status')
def given_i_request_to_start_raid_sensor_and_then_i_request_a_thread_status(step):
    egressMsg = {
        "title": "SSPL Actuator Request",
        "description": "Seagate Storage Platform Library - Actuator Request",
        "username" : "JohnDoe",
        "signature" : "None",
        "time" : "2015-05-29 14:28:30.974749",
        "expires" : 500,

        "message" : {
            "sspl_ll_msg_header": {
                 "schema_version": "1.0.0",
                 "sspl_version": "1.0.0",
                 "msg_version": "1.0.0"
            },
            "actuator_request_type": {
                "thread_controller": {
                     "module_name" : "RAIDsensor",
                     "thread_request": "start"
                }
            }
        }
    }
    world.sspl_modules[RabbitMQegressProcessor.name()]._write_internal_msgQ(RabbitMQegressProcessor.name(), egressMsg)

    # Request the status for the stopped thread
    egressMsg = {
        "title": "SSPL Actuator Request",
        "description": "Seagate Storage Platform Library - Actuator Request",
        "username" : "JohnDoe",
        "signature" : "None",
        "time" : "2015-05-29 14:28:30.974749",
        "expires" : 500,

        "message" : {
            "sspl_ll_msg_header": {
                "schema_version": "1.0.0",
                "sspl_version": "1.0.0",
                "msg_version": "1.0.0"
            },
            "actuator_request_type": {
                "thread_controller": {
                    "module_name" : "RAIDsensor",
                    "thread_request": "status"
                }
            }
        }
    }
    world.sspl_modules[RabbitMQegressProcessor.name()]._write_internal_msgQ(RabbitMQegressProcessor.name(), egressMsg)

@step(u'When SSPL Starts the raid sensor and receives a request for thread status')
def when_sspl_ll_starts_the_raid_sensor_and_receives_a_request_for_thread_status(step):
    print("SSPL Starts the thread for raid sensor msg handler")
    # TODO: Use an instance of JournalD sensor to monitor logs showing that SSPL performed the correct action

@step(u'Then I get the Start Successful JSON message then I get the thread status message')
def then_i_get_the_start_successful_json_message_then_i_get_the_thread_status_message(step):
    """I get the JSON response msg with 'thread_response': 'Stop Successful' key value"""
    while not world.sspl_modules[RabbitMQingressProcessorTests.name()]._is_my_msgQ_empty():
        ingressMsg = world.sspl_modules[RabbitMQingressProcessorTests.name()]._read_my_msgQ()
        print("Received: %s" % ingressMsg)

        try:
            # Verify module name and thread response
            module_name = ingressMsg.get("actuator_response_type").get("thread_controller").get("module_name")
            print("module_name: %s" % module_name)
            assert module_name == "RAIDsensor"

            thread_response = ingressMsg.get("actuator_response_type").get("thread_controller").get("thread_response")
            print("thread_response: %s" % thread_response)
            assert thread_response == "Start Successful"

            ingressMsg = world.sspl_modules[RabbitMQingressProcessorTests.name()]._read_my_msgQ()
            print("Received: %s" % ingressMsg)

            # Verify module name and thread response
            module_name = ingressMsg.get("actuator_response_type").get("thread_controller").get("module_name")
            print("module_name: %s" % module_name)
            assert module_name == "RAIDsensor"

            thread_response = ingressMsg.get("actuator_response_type").get("thread_controller").get("thread_response")
            print("thread_response: %s" % thread_response)
            assert thread_response == "Status: Running"
            print("Done")
            break
        except Exception as exception:
            print(exception)

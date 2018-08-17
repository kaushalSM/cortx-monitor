#!/usr/bin/env python

import sys
import pika
import json
import pprint

SSPL_USER = "sspluser"
SSPL_PASS = "sspl4ever"
SSPL_QUEUE = "SSPL-LL"
SSPL_EXCHANGE = "sspl_halon"
SSPL_KEY = "sspl_ll"
SSPL_VHOST = "SSPL"

def process_msg(ch, method, properties, body):
    print body

try:
    if len(sys.argv) > 2:
        SSPL_EXCHANGE = sys.argv[1]
        SSPL_QUEUE = sys.argv[2]

    creds = pika.PlainCredentials(SSPL_USER, SSPL_PASS)
    connection = pika.BlockingConnection(pika.\
        ConnectionParameters(host="localhost", virtual_host=SSPL_VHOST, credentials=creds))
    channel = connection.channel()
    result = channel.queue_declare(queue=SSPL_QUEUE, durable=False)
    channel.exchange_declare(exchange=SSPL_EXCHANGE, type='topic', durable=False)
    channel.queue_bind(queue=SSPL_QUEUE, exchange=SSPL_EXCHANGE, routing_key=SSPL_KEY)
    channel.basic_consume(process_msg, queue=result.method.queue)
    channel.start_consuming()

except Exception as e:
    print e

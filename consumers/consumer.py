"""Defines core consumer functionality"""
import logging

import confluent_kafka
from confluent_kafka import Consumer
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
from tornado import gen


logger = logging.getLogger(__name__)


class KafkaConsumer:
    """Defines the base kafka consumer class"""

    def __init__(
        self,
        topic_name_pattern,
        message_handler,
        is_avro=True,
        offset_earliest=False,
        sleep_secs=1.0,
        consume_timeout=0.1,
    ):
        """Creates a consumer object for asynchronous use"""
        self.topic_name_pattern = topic_name_pattern
        self.message_handler = message_handler
        self.sleep_secs = sleep_secs
        self.consume_timeout = consume_timeout
        self.offset_earliest = offset_earliest

        self.broker_properties = {
                'bootstrap.servers': "localhost:9092",
                'group.id': 'dashboard_server'
        }

        if is_avro is True:
            self.broker_properties["schema.registry.url"] = "http://localhost:8081"
            self.consumer = AvroConsumer(self.broker_properties)
        else:
            self.consumer = Consumer(self.broker_properties)

        self.consumer.subscribe([self.topic_name_pattern], on_assign=self.on_assign)

    def on_assign(self, consumer, partitions):
        """Callback for when topic assignment takes place"""
        for partition in partitions:
            partition.offset = 0
        logger.info("partitions assigned for %s", self.topic_name_pattern)
        consumer.assign(partitions)

    async def consume(self):
        """Asynchronously consumes data from kafka topic"""
        logger.info(f"Consuming messages from topic {self.topic_name_pattern}")
        while True:
            num_results = 1
            while num_results > 0:
                num_results = self._consume()
            await gen.sleep(self.sleep_secs)

    def _consume(self):
        """Polls for a message. Returns 1 if a message was received, 0 otherwise"""
        logger.info(f"_consume method was called for topic {self.topic_name_pattern}")
        logger.info("Polling")
        message = self.consumer.poll(timeout=5)
        logger.info("Finished waiting 5 seconds")
        if message is None:
            logger.info("No messages processed")
            return 0
        if message.error() is not None:
            logger.error(f"Error retrieving message: {message.error()}")
            return 1
        else:
            logger.info(f"Will handle message for topic {message.topic()}")
            logger.info(f"{message.value()}")
            self.message_handler(message)
            return 1

    def close(self):
        """Cleans up any open kafka consumers"""
        self.consumer.close()

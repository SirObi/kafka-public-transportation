"""Contains functionality related to Lines"""
import json
import logging

from models import Line


logger = logging.getLogger(__name__)


class Lines:
    """Contains all train lines"""

    def __init__(self):
        """Creates the Lines object"""
        self.red_line = Line("red")
        self.green_line = Line("green")
        self.blue_line = Line("blue")
        logger.info("Created lines")

    def process_message(self, message):
        """Processes a station message"""
        logger.info(f"Attempting to process message... for topic {message.topic()}")
        if "arrivals" in message.topic() or "stations" in message.topic():
            value = message.value()
            if message.topic() == "obi.transport_optimization.chicago.cta.stations.table.v2":
                logger.info("Received message from stations table")
                value = json.loads(value)
                logger.info(f"Value was {value}")
            if value["line"] == "green":
                self.green_line.process_message(message)
            elif value["line"] == "red":
                self.red_line.process_message(message)
            elif value["line"] == "blue":
                self.blue_line.process_message(message)
            else:
                logger.debug("discarding unknown line msg %s", value["line"])
        elif "TURNSTILE_SUMMARY" == message.topic():
            #self.green_line.process_message(message)
            #self.red_line.process_message(message)
            #self.blue_line.process_message(message)
            pass
        else:
            logger.info("ignoring non-lines message %s", message.topic())

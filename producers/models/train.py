"""Defines CTA Train Model"""
from enum import IntEnum
import logging


logger = logging.getLogger(__name__)


class Train:
    """Defines CTA Train Model"""

    def __init__(self, train_id, status):
        self.train_id = train_id
        self.status = status
        if self.status is None:
            self.status = "out_of_service"

    def __str__(self):
        return f"Train ID {self.train_id} is {self.status.replace('_', ' ')}"

    def __repr__(self):
        return str(self)

    def broken(self):
        return self.status == "broken_down"

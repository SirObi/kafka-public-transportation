import json
from confluent_kafka import avro
from producers.models.producer import Producer

EXAMPLE_KEY_SCHEMA = json.dumps(
    {
        "type": "record",
        "name": "user_info.key",
        "namespace": "my.example",
        "fields": [{"name": "user_name", "type": "string", "default": ""}],
    }
)


EXAMPLE_VALUE_SCHEMA = json.dumps(
    {
        "type": "record",
        "name": "user_info",
        "namespace": "my.example",
        "fields": [
            {"name": "user_name", "type": "string", "default": ""},
            {"name": "age", "type": "int", "default": -1},
        ],
    }
)


class Example(Producer):
    """Defines a single station"""

    key_schema = avro.loads(EXAMPLE_KEY_SCHEMA)
    value_schema = avro.loads(EXAMPLE_VALUE_SCHEMA)

    def __init__(self):
        topic_name = "test.producer"
        super().__init__(
            topic_name, key_schema=Example.key_schema, value_schema=Example.value_schema
        )
        print(f"value_schema was {self.value_schema}")

    def run(self, some_value):
        """Simulates train arrivals at this station"""

        self.producer.produce(
            topic=self.topic_name, key={"timestamp": self.time_millis()}, value={}
        )

    def close(self):
        """Prepares the producer for exit by cleaning up the producer"""
        print("closing")
        super(Example, self).close()


def test_producer_initializes_correctly():
    example = Example()
    example.run("obi")
    example.close()

"""Defines trends calculations for stations"""
import logging

import faust


logger = logging.getLogger(__name__)


# Faust will ingest records from Kafka in this format
class Station(faust.Record):
    stop_id: int
    direction_id: str
    stop_name: str
    station_name: str
    station_descriptive_name: str
    station_id: int
    order: int
    red: bool
    blue: bool
    green: bool


# Faust will produce records to Kafka in this format
class TransformedStation(faust.Record):
    station_id: int = 0
    station_name: str = ""
    order: int = 0
    line: str = ""


app = faust.App("stations-stream", broker="kafka://localhost:9092", store="memory://")
input_topic = app.topic("obi.transport_optimization.chicago.cta.stations.table.v1stations", value_type=Station)

output_topic = app.topic("obi.transport_optimization.chicago.cta.stations.table.v2", partitions=1)

table = app.Table(
    'stations_cleaned',
    default=TransformedStation,
    partitions=1,
    changelog_topic=output_topic,
)


#
#
# TODO: Using Faust, transform input `Station` records into `TransformedStation` records. Note that
# "line" is the color of the station. So if the `Station` record has the field `red` set to true,
# then you would set the `line` of the `TransformedStation` record to the string `"red"`
#
#

@app.agent(input_topic)
async def process(tables):
    async for value in tables:
        line_colours = {"red": value.red, "blue": value.blue, "green": value.green}
        try:
            colour = [k for (k,v) in line_colours.items() if v == True][0]
        except Exception as e:
            print(e)
            print(f"Stop {value.stop_id} is not on one of lines: {line_colours.keys()}")
            continue
        transformed_station = TransformedStation(
            value.station_id,
            value.station_name,
            value.order,
            colour
        )
        table.update({transformed_station.station_id: transformed_station})


if __name__ == "__main__":
    app.main()

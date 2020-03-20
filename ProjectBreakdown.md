Requirements in Udacity projects are usually quite chaotically documented.   
Therefore, I've created this document to help the reader understand the various objectives the code is supposed to achieve.   
This guide was also meant to help me keep track of what needed to be done, in a BDD fashion.

### End goal
**Given** I have access to a stream of arrival events from turnstile hardware  
**And** I have access to a weather data REST server  
**And** I have information about train stations in a static table  
**When** I start a server with a dashboard  
**Then** the dashboard displays a list of stations with line colours  
**And** the dashboard displays train arrivals at each station in real time  
**And** the dashboard displays total arrivals at given station in a certain time window  
**And** the dashboard displays current weather  

### Note
In order to demonstrate the different parts of the Kafka ecosystem, Udacity has shoehorned them into this project in rather unusual ways.
Static data from Postgres is run through a Faust Structured streaming application to help create data models.
Similarly, the server uses Kafka REST Proxy to talk to the REST weather server, rather than simply sending an HTTP request at regular intervals.

These (counterintuitive) solutions can slow you down while trying to understand the codebase, so just bear that in mind:
the sole focus of this project is to showcase the different parts of Kafka, and how they relate to the outside world.

### Milestones
**Given** I have access to a stream of arrival events from turnstile hardware  
**When** an arrival event is emitted  
**Then** the event is put in a topic by a Kafka producer  

**Given** I have a Postgres database with static station data  
**And** I want to have the data as a Kafka topic instead  
**When** I run the connector  
**Then** the raw data is placed in a Kafka topic  

**Given** I have a Kafka topic with raw station data  
**When** I transform it with Faust Stream processing  
**Then** I have a new topic with station data in a more convenient format  

**Given** I have a Kafka topic for arrival events for given station  
**And** I have a Kafka topic with transformed station data  
**When** a new event has arrived in the Kafka topic  
**Then** the event is joined on the table ....?

## Architecture  
There are two classes in the server code that handle incoming messages from a Kafka topic: Line and Weather.  

### Line
Line handles incoming `station`, `arrival` and `total_arrivals` messages.  
Line passes on `arrival` and `total_arrivals`  messages to another class, Station.  

`station` message {station_id, station_name, order} => initialize new Station  

`arrival` message {direction, train_id, train_status} => changes state of platform A or B  

`total_arrivals` message {station_id, COUNT} => changes state of turnstile entries counter on Station  

(there's possibly also a `departure` event)  

```
class Station:
    """Defines the Station Model"""

    def __init__(self, station_id, station_name, order):
        """Creates a Station Model"""
        self.station_id = station_id
        self.station_name = station_name
        self.order = order
        self.dir_a = None
        self.dir_b = None
        self.num_turnstile_entries = 0
```

### Weather
Weather handles incoming `weather` messages.  
There is only one instance of Weather on the server.  

`weather` message {temperature, status} => changes state of temperature and weather status on Weather instance

Weather should ignore any topic other than the weather topic (name unclear as of yet).  

### Lines
Lines groups 3 Line objects together: Line("red"), Line("green") and Line("blue").  
There's only one Lines instance on the server.  
Messages hit Lines first, and then get passed on to one of the three Line objects, or ignored.  
Accepted topics are: `*org.chicago.cta.station*` and `TURNSTILE_SUMMARY`.  



## Project milestones - completion
- [x] Schema for turnstile event defined
...
- [ ] Correctly named Kafka topic exists for each station in the simulation/in the database  
- [ ] Kafka REST Proxy creates and populates a topic with events containing {temperature, status}
...
- [ ] KSQL aggregates turnstile events into `TURNSTILE_SUMMARY` for each station (+direction?)
- [ ] Dashboard displays list of stations on the Blue line
- [ ] Emitting new turnstile event causes dashboard to update
- [ ] simulation.py works and doesn't crash after 1 minute
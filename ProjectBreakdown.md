Requirements in Udacity projects are usually quite chaotically documented.   
Therefore, I've created this document to help the reader understand the various objectives the code is supposed to achieve.   
This guide was also meant to help me keep track of what needed to be done, in a BDD fashion.

### End goal
**As a** Chicago Transport Authority executive  
**I would like to** have a website that displays train arrivals and people getting off the trains in real time  
**So that** I can have a more intuitive understanding of how people flow through my transportation system   

**Given** I have access to a stream of train arrival events from train sensors on station  
**And** I have access to a stream of turnstile events from people walking through the turnstiles  
**And** I have access to a weather data REST server  
**And** I have information about all Chicago train stations in a static table  
**When** I start a server with a dashboard  
**Then** the dashboard displays a list of stations on lines "Red", "Green" and "Blue"  
**And** the dashboard displays train arrivals at each station in real time  
**And** the dashboard displays total number of people who have got off at the station so far  
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

## Architecture - Kafka Consumers
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


## `server.py` dependencies

These are some of the preconditions for `python consumers/server.py` not crashing.  
1. "TURNSTILE_SUMMARY" topic exists
2. Faust Streaming aggregation table exists


## Architecture - Kafka Producers  

### Weather class + REST Proxy  
The Weather class is not a Kafka Producer.    
It's written in vanilla Python and simply simulates old hardware.  
The class sends weather events to the Kafka REST server in the form of POST requests.  
The requests include both the payload, and the AVRO schema to read it with.  

Kafka REST Proxy has all the client functionality required to parse the requests, create a new topic, and write the events to the topic.  

### Station (Postgres/Faust)  
The Station data model can be a bit misleading.  
Despite the name it actually defines the attributes of a platform in the Chicago transport network, not a station. Some of the attributes are:  
- stop (platform) name and ID  
- direction of the trains stopping at the platform  s
- parent station name and ID  
- line the station is on  

### Arrival  
It seems that arrival needs to contain the field `line` as well.  
Otherwise an `if` block on the consumer server will cause all arrival messages to be skipped.  
Seems like an argument in favour of having consumer-driven contract tests between Kafka clients...  
Or at least the client side creating and uploading the schemas to the Schema Registry.  


## Project milestones - completion
1. Create Kafka Producers
- [x] Properly defined schema for arrival events  
- [x] Properly defined schema for turnstile events  
- [x] Station producer implemented
- [x] Correctly named Kafka topic exists for each station in the simulation/in the database  
- [x] simulation.py is able to populate topics with arrival and turnstile events

2. Configure Kafka REST Proxy Producer
- [x] Kafka REST Proxy creates and populates a topic with events containing {temperature, status}

3. Configure Kafka Connect
- [x] Connector with appropriate name gets created on Kafka Connect server  
- [x] Connector ingests data from Postgres, creates a new topic  
- [x] New topic contains station data  

4. Configure Faust Stream Processor
- [x] Stream processor able to print out records from stations topic  
- [x] Logic to filter out unnecessary Station fields implemented  
- [x] TransformedStation data is persisted in Faust table  
- [x] `server.py` able to read from stations topic and display stations in web UI   

5. Configure the KSQL Table
- [ ] KSQL aggregates turnstile events into `TURNSTILE_SUMMARY` for each station (+direction?)

6. End-to-end success

- [x] Dashboard displays list of stations on the Blue, Red and Green lines
- [ ] Emitting new turnstile event causes dashboard to update
- [ ] simulation.py works and doesn't crash after 1 minute

## Setup
You need Docker in order to run this project.  
You also need Kafka, Java and Scala installed on your machine.  


The following commands should get you all the way to seeing the traffic flow on the dashboard.  

`cd` into the project  
`docker-compose up` to start all the Kafka tools.  

**Producer side**  
`cd producers`  
`brew install pipenv`  
`pipenv install`  
`pipenv shell`  
`python simulation.py`  

**Consumer side**  
Open up a new tab in your Terminal (Mac users).  
`cd ../`  
`pipenv install`  
`pipenv shell`  
`cd consumers`  
`faust -A faust_stream worker -l info`  
`python ksql.py`  
`python server.py`  


## Some useful commands: 

**List consumers registered with Zookeeper (hepful with debugging Faust consumer offsets)**  
`$KAFKA_HOME/bin/kafka-consumer-groups.sh  --list --bootstrap-server localhost:9092`  

**Reset offsets for Faust Stream Processing application**  
`$KAFKA_HOME/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --execute --reset-offsets --group stations-stream --to-earliest --all-topics`  

**Delete all topics in this project**  
`$KAFKA_HOME/bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic 'obi.*'`

**Delete a schema in Schema Registry**  
`curl -X DELETE http://localhost:8081/subjects/<schema_name>`

**Delete all schemas in Schema Registry with "transport_optimization" in the title**  
`for schema in $(echo $schemas | jq  | grep obi | cut -d\" -f2); do curl -X DELETE http://localhost:8081/subjects/$schema; done)`

**Restart the entire Kafka infrastructure (helpful with Kafka Connect issues)**  
`Ctrl+C` to stop docker containers  
`docker system prune` to remove all incorrect state you've created (removes stopped containers)  
`docker-compose up` to restart the infrastructure  


## Typical errors: 

`TypeError: encoding without a string argument`  
This means some application (usually `simulation.py`, in this project) tried to push a record containing a `null` where the schema only accepts a `string` for that field.  

This error is usually fixed by changing accepted type in schema to an array of types:  
```
"type": "string"
```  

=>  

```
"type": [
        "null",
        "string"
      ]
```

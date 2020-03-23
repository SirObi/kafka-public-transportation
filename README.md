
# Kafka - public transport optimization  
This project showcases the various parts of the Kafka ecosystem in one project.  
It uses a set of events representing the flow of passengers through Chicago's public transport network.  

## Motivation
The purpose of the project was to explore how various Kafka tools can be used, including:  
Kafka Connect, Kafka REST Proxy, KSQL, and Faust Stream Processing.  

[Diagram](./readme_images/diagram.png)


## Input 
This project two main inputs: 
- list of stations on the Chicago network  
- ridership inputs, used by `simulation.py`  

**Example list of stations:**  
```
stop_id,direction_id,stop_name,station_name,station_descriptive_name,station_id,order,red,blue,green
30004,W,Harlem (Terminal arrival),Harlem/Lake,Harlem/Lake (Green Line),40020,0,FALSE,FALSE,TRUE
30003,E,Harlem (63rd-bound),Harlem/Lake,Harlem/Lake (Green Line),40020,0,FALSE,FALSE,TRUE
30263,E,Oak Park (63rd-bound),Oak Park,Oak Park (Green Line),41350,1,FALSE,FALSE,TRUE
```

**Ridership simulation data:**
```
hour,ridership_ratio
0,0.01
1,0.01
2,0.01
3,0.01
4,0.0125
5,0.025
...
```
```
station_id,stationame,month_beginning,avg_weekday_rides,avg_saturday_rides,avg_sunday-holiday_rides,monthtotal
40380,Clark/Lake,10/01/2018,22811.6,6901.8,6233.5,577208
40260,State/Lake,10/01/2018,14098.7,7307.8,5824.5,376799
40200,Randolph/Wabash,10/01/2018,0,0,0,0
41700,Washington/Wabash,10/01/2018,11079.3,5920,4248.8,295498
...
```

The static station data is stored in a Postgres DB. Kafka Connect is used to read in the data, and Faust - to clean it up.  
The ridership data is used by a Python script which generates a stream of events, simulating real-time sensor data.  
In a real-world use case, the data would come from sensors detecting train arrivals/departures and turnstile hardware.  


Once you have the project set up (see instructions in [CONTRIBUTING.md](./CONTRIBUTING.md)), you should be able to view the flow of passengers on the dashboard available at:  
`localhost:8088` in your browser.  
It also gives you the current weather (random data available through a REST server, simulating old weather hardware).

[Server Dashboard](./readme_images/server_dashboard.png)  

## Detailed architecture   
Screenshots of the various elements of project are available under:  
[Architecture screenshots](./ARCHITECTURE.md)

## Detailed project requirements  
You can see the requirements exploration work under:  
[Project Breakdown](./ProjectBreakdown.md)

## Findings  
The main finding is that knowing how to set, reset and manage offsets in Kafka Consumers is extremely important to working with the Kafka ecosystem.  
Another finding is that Faust is an extremely good example of Pythonic code, although its documentation is lacking.  

## License
MIT © [Obi]()

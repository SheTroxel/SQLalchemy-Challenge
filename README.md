# SQLalchemy-Challenge
Homework Challenge 10
In this assignment, I used Python and SQLAlchemy to do a basic climate analysis and data exploration of a provided climate database.

## Analyze and Explore Climate Data
Used SQLAlchemy create_engine() function to connec to the provided SQlite databse
Used SQLAlchemy automap_base() function to reflect tables into classes, and saved references as station and measurement.
Linked Python to the database by creating a SQLAlchemy session


## Preciptation Analysis
Analysis included finding the most recent date in the dataset. 
Using this date, get the previous 12 months of precipitaton data.
By sorting the DataFrame values by date, I plotted the results to show the preciptation in inches.

![Precipitation](https://github.com/SheTroxel/SQLalchemy-Challenge/blob/main/precip_bar2.png)

## Weather Station Analysis

Designed a query to calculate the total number of stations in the dataset and determine which station is the most-active.
For the purposes of this activity, most active was defined as the station with the most rows of data. From this query, I was able to list the stations and observation counts in descending order to determine which station id has the greatest number of observations. 

The station with the most number of observation was Station_USC00519281.

Designed a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.
Designed a query to get the previous 12 months of temperature obstervation (TOBS) data for Station_USC00519281.

  • filtered by the station with the greatest number of observations
  
  • Queried the previous 12 months of TOBS data for Station_USC00519281
  
  • Plotted the reults as a histogram.

![temp_histogram](https://github.com/SheTroxel/SQLalchemy-Challenge/blob/main/temp_histogram.png)


## Designed a Flask API 
Using the queries from my analysis, I created a Flask API.
From the homepage, there are several routes.

/api/v1.0/precipitation   
JSON representation of data dictionary where date is the key and prcp is the value.

/api/v1.0/stations        
JSON list of stations from the dataset
 
/api/v1.0/tobs           
Returns a JSON list of temperature observations for the previous year for the most active station.

/api/v1.0/temp<start>   
Returns a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start data

/api/v1.0/temp_range<start>/<end>
Returns a JSON list where the minimum temperature, the average temperature, and the maximum temperature are calculated for a start-end range.





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

![Precipitation](https://github.com/SheTroxel/SQLalchemy-Challenge/blob/main/precip_bar.png)

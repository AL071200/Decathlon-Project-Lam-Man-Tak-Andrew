Part 1
The python file is a series of code used to convert the order of the tables from the raw data format 
to the specificed data format. I used python to reorder the files and to calculate the different durations
that an employee would work to the nearest hour, before including the par thereof as a decimal of an hour
in a seperate row underneath the modified row. It was modified on a copy of the man_hours file before I
generate an entirely new excel file. There are couple of assumptions as well. For workers who start on a 
certain date and end at a time of day before the start time, I assume that they did an overnight shift, 
and respectively truncate their shift at the 0000HR mark, and push forward the date by one day. 
The format of the date and time in excel is in the slash form as excel in default reads the 2024-01-30 dates as 30/01/2024.

Part 2
I used a transaction against customers to analyze the conversion rate of the customers before adding a seperate graph below
to help the user visualize whether the employees at work at the given hour are helping the conversion rate. I used a floor of 
the hour because the rest of the excel files have the hour of day in a discrete manner recorded. I then seperated this based
on the store, weekdays and the weekends

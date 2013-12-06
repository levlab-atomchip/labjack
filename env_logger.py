# Based on u6allio.py

import u6
from datetime import datetime
import sys
import psycopg2
#I need to import all drivers and postprocessors

# set up a sql connection
conn = psycopg2.connect()
c = conn.cursor


# sql query to get all the sensors I need. each sensor has a, id, driver, address and postprocessor
c.execute('''SELECT sensors._id, channels.driver, channels.address, postprocessors.name 
FROM sensors, channels, postprocessors 
WHERE sensors.channel = channels._id 
AND sensors.postprocessor = postprocessors._id 
AND sensors.environmental = true 
AND sensors.installed = true''')
sensors = c.fetchall()
# for each sensor
for sensor in sensors:

    #query the channel to get the driver
    this_driver = sensor(1) #string of form drivername()
    this_address = sensor(2)
    #get the time
    this_time = datetime.datetime.now()
    #use driver to get an output
    output = eval(this_driver + '(%s)'%this_address)
    #send output to postprocessor to get a result
    this_postprocessor = sensor(3) #string of form postprocessorname
    this_value = eval(this_postprocessor%output)
    this_sensor_id = sensor(0)
    
    #insert result and time into sensor_data
    c.execute("INSERT INTO sensor_data VALUES (%d, %s, %f, null)"%(this_sensor_id, this_time, this_value))
    conn.commit
    
#close sql connection
c.close()
conn.close()
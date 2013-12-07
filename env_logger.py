# Based on u6allio.py
from datetime import datetime
import psycopg2
from drivers import *
from postprocessors import *
#I need to import all drivers and postprocessors

# set up a sql connection
conn = psycopg2.connect("dbname=labjack_testing user=levlab host=levlabserver.stanford.edu")
c = conn.cursor()


# sql query to get all the sensors I need. each sensor has a, id, driver, address and postprocessor
c.execute('''SELECT s._id, d.name, c.address, p.name, s.name 
FROM sensors s, channels c, postprocessors p, drivers d
WHERE s.channel = c._id 
AND s.postprocessor = p._id 
AND c.driver = d._id
AND s.environmental = true 
AND s.installed = true;''')
sensors = c.fetchall()
# for each sensor
for sensor in sensors:
    print sensor[4]
    print sensor[0]
    #query the channel to get the driver
    this_driver = sensor[1] #string of form drivername()
    this_address = sensor[2]
    #get the time
    this_time = datetime.now()
    print this_time
    #use driver to get an output
    output = eval(this_driver + '(%s)'%this_address)
    print output
    #send output to postprocessor to get a result
    this_postprocessor = sensor[3] #string of form postprocessorname
    this_value = eval(this_postprocessor + '(%f)'%output)
    print this_value
    this_sensor_id = sensor[0]
    
    #insert result and time into sensor_data
    # insert_query = "INSERT INTO sensor_data VALUES (%d, '%s', %f, null);"%(this_sensor_id, this_time, this_value)
    c.execute("INSERT INTO sensor_data (sensor, time, value) VALUES (%s, %s, %s);",(this_sensor_id, this_time, this_value))
    # c.execute(insert_query)
    print c.query
    conn.commit()
    
#close sql connection
c.close()
conn.close()
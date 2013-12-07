import u6

def HumidiconRH_Driver(channelnum):

    d = u6.U6()
    
    try:
        d.i2c() # Send Measurement Request
    
        isDataStale = 1
        while isDataStale:
            results = d.i2c() # Send Data Fetch
            isDataStale = results[1]
        rh_count = results[2:13]
        return rh_count
    finally:
        d.close()
# Based on u6allio.py

import u6
from datetime import datetime
import sys

numChannels = int(sys.argv[1])
resolutionIndex = 1
gainIndex = 0
settlingFactor = 0
differential = False

latestAinValues = [0] * numChannels

numIterations = 1000

d = u6.U6()
d.getCalibrationData() #fills d.calInfo; required for binaryToCalibratedAnalogVoltage()

try:
    #Configure the IOs before the test starts

    feedbackArguments = []
    
    for i in range(numChannels):
        feedbackArguments.append( u6.AIN24(i, resolutionIndex, gainIndex, settlingFactor, differential) )
    
    
    start = datetime.now()
    # Call Feedback 1000 times
    i = 0
    while i < numIterations:
        results = d.getFeedback( feedbackArguments ) #Returns 
        
        for j in range(numChannels):
            latestAinValues[j] = d.binaryToCalibratedAnalogVoltage(gainIndex, results[ j ])
            # binaryToCalibratedAnalogVoltage only works if you ran getCalibrationData() previously.
        i += 1

    end = datetime.now()
    delta = end - start
    print "Time difference: ", delta
    dm = delta / numIterations
    print "Time per iteration: ", dm
    print "Time per iteration in millis: ", dm.microseconds  / 1000.0
    print "Latest readings: ", latestAinValues

finally:
    d.close()
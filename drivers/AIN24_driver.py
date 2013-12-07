import u6

def AIN24_Driver(channelnum):
    resolutionIndex = 1
    gainIndex = 0
    settlingFactor = 0
    differential = False

    d = u6.U6()
    d.getCalibrationData() #fills d.calInfo; required for binaryToCalibratedAnalogVoltage()

    try:
        results = d.getFeedback( u6.AIN24(channelnum, resolutionIndex, gainIndex, settlingFactor, differential) ) #Returns 
        AINvalue = d.binaryToCalibratedAnalogVoltage(gainIndex, results[0])
        return AINvalue
    finally:
        d.close()
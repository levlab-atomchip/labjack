import u6

def HumidiconRH_Driver(SDAnum, SCLnum):

    d = u6.U6()

    try:
        WriteMask_str = (bin((1 << SDAnum) + (1 << SCLnum))[2:].zfill(24)) # Generate the Write Mask
        WriteMask = [int(WriteMask_str[0:8],2), int(WriteMask_str[8:16],2), int(WriteMask_str[16:24],2)] # Separate Write Mask into bytes
        d.getFeedback(u6.PortDirWrite(Direction = [15, 15, 15], WriteMask)) # Sets the direction of digital I/O to output
        
        d.i2c(0x27,[],SDAPinNum = SDAnum, SCLPinNum=SCLnum ) # Send Measurement Request
        
        WriteMask_str = (bin(1 << SDAnum))[2:].zfill(24)) # Generate Write Mask
        WriteMask = [int(WriteMask_str[0:8],2), int(WriteMask_str[8:16],2), int(WriteMask_str[16:24],2)] # Separate Write Mask into bytes
        d.getFeedback(u6.PortDirWrite(Direction = [0, 0, 0], WriteMask)) # Sets the direction of digital I/O to input

        isDataStale = 1
        while isDataStale:
            results = d.i2c(0x27, [], SDAPinNum = SDAnum, SCLPinNum=SCLnum, NumI2CBytesToReceive = 4) # Send Data Fetch
            isDataStale = results['I2CBytes'][1]
        rh_count = results['I2CBytes'][2:16]
        return eval('0b' + ''.join([str(i) for i in rh_count]))
    finally:
        d.close()
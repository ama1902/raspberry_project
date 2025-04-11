from machine import Pin, I2C
import time

i2c0 = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000)    

print(i2c0.scan())    #Scan the address of the current device
address = 16          #Radar module communication address 0x10
getLidarDataCmd = bytearray([0x5A,0x05,0x00,0x01,0x60])    #Data fetch instruction

def getLidarData(I2C,I2C_ADDR,CMD):
    temp = bytes(9)          
    
    I2C.writeto(I2C_ADDR, CMD)
    temp = I2C.readfrom(16, 9)

    if temp[0] == 0x59 and temp[1] == 0x59 :
        distance   = temp[2] + temp[3] * 256            #DistanceValue
        strengh    = temp[4] + temp[5] * 256            #signal strength
        temperature= (temp[6] + temp[7]* 256)/8-256     #Chip temperature
        print("distance =%5dcm,strengh = %5d,temperature = %5d℃"%(distance,strengh,temperature))
        
time.sleep(1)  
while True:
    getLidarData(i2c0,address,getLidarDataCmd) # Radar data was obtained and analyzed
    time.sleep(0.1) 

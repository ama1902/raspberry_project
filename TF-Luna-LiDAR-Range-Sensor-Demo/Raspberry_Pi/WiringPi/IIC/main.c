#include <wiringPi.h>
#include <wiringPiI2C.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#define I2C_ADDR 0x10             // Radar module communication address
#define CMD_LEN  5                // Number of sent instruction bytes
#define RECV_LEN 10                // Number of bytes of data received. 

unsigned char buf[CMD_LEN] = {0x5A,0x05,0x00,0x01,0x60}; // Data fetch instruction
unsigned char recvBuf[RECV_LEN] = {0}; // Receiving data buffer

void getLidarData(int fd)
{
    write(fd, buf,5); // Send fetch distance value instruction

    delay(50); // Wait for the module to return the distance data
    read(fd,recvBuf,9); 
    if (recvBuf[0] == 0x59 && recvBuf[1] == 0x59) // data validation
        {
            int distance    = recvBuf[2] + recvBuf[3] * 256;                                   // DistanceValue
            int strength    = recvBuf[4] + recvBuf[5] * 256;                                   // signal strength
            int temperature = (recvBuf[6] + recvBuf[7] * 256) / 8 - 256;                       // Chip temperature
            printf("distance = %5d cm, strength = %5d, temperature = %5d ℃\n", distance, strength, temperature);
        }
    
}

int main(void)
{
    int tf=wiringPiI2CSetup(I2C_ADDR);
    printf("I2C slave address: 0x%x\n", I2C_ADDR);
    while (1)
    {
        getLidarData(tf); // Radar data was obtained and analyzed
        delay(10);        
    }

    return 0;
}
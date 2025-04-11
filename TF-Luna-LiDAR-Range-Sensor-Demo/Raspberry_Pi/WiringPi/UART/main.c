#include <stdio.h>
#include <wiringPi.h>
#include <unistd.h>
#include <wiringSerial.h>
#include <termios.h>

#define SERIAL_PORT "/dev/ttyS0"
#define BAUD_RATE 115200

void read_data(int serial_fd) {
    delayMicroseconds(1000000); //Sleep 1000ms
    while(1) {
    
        delayMicroseconds(10000); //Sleep 10ms
        if(serialDataAvail(serial_fd) > 8) { //Determines the number of bytes received by the serial port
            unsigned char bytes_serial[9];
            read(serial_fd, bytes_serial, 9);
            tcflush(serial_fd, TCIFLUSH); //Clear the serial port receive buffer
            
            
            if(bytes_serial[0] == 0x59 && bytes_serial[1] == 0x59) {
                int distance = bytes_serial[2] + bytes_serial[3] * 256;
                int strength = bytes_serial[4] + bytes_serial[5] * 256;
                int temperature = bytes_serial[6] + bytes_serial[7] * 256; // For TFLuna
                temperature = (temperature / 8) - 256;
                
                printf("TF-Luna C portion\n");
                printf("Distance: %d cm\n", distance);
                printf("Strength: %d\n", strength);
                if(temperature != 0) {
                    printf("Chip Temperature: %d℃\n", temperature);
                }
                
                
            }
        }
    }
}

int main() {
    int serial_fd;
    
    serial_fd = serialOpen(SERIAL_PORT, BAUD_RATE);
     
    read_data(serial_fd);
    return 0;
}

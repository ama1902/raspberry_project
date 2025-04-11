# Raspberry-Pi pan and tilt using arrow keys script
# must be run from Pi's terminal!
# use code "python KeyboardPanTilt.py" after you cd into the correct folder!

# Importing required libraries
import curses
import os
import time
import pantilthat

# Initialise camera

# Set up key mappings and curses for arrow key responses
screen = curses.initscr()  # Get the curses screen window
curses.noecho()            # Turn off input echoing
curses.cbreak()            # Respond to keys immediately (don't wait for enter)
screen.keypad(True)        # Map arrow keys to special values

# Initialise pan and tilt positions and process increments driven by arrow keys
# Set start-up servo positions
pan_angle = 0.0
tilt_angle = 0.0
pantilthat.pan(pan_angle)
pantilthat.tilt(tilt_angle)

# Set arrow key delta
delta_pan = 1.0
delta_tilt = 1.0

pic_num = 1  # Initialise picture number

# Process active key presses
# -- Letter 'p' will take a picture and store as image[pic_num].jpg
# -- Arrow keys control Pan Tilt Camera (delta_pan/delta_tilt degrees)
# -- Letter 'q' will quit the application
try:
    while True:
        char = screen.getch()
        if char == ord('q'):
            # If 'q' is pressed, quit
            break
        elif char == curses.KEY_RIGHT:
            screen.addstr(0, 0, 'Moving right    ')
            if (pan_angle - delta_tilt) > -90:
                pan_angle -= delta_tilt
            pantilthat.pan(pan_angle)
            time.sleep(0.005)
        elif char == curses.KEY_LEFT:
            screen.addstr(0, 0, 'Moving left     ')
            if (pan_angle + delta_tilt) < 90:
                pan_angle += delta_tilt
            pantilthat.pan(pan_angle)
            time.sleep(0.005)
        elif char == curses.KEY_DOWN:
            screen.addstr(0, 0, 'Moving down     ')
            if (tilt_angle + delta_pan) < 90:
                tilt_angle += delta_pan
            pantilthat.tilt(tilt_angle)
            time.sleep(0.005)
        elif char == curses.KEY_UP:
            screen.addstr(0, 0, 'Moving up       ')
            if (tilt_angle - delta_pan) > -90:
                tilt_angle -= delta_pan
            pantilthat.tilt(tilt_angle)
            time.sleep(0.005)
finally:
    # Shut down cleanly
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()


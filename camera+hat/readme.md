version 1 is start from last week

version 2 -  added a function that lets me see the HSV value of what i want to detect

version 3 - added a function that sets the HSV extracted from v2 into the taskbar, so that you can select which colour  to track (line 69-86)

version 4 - implemented the lidar, showing distance, siignal strenght, chip temperature on the frame

version 5 - fixed issue with window positioning (simply added cvmovewindow(position)) and fixed issue with mouse/training method (mistake was  i was never stopping the mousecallback function)

version6 - trying to add pid
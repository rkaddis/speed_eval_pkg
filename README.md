# speed_eval_pkg
ROS Project for evaluating speed control for human/automated drivers <br>
Intended for use in LTU's Lot H testing course
<br> <br>
Reports the time taken, average speed, and distance covered above the speed limit for 2 laps of the course. 
<br> <br>
<b> Running </b> <br>
Run program with: $ roslaunch speed_eval_pkg speed_eval.launch <br>
Requires '/vehicle/steering_report' messages from dbw_polaris_msgs.
<br> <br>
<b> Use </b> <br>
After launching, a dynamic reconfigure window will open. <br>
The 'max_speed' slider can be configured to set the speed limit for the course. The unit is mph. <br>
Check the 'start_test' box to begin testing. The program will only start evaluating vehicle data until the vehicle
reaches 0.1 m/s. <br>
After the first lap, ensure the driver comes to a complete stop at the line, and waits 3 seconds before starting
the second lap. <br>
Once the second lap has started, the 'start_test' box can be unchecked at any time. The test will end once the vehicle comes
to a complete stop. <br>
Total time, average speed, and distance covered over the speed limit will be reported to the terminal window. <br>

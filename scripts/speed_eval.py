#!/usr/bin/env python3
#Evaluate a driver's speed control

import rospy
from dynamic_reconfigure.server import Server
from speed_eval_pkg.cfg import SpeedEvalConfig   # packageName.cfg
from dbw_polaris_msgs.msg import SteeringReport

global dist_over_limit, over_limit, start_timer, t0, perimeter, prev_time, over_counter

dist_over_limit = 0 #distance covered when speed >max_speed
over_limit = False
start_timer = False
t0 = 0
perimeter = 105.6814 #Total length of course
over_counter = 0


def dyn_rcfg_cb(config, level):
    global start_test, max_speed
    start_test = config.start_test
    max_speed = config.max_speed
    return config
  
def steer_callback(data):
    
    global dist_over_limit, over_limit, start_timer, t0, perimeter, prev_time
    if(start_test and not start_timer and data.speed > 0.01):
        t0 = rospy.Time.now()
        rospy.loginfo("Test started...")
        start_timer = True
        dist_over_limit = 0
        
    if(start_timer and not over_limit and data.speed > max_speed * 0.44704):
        prev_time = rospy.Time.now()
        rospy.loginfo("Over speed limit!")
        over_limit = True
        
    if(start_timer and over_limit and data.speed > max_speed * 0.44704):
        curr_time = rospy.Time.now()
        dt = curr_time - prev_time
        #rospy.loginfo(f"{dt.to_sec()}")
        dist_over_limit = dist_over_limit + (data.speed * dt.to_sec())
        rospy.loginfo(f"{dist_over_limit}")
        prev_time = curr_time
    
    if(start_timer and over_limit and not data.speed > max_speed * 0.44704):
        rospy.loginfo("Normal speed recovered.")
        over_limit = False
        
    if(start_timer and not start_test and not data.speed > 0.1):
        t1 = rospy.Time.now()
        total_time = (t1-t0).to_sec()
        avg_speed = ((perimeter * 2) / (total_time - 3)) * 2.2369
        rospy.loginfo("####### TEST COMPLETE #######")
        rospy.loginfo(f"Total Time: {total_time}")
        rospy.loginfo(f"Average Speed: {avg_speed}mph")
        rospy.loginfo(f"Distance Traveled over {max_speed} mph: {dist_over_limit}")
        rospy.loginfo("#############################")
        start_timer = False
        
if __name__ == '__main__':
    rospy.init_node("speed_eval", anonymous=True)
    rospy.Subscriber('/vehicle/steering_report', SteeringReport, steer_callback)
    srv = Server(SpeedEvalConfig, dyn_rcfg_cb)
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    
    
    
    
    
    
    
    
    
    

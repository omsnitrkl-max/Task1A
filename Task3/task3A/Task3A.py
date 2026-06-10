#!/usr/bin/env pythonimport time
import time
from geometry_msgs import msg
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
start=time.time()
class DrawCircleNode(Node):
    def __init__(self):
        super().__init__('draw_circle')
        self.cmd_vel_pub_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 100)
        self.timer_=self.create_timer(0,self.send_velocity_command)
        self.get_logger().info('Draw Circle Node has been started.')


    def send_velocity_command(self):
        if time.time()-start>6.32 and time.time()-start<12.5:
            a=-1.0
            b=2.0
        elif time.time()-start>12.5:
            a=0.0
            b=0.0
        else:
            a=1.0
            b=2.0
        msg=Twist()
        msg.linear.y = b
        msg.angular.z = a
        self.cmd_vel_pub_.publish(msg)
   
def main(args=None):
    rclpy.init(args=args)
    node=DrawCircleNode()
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ == "__main__":
    main()

#Write your implementation
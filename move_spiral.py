#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node

from nav_msgs.msg import Odometry
from std_msgs.msg import Float64MultiArray

from bot_control.ik import inverse_kinematics


class SpiralTrajectory(Node):

    def __init__(self):

        super().__init__("spiral_trajectory")

        #Subscriber to /odom 

        self.create_subscription(
            Odometry,
            "/odom",
            self.odom_callback,
            10
        )

        #Publisher to wheel controller

        self.wheel_pub = self.create_publisher(
            Float64MultiArray,
            "/wheel_velocity_controller/commands",
            10
        )

        #Current robot pose (from /odom) 

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        # Spiral trajectory parameters 

        self.r_growth=0.1     
        self.omega_traj=0.3   

        self.t=0.0

        #  Controller gain 

        self.Kp=1.0

        # Timer for control loop 

        self.dt=0.05   
        self.create_timer(self.dt, self.control_loop)

    def odom_callback(self,msg):

        self.x=msg.pose.pose.position.x
        self.y=msg.pose.pose.position.y

        q=msg.pose.pose.orientation

        # Yaw from quaternion)
        self.theta=2.0 *math.atan2(q.z,q.w)

    def control_loop(self):

        # Desired point on the spiral

        r = self.r_growth*self.t

        x_d = r*math.cos(self.omega_traj*self.t)
        y_d = r*math.sin(self.omega_traj*self.t)

        self.t +=self.dt

        #Position error (world frame)

        error_x=x_d-self.x
        error_y=y_d-self.y

        #Desired velocity in world frame

        vx_world=self.Kp*error_x
        vy_world=self.Kp*error_y

      

        vx=(
            vx_world*math.cos(self.theta)
            +vy_world*math.sin(self.theta)
        )

        vy = (
            -vx_world*math.sin(self.theta)
            +vy_world*math.cos(self.theta)
        )

        omega=0.0   

        # Inverse Kinematics 

        wl,wr,wb =inverse_kinematics(vx,vy,omega)

        # wheel velocities

        msg=Float64MultiArray()
        msg.data = [wl,wr,wb]

        self.wheel_pub.publish(msg)


def main(args=None):

    rclpy.init(args=args)

    node = SpiralTrajectory()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()

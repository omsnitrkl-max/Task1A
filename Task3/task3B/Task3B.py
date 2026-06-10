#!/usr/bin/env python3

#Write your implementation

import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class GoToPoints(Node):
    def __init__(self):
        super().__init__("task3b")

        self.pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.sub = self.create_subscription(Pose, "/turtle1/pose", self.get_pose, 10)

        self.x = 0.0
        self.y = 0.0
        self.th = 0.0
        self.got_pose = False

        self.i = 0

        self.points = [
            [5.5, 9.5],
            [7.0, 5.5],
            [10.0, 5.5],
            [7.8, 3.0],
            [9.0, 0.5],
            [5.5, 2.5],
            [2.0, 0.5],
            [3.2, 3.0],
            [1.0, 5.5],
            [4.0, 5.5],
            [5.5, 9.5],
        ]

        self.timer = self.create_timer(0.05, self.run)

    def get_pose(self, data):
        self.x = data.x
        self.y = data.y
        self.th = data.theta
        self.got_pose = True

    def fix_angle(self, a):
        if a > math.pi:
            a = a - 2.0 * math.pi
        if a < -math.pi:
            a = a + 2.0 * math.pi
        return a

    def run(self):
        if not self.got_pose:
            return

        vel = Twist()

        if self.i == len(self.points):
            self.pub.publish(vel)
            self.get_logger().info("All points done")
            self.destroy_timer(self.timer)
            return

        gx = self.points[self.i][0]
        gy = self.points[self.i][1]

        dx = gx - self.x
        dy = gy - self.y

        dist = math.sqrt(dx * dx + dy * dy)
        ang = math.atan2(dy, dx)
        turn = self.fix_angle(ang - self.th)

        if dist < 0.2:
            self.i = self.i + 1
            self.pub.publish(vel)
            self.get_logger().info("Point reached")
            return

        if abs(turn) > 0.2:
            vel.linear.x = 0.0
            vel.angular.z = 2.0 * turn
        else:
            vel.linear.x = 1.4
            vel.angular.z = turn

        self.pub.publish(vel)


def main(args=None):
    rclpy.init(args=args)

    obj = GoToPoints()
    rclpy.spin(obj)

    obj.pub.publish(Twist())
    obj.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
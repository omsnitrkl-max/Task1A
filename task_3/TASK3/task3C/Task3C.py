#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from turtlesim.msg import Pose
from turtlesim.srv import Spawn
from geometry_msgs.msg import Twist

import math
import random


class Task3C(Node):

    def __init__(self):

        super().__init__("task3c")

        self.thief_pose = None
        self.police_pose = None
        self.goal_x = random.uniform(1.0, 8.0)
        self.goal_y = random.uniform(1.0, 8.0)

        self.goal_timer = 0.0

        # ============================
        # Spawn Police Turtle
        # ============================

        self.spawn_client = self.create_client(
            Spawn,
            "/spawn"
        )

        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(
                "Waiting for spawn service..."
            )

        req = Spawn.Request()

        req.x = random.uniform(1.0, 5.0)
        req.y = random.uniform(5.0, 10.0)
        req.theta = 0.0
        req.name = "police"

        future = self.spawn_client.call_async(req)

        rclpy.spin_until_future_complete(
            self,
            future
        )

        self.get_logger().info(
            "Police spawned"
        )

        # ============================
        # Subscribers
        # ============================
        self.create_subscription(
            Pose,
            "/turtle1/pose",
            self.thief_callback,
            10
        )

        self.create_subscription(
            Pose,
            "/police/pose",
            self.police_callback,
            10
        )

        # ============================
        # Publishers
        # ============================
        self.thief_pub = self.create_publisher(
            Twist,
            "/turtle1/cmd_vel",
            10
        )

        self.police_pub = self.create_publisher(
            Twist,
            "/police/cmd_vel",
            10
        )

        self.timer = self.create_timer(
            0.1,
            self.control_loop
        )

    def thief_callback(self, msg):
        self.thief_pose = msg

    def police_callback(self, msg):
        self.police_pose = msg

    def control_loop(self):

        if self.thief_pose is None:
            return

        if self.police_pose is None:
            return

        # ==================================
        # PROVIDED THIEF LOGIC
        # ==================================

        self.goal_timer += 0.1

        if self.goal_timer >= 2.0:

            self.goal_timer = 0.0

            self.goal_x = random.uniform(
                1.0,
                10.0
            )

            self.goal_y = random.uniform(
                1.0,
                10.0
            )

        dx = self.goal_x - self.thief_pose.x
        dy = self.goal_y - self.thief_pose.y

        desired_theta = math.atan2(
            dy,
            dx
        )

        angle_error = (
            desired_theta -
            self.thief_pose.theta
        )

        while angle_error > math.pi:
            angle_error -= 2 * math.pi

        while angle_error < -math.pi:
            angle_error += 2 * math.pi

        thief_cmd = Twist()

        thief_cmd.angular.z = (
            6.0 * angle_error
        )

        if abs(angle_error) < 0.4:
            thief_cmd.linear.x = 4.0
        else:
            thief_cmd.linear.x = 0.0

        self.thief_pub.publish(
            thief_cmd
        )


        # ==================================
        # STUDENT SECTION
        # ==================================

        #
        # Objective:
        # Catch turtle1
        #
        # Available:
        # self.thief_pose
        # self.police_pose
        # self.police_pub
        #
        # Publish velocity commands
        # using self.police_pub
        #
        # Do not modify thief logic.
        
        dx = self.thief_pose.x - self.police_pose.x
        dy = self.thief_pose.y - self.police_pose.y

        distance = math.sqrt(dx * dx + dy * dy)

        if distance < 0.5:
            stop_cmd = Twist()
            self.police_pub.publish(stop_cmd)

            self.get_logger().info(
                "THIEF CAPTURED!"
            )
            self.timer.cancel()
            return

        desired_theta = math.atan2(
            dy,
            dx
        )

        angle_error = (
            desired_theta -
            self.police_pose.theta
        )

        while angle_error > math.pi:
            angle_error -= 2 * math.pi

        while angle_error < -math.pi:
            angle_error += 2 * math.pi

        police_cmd = Twist()

        police_cmd.angular.z = (
            6.0 * angle_error
        )

        if abs(angle_error) < 0.4:
            police_cmd.linear.x = 4.0
        else:
            police_cmd.linear.x = 0.0

        self.police_pub.publish(
            police_cmd
        )


def main(args=None):

    rclpy.init(args=args)

    node = Task3C()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()
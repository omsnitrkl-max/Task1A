#!/usr/bin/env python3

import math


def inverse_kinematics(vx,vy,omega):

    # Wheel radius
    r=0.15

    # Distance from the robot centre to each wheel
    l=0.68

    # Left wheel
    wl=(vx-l *omega)/r

    # Right wheel
    wr=(
        -0.5*vx -(math.sqrt(3)/2)*vy- l*omega
    ) /r

    # Rear wheel
    wb =(
        -0.5* vx+(math.sqrt(3)/2)*vy-l*omega
    )/r

    return wl,wr,wb


def main():

    vx = float(input("vx (m/s): "))
    vy = float(input("vy (m/s): "))
    omega = float(input("omega (rad/s): "))

    wl, wr, wb = inverse_kinematics(vx, vy, omega)

    print(f"\nLeft wheel  : {wl:.3f} rad/s")
    print(f"Right wheel : {wr:.3f} rad/s")
    print(f"Rear wheel  : {wb:.3f} rad/s")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3

import math


def forward_kinematics(omega_left,omega_right,omega_rear):

    # Wheel radius
    r=0.15

    # Distance from robot center to each wheel
    l=0.68

    # Forward kinematics

    vx=(2*r*omega_left-r*omega_right-r *omega_rear)/3

    vy=(r*(omega_rear-omega_right))/math.sqrt(3)

    omega=-(r *(omega_left+omega_right+omega_rear))/(3*l)

    return vx,vy,omega


def main():

    wl = float(input("Left wheel (rad/s): "))
    wr = float(input("Right wheel (rad/s): "))
    wb = float(input("Rear wheel (rad/s): "))

    vx, vy, omega = forward_kinematics(
        wl,
        wr,
        wb
    )

    print(f"\nvx     : {vx:.3f} m/s")
    print(f"vy     : {vy:.3f} m/s")
    print(f"omega  : {omega:.3f} rad/s")


if __name__ == "__main__":
    main()
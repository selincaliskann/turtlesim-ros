#!/usr/bin/env python3

import rospy
import math
from turtlesim.srv import TeleportAbsolute, SetPen

class TurkishFlagDrawer:
    def __init__(self):
        rospy.init_node('turkish_flag_drawer')
        rospy.wait_for_service('/turtle1/teleport_absolute')
        rospy.wait_for_service('/turtle1/set_pen')
        self.teleport = rospy.ServiceProxy('/turtle1/teleport_absolute', TeleportAbsolute)
        self.set_pen = rospy.ServiceProxy('/turtle1/set_pen', SetPen)

    def draw_circle(self, center_x, center_y, radius, step_size=0.02, delay=0.05):
        """Draw a smooth and slow circle."""
        for angle in range(0, 360, int(step_size * 360)):
            x = center_x + radius * math.cos(math.radians(angle))
            y = center_y + radius * math.sin(math.radians(angle))
            self.teleport(x, y, 0.0)
            rospy.sleep(delay)

    def draw_star(self, center_x, center_y, size, delay=0.1):
        """Draw a 5-pointed star."""
        points = [
            (center_x + size * math.cos(math.radians(72 * i)),
             center_y + size * math.sin(math.radians(72 * i)))
            for i in range(5)
        ]
        for i in range(5):
            self.teleport(points[i][0], points[i][1], 0.0)
            rospy.sleep(delay)
            next_point = points[(i + 2) % 5]
            self.teleport(next_point[0], next_point[1], 0.0)
            rospy.sleep(delay)

    def draw_turkish_flag(self):
        """Draw the Turkish flag."""
        rospy.set_param('/turtlesim/background_r', 255)
        rospy.set_param('/turtlesim/background_g', 0)
        rospy.set_param('/turtlesim/background_b', 0)
        rospy.sleep(1)  # Allow background change to take effect

        # Draw crescent
        self.set_pen(255, 255, 255, 2, 0)
        self.draw_circle(5.5, 5.5, 2, step_size=0.02, delay=0.05)
        self.set_pen(255, 0, 0, 2, 0)
        self.draw_circle(6.0, 5.5, 1.5, step_size=0.02, delay=0.05)

        # Draw star
        self.set_pen(255, 255, 255, 2, 0)
        self.draw_star(7.5, 5.5, 1.0, delay=0.1)

    def run(self):
        """Run the flag drawing process."""
        self.draw_turkish_flag()
        rospy.loginfo("Turkish flag drawn successfully!")

if __name__ == '__main__':
    try:
        TurkishFlagDrawer().run()
    except rospy.ROSInterruptException:
        pass


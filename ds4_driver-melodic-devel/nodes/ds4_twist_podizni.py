#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist, TwistStamped
from ds4_driver.msg import Status

from std_msgs.msg import Bool
from std_msgs.msg import Int16


class StatusToTwist(object):
    def __init__(self):
        self._stamped = rospy.get_param('~stamped', False)
        if self._stamped:
            self._cls = TwistStamped
            self._frame_id = rospy.get_param('~frame_id', 'base_link')
        else:
            self._cls = Twist
        self._inputs = rospy.get_param('~inputs')
        self._scales = rospy.get_param('~scales')

	print(self._inputs)
	
	self._podizni_obj = Int16
	#self._in_podizni_g = rospy.get_param('~podizni_gore')
	#self._in_podizni_d = rospy.get_param('~podizni_dolje')

	

        self._attrs = []
        for attr in Status.__slots__:
            if attr.startswith('axis_') or attr.startswith('button_'):
                self._attrs.append(attr)

	print(self._attrs)

        self._pub = rospy.Publisher('cmd_vel', self._cls, queue_size=1)
        rospy.Subscriber('status', Status, self.cb_status, queue_size=1)

	self._pub2 = rospy.Publisher('podizni', self._podizni_obj, queue_size=1)

    def cb_status(self, msg):
        """
        :param msg:
        :type msg: Status
        :return:
        """
        input_vals = {}
        for attr in self._attrs:
            input_vals[attr] = getattr(msg, attr)
	

	podizni_pub = self._podizni_obj()

	podizni_val_up = getattr(msg, 'button_dpad_up')
	#print(podizni_val_up)

	podizni_val_down = getattr(msg, 'button_dpad_down')
	#print(podizni_val_down)

	if podizni_val_up == 1:
            podizni_pub.data = 1

	elif podizni_val_down == 1:
            podizni_pub.data = -1
	

        to_pub = self._cls()
        if self._stamped:
            to_pub.header.stamp = rospy.Time.now()
            to_pub.header.frame_id = self._frame_id
            twist = to_pub.twist
        else:
            twist = to_pub

        for vel_type in self._inputs:
            vel_vec = getattr(twist, vel_type)
            for k, expr in self._inputs[vel_type].items():
                scale = self._scales[vel_type].get(k, 1.0)
                val = eval(expr, {}, input_vals)
                setattr(vel_vec, k, scale * val)

        self._pub.publish(to_pub)

	self._pub2.publish(podizni_pub)

        


def main():
    rospy.init_node('ds4_twist')

    StatusToTwist()

    rospy.spin()


if __name__ == '__main__':
    main()

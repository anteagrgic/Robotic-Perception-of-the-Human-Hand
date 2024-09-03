#!/usr/bin/env python

import moveit_commander, rospy
from geometry_msgs.msg import Pose
import roslib
from time import time
from trac_ik_python.trac_ik import IK 

roslib.load_manifest('robotiq_3f_gripper_control')

from robotiq_3f_gripper_articulated_msgs.msg import Robotiq3FGripperRobotOutput

class RobotControl:
    def __init__(self):
        rospy.init_node('move_robot', anonymous=True)

        # definirati instancu
        self.robot = moveit_commander.RobotCommander()

        # definirati scenu
        self.scene = moveit_commander.PlanningSceneInterface()

        # stvoriti objekt koji pruza sucelje za planiranje pomaka za definiranu grupu u setup assistant-u
        self.group_name = "manipulator"
        self.move_group = moveit_commander.MoveGroupCommander(self.group_name)
        
        #INVERSE KINEMATICS
        self.ik = IK('base_link', 'tool0', solve_type="Distance")


    def get_current_pose(self):
        return self.move_group.get_current_pose().pose
        

    def set_pose_and_execute(self, pose):
        x = pose.position.x
        y = pose.position.y
        z = pose.position.z
        qx = pose.orientation.x
        qy = pose.orientation.y
        qz = pose.orientation.z
        qw = pose.orientation.w

        current_joints = self.move_group.get_current_joint_values()
        goal_joints = self.ik.get_ik(current_joints, x, y, z, qx, qy, qz, qw)

        print("Inverse kin:")
        print(goal_joints)

        joint_goal = self.move_group.get_current_joint_values()
        joint_goal[0] = goal_joints[0]
        joint_goal[1] = goal_joints[1]
        joint_goal[2] = goal_joints[2]
        joint_goal[3] = goal_joints[3]
        joint_goal[4] = goal_joints[4]
        joint_goal[5] = goal_joints[5]
        
        self.move_group.go(joint_goal, wait=True)

        self.move_group.stop()


    def execute_trajectory(self, plan):
        self.move_group.execute(plan, wait=True)


if __name__ == '__main__':
    
    # instanca upravljaca robotom

    RC = RobotControl()
    StartPose = RC.get_current_pose()

    while not rospy.is_shutdown():
        current_pose = RC.get_current_pose()
        x = input("ODABERI POZICIJU 1, 2 ILI 3")

        goal_pose = Pose()
        goal_pose.orientation = current_pose.orientation
        goal_pose.position = current_pose.position

        if x == "1":
            goal_pose = StartPose
        elif x == "2":
            goal_pose.position.x = -0.4
            goal_pose.position.z = 0.5
        elif x=="3":
            goal_pose.position.x = 0.4
            goal_pose.position.z = 0.5
        # goal_pose.position.x = 0
        # goal_pose.position.y = 0
        # goal_pose.position.z = 0

        RC.set_pose_and_execute(goal_pose)
 
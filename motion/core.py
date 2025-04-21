#!/usr/bin/python3

#
#   Developer : Mikhail Filchenkov (m.filchenkov@gmail.com)
#   All rights reserved. Copyright (c) 2025 Applied Robotics.
#

import os
import motorcortex
from math import *
from robot_control.motion_program import Waypoint, MotionProgram, PoseTransformer
from robot_control.robot_command import RobotCommand
from robot_control.system_defs import *
from system_def import Path, JoyVelicity
import logging
import threading

class RobotControl(object):
    """
    Class represents a control machine of the robot ARM.
    Args:
        ip(str): IP-address robot ARM
        port(str): Port robot ARM
        login(str): login robot ARM
        password(str): password robot ARM

    """
        
    def __init__(self, ip='192.168.56.101', port='5568:5567', login='*', password='*'):
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(levelname)s: %(message)s'
        )

        self.__hostname = ip
        self.__port = port
        self.__login = login
        self.__password = password
        self.__pathCert = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mcx.cert.pem')
        
    def connect(self):
        """
        Connect to the robot ARM
            Returns:
                bool: True if operation is completed, False if failed
            
        """
        
        parameter_tree = motorcortex.ParameterTree()
        self.__messageTypes = motorcortex.MessageTypes()
        try:
            self.__req, sub = motorcortex.connect("ws://" + self.__hostname + ":" + self.__port,
                                                self.__messageTypes, parameter_tree,
                                                certificate=self.__pathCert, timeout_ms=1000,
                                                login=self.__login, password=self.__password)
            
            self.__robot = RobotCommand(self.__req, self.__messageTypes)
            tree_req = self.__req.getParameterTree()
            params = tree_req.get()
            with open("parameters_new.txt", "w", encoding="utf-8") as f:
                f.write(str(params))
            logging.info("Robot ARM connected")
            return True
        
        except RuntimeError as err:
            logging.error(err)
            return False
        
    def engage(self):
        """
        Engage motor to the robot ARM
            Returns:
                bool: True if operation is completed, False if failed
        
        """
        try:
            if self.__robot.engage():
                logging.info("Robot is Engage")
                return True
                
        except RuntimeError as err:
            logging.error(err)
            return False
        
    def disengage(self):
        """
        Disngage motor to the robot ARM
            Returns:
                bool: True if operation is completed, False if failed
        
        """
        try:
            if self.__robot.disengage():
                self.__robot.off()
                logging.info("Robot is Disengage")
                return True
            
        except RuntimeError as err:
            logging.error(err)
            return False

    def manualCartMode(self):
        """
        Set manual cartesian mode for robot ARM.
            Returns:
                bool: True if operation is completed, False if failed
        
        """

        try:
            if self.__robot.manualCartMode():
                logging.info("Cartesian mode active")
                return True
            
        except RuntimeError as err:
            logging.error(err)
            return False
        
    def manualJointMode(self):
        """
        Set manual joint mode for robot ARM.
            Returns:
                bool: True if operation is completed, False if failed
        
        """

        try:
            if self.__robot.manualJointMode():
                logging.info("Joint mode active")
                return True
            
        except RuntimeError as err:
            logging.error(err)
            return False

    def setJointVelocity(self, velicity=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]):
        """
        Robot ARM control in joint mode by joysticks.
            Args:
                velocity(list(double)): joint velocity (motor1, motor2, motor3, motor4, motor5, motor6)

            Returns:
                bool: ARM parameter if operation is completed, False if failed
        
        """

        actual_state = self.__req.getParameter(Path.ROBOT_MODE.value).get().value[0]
        if actual_state is ModeCommands.GOTO_MANUAL_JOINT_MODE_E.value:
            if len(velicity) == 6:
                cap_vel = self.__cap_velocity(velicity, JoyVelicity.MAX_JOY_VELOCITY_JOINT.value)
                return self.__req.setParameter(Path.HOSTIN_JOINT_VELOCITY.value, cap_vel).get()
            else:
                logging.warning("The number of values doesn't correspond to the number of motors")
                return False

        else:
            logging.info("Actual robot state isn't joint mode")
            return False
        
    def setCartesianVelocity(self, velicity=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]):
        """
        Robot ARM control in cartesian mode by joysticks.
            Args:
                velocity(list(double)): cartesian velocity (x, y, z, rx, ry, rz)

            Returns:
                bool: ARM parameter if operation is completed, False if failed
        
        """

        actual_state = self.__req.getParameter(Path.ROBOT_MODE.value).get().value[0]
        if actual_state is ModeCommands.GOTO_MANUAL_CART_MODE_E.value:
            if len(velicity) == 6:
                cap_vel = self.__cap_velocity(velicity, JoyVelicity.MAX_JOY_VELOCITY_CARTESIAN.value)
                return self.__req.setParameter(Path.HOSTIN_TOOL_VELOCITY.value, cap_vel).get()
            else:
                logging.warning("The number of values doesn't correspond to the tool")
                return False

        else:
            logging.info("Actual robot state isn't cartesian mode")
            return False
    
    def moveToStart(self):
        """
        Robot ARM control in cartesian mode by joysticks.
            Returns:
                bool: ARM parameter if operation is completed, False if failed
        
        """
        self.__robot.semiAutoMode()
        motion_program = MotionProgram(self.__req, self.__messageTypes)    
        start_point = []
        start_point.append(Waypoint([radians(0), radians(0), radians(90), radians(0), radians(90), radians(0)]))
        motion_program.addMoveJ(start_point, 0.05, 0.1)

        motion_program.send("move_to_start_point").get() 
        # self.__robot.play(wait_time=0.25)

        if self.__robot.play(wait_time=0.25) is InterpreterStates.MOTION_NOT_ALLOWED_S.value:
            if self.__robot.moveToStart(200):
                logging.info("Robot move to start position")
            else:
                logging.warning('Failed to move to the start position')
            
        motion_program.send("move_to_start_point").get() 
        self.__robot.play(wait_time=0.25)

        while not(self.__robot.play(wait_time=0.25) is InterpreterStates.PROGRAM_IS_DONE.value):
            pass
        else:
            logging.info('Robot is at the start position')
            return True
        
    def activateMoveToStart(self):
        """
        Manual activate move to start robot ARM.
        Description:
            Used for the button
        
        """
        logging.info("Robot move to start")
        self.__req.setParameter(Path.ACTIVATE_MOVE_TO_START.value, 1).get()
    
    def moveToPointL(self, waypoint_list, tool=0, velocity=0.1, acceleration=0.2,
                 rotational_velocity=3.18, rotational_acceleration=6.37,
                 ref_joint_coord_rad=[]):
        """
        Adds a MoveL(Linear move) command to the program
        Args:
            waypoint_list(list(WayPoint)): a list of waypoints
            tool(int): state of robot tool
            velocity(double): maximum velocity, m/sec
            acceleration(double): maximum acceleration, m/sec^2
            rotational_velocity(double): maximum joint velocity, rad/sec
            rotational_acceleration(double): maximum joint acceleration, rad/sec^2
            ref_joint_coord_rad: reference joint coordinates for the first waypoint
        Description:
            Waypoint([x, y, z, rx, ry, rz]) - the waypoint is set as the absolute position of the manipulator in meters

        """
        # if tool == 1:
        #     self.__toolON()
        # else:
        #     self.__toolOFF()
        # self.__robot.semiAutoMode()
        motion_program = MotionProgram(self.__req, self.__messageTypes) 
        motion_program.addMoveL(waypoint_list, velocity, acceleration,
                 rotational_velocity, rotational_acceleration,
                 ref_joint_coord_rad)
        motion_program.send("move_to_point_l").get() 

    def moveToPointC(self, waypoint_list, angle, tool=0, velocity=0.1, acceleration=0.2,
                 rotational_velocity=3.18, rotational_acceleration=6.37,
                 ref_joint_coord_rad=[]):
        
        """
        Adds a MoveC(circular move) command to the program
        Args:
            waypoint_list(list(WayPoint)): a list of waypoints
            tool(int): state of robot tool
            angle(double): rotation angle, rad
            velocity(double): maximum velocity, m/sec
            acceleration(double): maximum acceleration, m/sec^2
            rotational_velocity(double): maximum joint velocity, rad/sec
            rotational_acceleration(double): maximum joint acceleration, rad/sec^2
            ref_joint_coord_rad: reference joint coordinates for the first waypoint
        Description:
            Waypoint([x, y, z, rx, ry, rz]) - the waypoint is set as the absolute position of the manipulator 
            x, y, z in meters (example: 0.85, -0.191, 0.921)
            rx, ry, rz in radians (example: pi/2, 0, pi)
        """
                
        # self.__robot.semiAutoMode()
        # if tool == 1:
        #     self.__toolON()
        # else:
        #     self.__toolOFF()

        motion_program = MotionProgram(self.__req, self.__messageTypes) 
        motion_program.addMoveC(waypoint_list, angle, velocity, acceleration,
                 rotational_velocity, rotational_acceleration,
                 ref_joint_coord_rad)
        motion_program.send("move_to_point_c").get() 

    def moveToPointJ(self, waypoint_list=[], tool=0,  rotational_velocity=3.18, rotational_acceleration=6.37):
        """
        Adds MoveJ(Joint move) command to the program
        Args:
            waypoint_list(list(WayPoint)): a list of waypoints
            tool(int): state of robot tool
            rotational_velocity(double): maximum joint velocity, rad/sec
            rotational_acceleration(double): maximum joint acceleration, rad/sec^2
        Description:
            Waypoint(0.0, 0.0, 1.57, 0.0, 1.57, 0.0) - the waypoint is set as the position of the motors in radians

        """

        # if tool == 1:
        #     self.__toolON()
        # else:
        #     self.__toolOFF()
        
        # self.__robot.semiAutoMode()
        motion_program = MotionProgram(self.__req, self.__messageTypes) 
        motion_program.addMoveJ(waypoint_list, rotational_velocity, rotational_acceleration)
        motion_program.send("move_to_point_j").get() 

    def play(self):
        """
        Needed for start robot programm
            Returns:
                InterpreterStates: actual state of the interpreter
        """
        logging.info("Robot programm play")
        if self.__robot.play(wait_time=0.25) is InterpreterStates.MOTION_NOT_ALLOWED_S.value:
            logging.info("Robot don't in start position")
        return self.__robot.play(wait_time=0.25)
    

    def pause(self):
        """
        Needed for pause robot programm
            Returns:
                InterpreterStates: actual state of the interpreter
        """
        logging.info("Robot programm pause")
        return self.__robot.pause()

    def stop(self):
        """
        Needed for stop robot programm
            Returns:
                InterpreterStates: actual state of the interpreter
        """
        logging.info("Robot programm stop")
        return self.__robot.stop()

    def reset(self):
        """
        Needed for reset robot programm
            Returns:
                InterpreterStates: actual state of the interpreter
        """
        logging.info("Robot programm reset")
        return self.__robot.reset()

    def __toolON(self):
        """
        Turns on the working tool
            Description:
                If there is a vacuum system, the suction cup is activated.
                In the presence of a gripping device, the grip is compressed.
            Returns:
                InterpreterStates: Tool of the IO
        """
        logging.info("Robot programm play")
        return self.__req.setParameter(Path.TOOL_CMD.value, 1).get()
    
    def __toolOFF(self):
        """
        Turns off the working tool
            Description:
                If there is a vacuum system, the suction cup is disactivated.
                In the presence of a gripping device, the grip is unclenches.
            Returns:
                InterpreterStates: Tool of the IO
        """
        logging.info("Robot programm play")
        return self.__req.setParameter(Path.TOOL_CMD.value, 0).get()
    
    def getRobotMode(self):
        """
        Returns:
            InterpreterStates: actual robot mode

        """
        
        return self.__req.getParameter(Path.ROBOT_MODE.value).get().value[0]
    
    def getRobotState(self):
        """
        Returns:
            InterpreterStates: actual robot state

        """
        
        return self.__req.getParameter(Path.ROBOT_STATE.value).get().value[0]
    
    def getActualStateOut(self):
        """
        Returns:
            InterpreterStates: actual state of the interpreter

        """
        return self.__req.getParameter(Path.STATE_CMD.value).get().value[0]
    
    def getMotorPositionTick(self):
        """
        Returns:
            list(float): actual encoder positions
        """
        return [self.__req.getParameter(tick).get().value[0] for tick in Path.CURRENT_JOINT_POSE_TICK.value]

    def getToolPosition(self):
        """
        Returns:
            list(float): actual tool positions
        """

        return self.__req.getParameter(Path.CURRENT_TOOL_POSE.value).get().value

    def getMotorPositionRadians(self):
        """
        Returns:
            list(float): actual motor positions in radians
        """
        return self.__req.getParameter(Path.CURRENT_JOINT_POSE_RADIANS.value).get().value
    
    def getManipulability(self):
        """
        Description:
            Ability to maneuver range 0..1
            0 - critical situation
            1 - safe situation
        
        Returns:
            float: actual manipulability
        """
                
        return self.__req.getParameter(Path.MANIPULABILITY_CMD).get().value[0]
        
    def getActualTemperature(self):
        """
        Returns:
            float: actual motor temperature
        """
                
        self.__req.setParameter(Path.READSDO_CMD.value, 1).get()
        return self.__req.getParameter(Path.MANIPULABILITY_CMD).get().value[0]

        
    def __cap_velocity(self, velocities, max_velocity):
        return [min(max(velocity, -max_velocity), max_velocity) for velocity in velocities]
    
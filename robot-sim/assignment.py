from __future__ import print_function

import time
from sr.robot import *

R = Robot()

# Robot constants
R.a_th = 2.0
R.d_th = 0.4
R.tokens_set = []
R.currently_held = -1
R.drive_speed = 100
R.turn_speed = 10
R.turn_interval = 0.1
R.drive_interval = 0.1
R.search_speed = 50
R.search_interval = 0.1
# This is not the best solution but is better than having a
# global variable before the functions that use this parameter
R.print_once_speed = True
R.print_once_anchor_warn = True

# Color constants
# pure debugging
DEBUG = "[\033[90mDEBUG\033[39m] - "
# general information
INFO = "[\033[96mINFO\033[39m] - "
# warning
WARN = "[\033[93mWARN\033[39m] - "
# relevant success
SUCC = "[\033[92mSUCC\033[39m] - "
# task completed successfully
COMP = "[\033[95mCOMP\033[39m] - "

# set this to True to print distance and rotations
DEBUG_INFO = False


def drive(speed, seconds):
    """
    Function for setting a linear velocity

    Args: speed (int): the speed of the wheels
          seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def turn(speed, seconds):
    """
    Function for setting an angular velocity

    Args: speed (int): the speed of the wheels
          seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def set_anchor():
    """
    Function to set the anchor

    Returns:
      - anchor (int): the numeric code of the marker
    """
    dist = 100
    while True:
        for token in R.see():
            if token.dist < dist:
                dist = token.dist
                anchor = token.info.code
        if dist == 100:
            turn(R.turn_speed, R.turn_interval)
        else:
            print(SUCC+"Anchor set")
            return anchor


def speed_regulator(dist):
    """
    Function to reduce speed when near the targets

    Args:
      - dist (float): distance between the robot and the
                      target

    Returns:
      - an appropriate drive speed (float)
    """
    if dist < 1:
        if R.print_once_speed:
            R.print_once_speed = False
            print(INFO+"Moderating speed for beeing near to target")
        return R.drive_speed/2
    else:
        R.print_once_speed = True
        return R.drive_speed


def retrieve_stack_pos(object_seen):
    """
    Function that allows the turtle to position the token
    next to the anchor if the anchor becomes no more visible

    Args:
      - object_seen (int): id of the object to collect
    Returns:
      - rot_y (float): relative rotation between robot and
                       token in polar coordinates
      - dist (float): distance between robot and token
    """
    if object_seen == R.anchor:
        # try if is not obstructed by other objects
        for token in R.see():
            if token.info.code == R.anchor:
                R.print_once_anchor_warn = True
                return (token.rot_y, token.dist)

        """
        if we arrive here the anchor cannot be found
        meaning it's hidden behind other tokens
        The best way to address the issue is to go towards
        a token that is already set
        """
        if R.print_once_anchor_warn:
            print(WARN+"The anchor could not be found "
                  "because hidden by other tokens")
            print(WARN+"Proceding towards one token already set")
            R.print_once_anchor_warn = False

        for token in R.see():
            if token.info.code in R.tokens_set:
                return (token.rot_y, token.dist)
    else:
        for token in R.see():
            if token.info.code == object_seen:
                return (token.rot_y, token.dist)


def move_robot_to(target):
    """
    Function that enables the turtle to go towards it's target.
    The target can be both the anchor or a token

    Args:
      - target (int): the id of the token
    """
    done = False
    while not done:
        (rot, dist) = retrieve_stack_pos(target)
        if DEBUG_INFO:
            print(DEBUG+"Dist: ", round(dist, 2), "\tRot: ", round(rot, 2))
        """
        Setting the rotation of the robot with an higher
        priority in respect to the starting to drive towards
        the target. In testing this seemed to have better
        results
        """
        if rot > R.a_th:
            turn(R.turn_speed, R.turn_interval)
        elif rot < -R.a_th:
            turn(-R.turn_speed, R.turn_interval)
        elif dist >= R.d_th:
            drive(speed_regulator(dist), R.drive_interval)

        """
        If the target of this function is the anchor then
        more distance is taken in consideration in the
        threshold for reaching the anchor because there is
        also the token attached to the grabber
        """
        if target == R.anchor:
            d_aux = R.d_th + 0.3
        else:
            d_aux = R.d_th

        """
        If the robot is alligned and close to the target
        then it's time to perform the required action
        """
        if rot < R.a_th and dist < d_aux:
            if target == R.anchor:
                print(SUCC+"Token carried successfully, releasing it")
                R.release()
                # Adds to the tokens positioned successfully
                # the last held token id
                R.tokens_set.append(R.currently_held)
                # Having released the token now the gripper is empty
                R.currently_held = -1
                done = True
                break
            else:
                print(SUCC+"Token reached successfully, grabbing it")
                R.grab()
                # Set currently held token id
                R.currently_held = target
                done = True
                break


def search_new_token():
    """
    Function to search a new token to take to the stack
    """
    print(INFO+"Searching for new token to take...")
    while 1:
        # Turning in the spot untill a token appears
        turn(R.search_speed, R.search_interval)
        for token in R.see():
            code = token.info.code
            # If the token is not already positioned then
            # it's time to go grab it
            if code not in R.tokens_set and code != R.anchor:
                print(SUCC+"Found new token!")
                move_robot_to(code)
                return


def search_anchor():
    """
    Function to search for the anchor
    """
    print(INFO+"Searching for the anchor...")
    while 1:
        # Turning in the spot untill the anchor appears
        turn(R.search_speed, R.search_interval)
        for token in R.see():
            if token.info.code == R.anchor:
                print(SUCC+"Found the anchor!")
                move_robot_to(R.anchor)
                return


def main():
    # setting the new anchor
    R.anchor = set_anchor()
    while 1:
        search_new_token()
        search_anchor()
        print(INFO+"Backing up...")
        drive(-R.drive_speed, 0.5)
        """
        If the number of tokens that have been positioned next
        to the anchor is 5 then we have finished the task
        """
        if (len(R.tokens_set) == 5):
            print(COMP+"Task completed!")
            exit(0)


main()

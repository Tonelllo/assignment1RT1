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


# TODO maybe remove
print_speed_once = True


def speed_regulator(dist):
    global print_speed_once
    """
    Function to reduce speed when near the targets

    Args:
      - dist (float): distance between the robot and the
                      target

    Returns:
      - an appropriate drive speed (float)
    """
    if dist < 1:
        if print_speed_once:
            print_speed_once = False
            print(INFO+"Moderating speed for beeing near to target")
        return R.drive_speed/2
    else:
        print_speed_once = True
        return R.drive_speed


# TODO maybe remove
print_once = True


def retrieve_stack_pos(object_seen):
    global print_once
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
                print_once = True
                return (token.rot_y, token.dist)

        """
        if we arrive here the anchor cannot be found
        meaning it's hidden behind other tokens
        The best way to address the issue is to go towards
        a token that is already set
        """
        if print_once:
            print(WARN+"The anchor could not be found "
                  "because hidden by other tokens")
            print(WARN+"Proceding towards one token already set")
            print_once = False

        for token in R.see():
            if token.info.code in R.tokens_set:
                return (token.rot_y, token.dist)
    else:
        for token in R.see():
            if token.info.code == object_seen:
                return (token.rot_y, token.dist)

# TODO take into account the position of the object relative to the robot


def object_avoidance(target, target_distance):
    """
    Function that enables the turtle to avoid a token that is
    between the robot and it's target.
    The target can be both the anchor or a token

    Args:
      - target (int): the id of the target token
      - target_distance (float): the distance of the target
    """
    for tokens in R.see():
        if (tokens.info.code != target and
                tokens.info.code != R.currently_held and
                tokens.dist <= target_distance and
                abs(tokens.rot_y) <= R.a_th+30 and
                tokens.dist <= R.d_th + 1):

            # Trying to avoid the token
            turn(30, 0.7)
            drive(50, 1)
            turn(-30, 0.7)

            """
            If by moving the turtle the target dissappeared try to
            search for it
            """
            while (sum(t.info.code == target for t in R.see()) == 0):
                turn(-R.turn_speed, R.turn_interval)
            return True
        return False


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
            if not object_avoidance(target, dist):
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
            turn(100, 1)
            exit(0)


main()

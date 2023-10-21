from __future__ import print_function

import time
from sr.robot import *

R = Robot()

a_th = 2.0

d_th = 0.4
tokens_set = []
currently_held = -1


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
        anchor (int): the numeric code of the marker (-1 if no anchor is found)
    """
    dist = 100
    for token in R.see():
        if token.dist < dist:
            dist = token.dist
            anchor = token.info.code
    if dist == 100:
        return -1
    else:
        return anchor


def initial_orientation(id):
    while 1:
        for token in R.see():
            if token.info.code == id:
                rot = token.rot_y
                print(rot)
                if rot > a_th:
                    turn(5, 0.1)
                elif rot < -a_th:
                    turn(-5, 0.1)
                else:
                    return


def pick_it_up(id):
    initial_orientation(id)
    grabbed = False
    while not grabbed:
        for token in R.see():
            if token.info.code == id:
                rot = token.rot_y
                dist = token.dist

                if rot > a_th:
                    turn(5, 0.1)
                elif rot < -a_th:
                    turn(-5, 0.1)
                if dist >= d_th:
                    drive(50, 0.1)

                print(rot, dist)
                if rot < a_th and dist < d_th:
                    R.grab()
                    global currently_held
                    currently_held = token.info.code
                    grabbed = True
                    break


def release_it():
    close = False
    while not close:
        for token in R.see():
            if token.info.code == anchor:
                rot = token.rot_y
                dist = token.dist

                if rot > a_th:
                    turn(5, 0.1)
                elif rot < -a_th:
                    turn(-5, 0.1)
                if dist >= d_th:
                    drive(50, 0.1)

                print(rot, dist)
                if rot < a_th and dist < d_th+0.3:
                    R.release()
                    global currently_held
                    tokens_set.append(currently_held)
                    currently_held = -1
                    close = True
                    break


def search_new_token():
    while 1:
        turn(10, 0.1)
        for token in R.see():
            code = token.info.code
            if code not in tokens_set and code != anchor:
                pick_it_up(code)
                return


def search_anchor():
    while 1:
        turn(10, 0.1)
        for token in R.see():
            if token.info.code == anchor:
                initial_orientation(anchor)
                release_it()
                return


turn(-10, 1)
anchor = set_anchor()
while 1:
    search_new_token()
    search_anchor()
    drive(-30, 2)


# while 1:
#     search_new_token()
# while 1:
#
#     pass


# Table of Contents

1.  [Research Track Assignment 1](#org8a84310)
    1.  [What does this code do?](#orgb15ac13)
        1.  [Objective](#orgfebffcd)
    2.  [Solution implemented](#org5c61b98)
        1.  [Possible improvements](#org19260d9)
        2.  [Why they have not been implemented](#orgf084057)
    3.  [Pseudocode](#org6534196)
    4.  [Improvements](#org63a695a)



<a id="org8a84310"></a>

# Research Track Assignment 1


<a id="orgb15ac13"></a>

## What does this code do?

The code contained in this repo was written for the first assignment of the
course Research Track 1 of University of Genova.


<a id="orgfebffcd"></a>

### Objective

The objective was to develop a python script able to control the turtle-bot in
such a way that the robot could be able to stack all the golden tokens close to
each other


<a id="org5c61b98"></a>

## Solution implemented

The general idea behind the script is to immediately select an anchor token to
which bring all the other tokens. In the script there is also a logic to face the
edge case when the anchor is not seen by the robot because hidden by other
tokens that have already been set.


<a id="org19260d9"></a>

### Possible improvements

An element which is missing from the script is object avoidance. With this I
mean that if presented with this situation:
![caseBase](./img/caseBase.png?raw=true)
The robot would not be able to see the object in front because no logic for it
was developed. The end result would be:
![caseError](./img/caseError.png?raw=true)
Now it could be said that a simple solution would have been to make the robot
turn $90^{\circ}$ degrees to th
![caseSol](./img/caseSol.png?raw=true)


<a id="orgf084057"></a>

### Why they have not been implemented


<a id="org6534196"></a>

## Pseudocode


<a id="org63a695a"></a>

## Improvements


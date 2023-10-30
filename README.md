
# Table of Contents

1.  [Research Track Assignment 1](#org9af548e)
    1.  [How to run code](#org96ded60)
    2.  [What does this code do?](#org0bcb10e)
        1.  [Objective](#org91fb8d9)
    3.  [Solution implemented](#org70d2e24)
        1.  [Possible improvements](#org33e7206)
        2.  [Why they have not been implemented](#org708196b)
    4.  [Pseudocode](#org4cac8fe)
    5.  [Improvements](#org2b72698)



<a id="org9af548e"></a>

# Research Track Assignment 1


<a id="org96ded60"></a>

## How to run code

To run this code python3 is needed because it was developed starting from the
assignment23<sub>python3</sub> branch of [@CarmineD8](https://github.com/CarmineD8) [python_simulator](https://github.com/CarmineD8/python_simulator/) github repo:
<https://github.com/CarmineD8/python_simulator/tree/assignment23_python3>

    python3 run.py assignment.py


<a id="org0bcb10e"></a>

## What does this code do?

The code contained in this repo was written for the first assignment of the
course Research Track 1 of University of Genova.


<a id="org91fb8d9"></a>

### Objective

The objective was to develop a python script able to control the turtle-bot in
such a way that the robot could be able to stack all the golden tokens close to
each other


<a id="org70d2e24"></a>

## Solution implemented

The general idea behind the script is to immediately select an anchor token to
which bring all the other tokens. In the script there is also a logic to face the
edge case when the anchor is not seen by the robot because hidden by other
tokens that have already been set.


<a id="org33e7206"></a>

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


<a id="org708196b"></a>

### Why they have not been implemented

Now it could be said that a simple solution would have been to make the robot
turn $90^{\circ}$ degrees to the left for example. This would have been only a
partial solution because for example in the following situation the robot would
run into a wall forever finding in front of itself always a extraneous token.
The same goes for implementing a rotation to the right.
![solCase](./img/caseSol.png?raw=true)
No simple solution to this problem with the data available has been found so
instead of producing a partial solution that would have worked only for
particular cases the problem has been ignored seeing that in the proposed
simulation this kind of situation do not occur.


<a id="org4cac8fe"></a>

## Pseudocode
```
    function take_token(id)
        while true do
            drive_towards_token(id);
            if token_close_enough() then
                R.grab()
                return
            end
        end
    end
    
    function go_to_anchor()
        while true do
            drive_towards_anchor()
            if anchor_close_enough() then
                R.grab()
                return
            end
            if anchor_not_visible() then
                go_towards_an_already_set_token()
            end
        end
    end
    
    anchor = set_anchor()
    while True do
        take_token()
        go_to_anchor()
        if finished then
            exit(0)
        end
    end
```

<a id="org2b72698"></a>

## Improvements

A possible improvement would be adding logic for object avoidance


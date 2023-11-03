
# Table of Contents
- [Table of Contents](#table-of-contents)
- [Research Track Assignment 1](#research-track-assignment-1)
  * [How to run code](#how-to-run-code)
  * [What does this code do?](#what-does-this-code-do)
    + [Objective](#objective)
  * [Solution implemented](#solution-implemented)
    + [Possible improvements](#possible-improvements)
    + [Why they have not been implemented](#why-they-have-not-been-implemented)
  * [Pseudocode](#pseudocode)
  * [Improvements](#improvements)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

# Research Track Assignment 1


## How to run code

To run this code python3 is needed because it was developed starting from the
assignment23_python3 branch of [@CarmineD8](https://github.com/CarmineD8) [python_simulator](https://github.com/CarmineD8/python_simulator/) github repo:
<https://github.com/CarmineD8/python_simulator/tree/assignment23_python3>

    python3 run.py assignment.py


## What does this code do?

The code contained in this repo was written for the first assignment of 
Research Track 1 of Robotics Engineering course of University of Genova.
The purpose was to make us familiarize with python3.


### Objective

The objective was to develop a python script able to control the turtle-bot in
such a way that the robot could be able to stack all the golden tokens close to
each other.


## Solution implemented

The general idea behind the script is to immediately select an anchor token to
which bring all the other tokens. In the script there is also a logic to face the
edge case when the anchor is not seen by the robot because hidden by other
tokens that have already been set. 


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

### object_avoidance branch
To prove the point that the solution presented in the previous paragraph would
have it's own drawbacks it has been implemented in the object_avoidance branch.
At a certain point during execution the robot would run into a wall while trying to
avoid other tokens. Different solutions could be to turn the other direction or to 
move the anchor token to the center, but all of these solutions are build for this 
particular case. The idea behind the proposed solution is that it should be the most 
general possible.


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

## Improvements

A possible improvement would be adding some sort of positioning based on 
the tokens present in the board. Another improvement would be to add some 
logic for dealing with the edge case of not beeing able to see the anchor
or neww tokens during the search phase.


# object_avoidance branch
As said in the README in the main branch, this branch has been created to
prove that the solution of moving to the side to try to avoid an object 
in the path of the robot is only a partial solution to the problem
because not having any notion of the position in the arena can cause the robot
to collide with the wall.

This happens in the simulation after the robot has placed the third token.
It tries to avoid the other tokens by avoiding them to the right, but keeps
colliding with the wall. In this case there is no much damage to the structure of the
pile but in other cases the damage could be much worse. It could also
happen that the robot gets stuck in an infinite loop trying to avoid the tokens but keeping 
colliding with the wall. The idea of making the robot avoid the tokens to the left is
suited for this particular case but could fail in others, so the code developed
to this branch has not been merged into the main.

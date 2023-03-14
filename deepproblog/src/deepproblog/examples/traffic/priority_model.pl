% 0 obj is a car turning to the right 
% 1 obj is a car turning to the left
% 2 obj is a car goeing straight
% 3 obj is a crosswalk 
% 4 no object 
nn(right_net,[X],Y, [0, 1, 2, 3,4]) :: obj_right(X, Y).
nn(down_net,[X], Y, [0, 1, 2, 3,4]) :: obj_down( X, Y).
nn(left_net,[X],Y, [0, 1, 2, 3,4]) :: obj_left(X, Y).
nn(up_net,[X], Y, [0, 1, 2, 3,4]) :: obj_up( X, Y).

% 0 there are no priority signs 
% 1 there are priority signs in the horizontal direction so left and right 
% 2 there are priority signs in the vertical direction so up and down
nn(priority_net,[X], Y, [0, 1, 2]) :: priority(X, Y).

p_new(0,0).
p_new(1,2).
p_new(2,1).

% does the object on the left get priority
left(X,Y) :- 
    obj_right(X, R), 
    obj_down( X,D), 
    obj_left(X, L),
    obj_up( X, T), 
    priority(X,P),
    p_new(P,PNEW),
    has_priority(PNEW, L, R, D,  T,Y).

% does the object on the right get priority
right(X,Y) :-     
    obj_right(X, R), 
    obj_down( X,D), 
    obj_left(X, L),
    obj_up( X, T), 
    priority(X,P),
    p_new(P,PNEW),
    has_priority(PNEW, R, L, T,  D,Y).
    
% does the object on the bottem get priority
down(X,Y) :-     
    obj_right(X, R), 
    obj_down( X,D), 
    obj_left(X, L),
    obj_up( X, T), 
    priority(X,P),
    has_priority(P, D, T, R,  L,Y).


% does the object on the top get priority
up(X,Y) :-     
    obj_right(X, R), 
    obj_down( X,D), 
    obj_left(X, L),
    obj_up( X, T), 
    priority(X,P),
    has_priority(P, T, D, L,  R,Y).



has_priority(P, C, O, R, L,1):-
    priority_rules(P, C, O, R, L,1).
    
has_priority(P, C, O, R, L,0):-
    \+priority_rules(P, C, O, R, L,1).



% priority_rules(P, C, O, R, L,Y)
% p = 0 no priority signs on MY direction
% p = 1 priority sign on my direction
% p = 2 triangles or stop sign in my direction

% C currecnt direction object (Left)
% O object on the opposite side of the intersection
% R object on the right side of the intersection
% L object on the left side of the intersection
% Y = 1 object C has priority
% Y = 0 object C has not priority

% crosswalk always has priority
priority_rules(_, 3, _, _, _,1).

% I can go right if:
priority_rules(0, 0, _, _, _,1). %if priority of right, you can always turn right
priority_rules(1, 0, _, _, _,1). %if I have priority
priority_rules(2, 0, _, _, L,1):- %no priority, but left isnt going straight
   L =\= 2.

% I can go straight if:
priority_rules(0, 2, _, 3, _,1).
priority_rules(0, 2, _, 4, _,1).
priority_rules(1, 2, _, _, _,1). %I have priority
priority_rules(2, 2, _, R, L,1):-
   L =\= 2,
   R =\= 2.

% I can go left if:
priority_rules(0, 1, O, R, _,1):-
   O =\= 0,
   O =\= 2,
   R =\= 0,
   R =\= 1,
   R =\= 2.
priority_rules(1, 1, O, _, _,1):- %if I have priority and I dont block the opposite car.
   O =\= 0,
   O =\= 2.
priority_rules(2, 1, O, R, L,1):- %no priority, 
   O =\= 0,
   O =\= 2,
   L =\= 1,
   L =\= 2,
   R =\= 0,
   R =\= 1,
   R =\= 2.
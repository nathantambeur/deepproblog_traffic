%priority_rules(P, C, O, R, L,Y)
%p = 0 no priority signs on MY direction
%p = 1 priority sign on my direction
%p = 2 triangles or stop sign in my direction

%C currecnt direction object (Left)
%O object on the opposite side of the intersection
%R object on the right side of the intersection
%L object on the left side of the intersection
%Y = 1 object C has priority
%Y = 0 object C has not priority


%if the direction im going going has a crosswalk, I dont have priority.
priority_rules(_, 0, _, 3, _, 0).
priority_rules(_, 1, _, _, 3, 0).
priority_rules(_, 2, 3, _, _, 0).

%if there is no object there is never any priority
priority_rules(_, 4, _, _, _, 0).

%crosswalk always has priority
priority_rules(_, 3, _, _, _,1).

%I can go right if:
priority_rules(0, 0, _, _, _,1). %if priority of right, you can always turn right
priority_rules(1, 0, _, _, _,1). %if I have priority
priority_rules(2, 0, _, _, L,1):- %no priority, but left isnt going straight
    L =\= 2.

%I can go straight if:
priority_rules(0, 2, _, 3, _,1).
priority_rules(0, 2, _, 4, _,1).
priority_rules(1, 2, _, _, _,1). %I have priority
priority_rules(2, 2, _, R, L,1):-
    L =\= 2,
    R =\= 2.

%I can go left if:
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

%ELSE you dont have priority:
priority_rules(_,_,_,_,_,0).
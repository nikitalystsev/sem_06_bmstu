domains
    	number = integer.

predicates
    	max(number, number, number, number)
	
clauses
   	max(X, Y, Z, X) :- X > Y, X > Z, !.
    	max(X, Y, Z, Y) :- Y > Z, !.
    	max(X, Y, Z, Z).
goal
	max(7, 11, 5, Max).
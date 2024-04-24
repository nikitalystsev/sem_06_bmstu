domains
    	number = integer.

predicates
    	max(number, number, number, number)
	
clauses
   	max(X, Y, Z, X) :- X > Y, X > Z.
   	max(X, Y, Z, Z) :- Z > X, Z > Y.
    	max(X, Y, Z, Y) :- Y > X, Y > Z.
 
goal
	max(7, 11, 5, Max).
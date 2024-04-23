domains
    	number = integer.

predicates
    	max(number, number, number)
	
clauses
   	max(X, Y, X) :- X >= Y, !.
    	max(X, Y, Y).
goal
	max(4, 3, Max).
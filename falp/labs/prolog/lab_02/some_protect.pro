domains
    	number = integer.

predicates
    	maximum(number, number, number)
	
clauses
   	maximum(X, Y, X) :- X >= Y.
    	maximum(X, Y, Y) :- Y > X.
goal
	maximum(3, 4, Max).
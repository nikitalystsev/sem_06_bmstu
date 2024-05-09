domains 
	number=integer
predicates
	factorial(number, number)
	factoriall(number, number, number)
clauses
	factorial(0, 1) :- !.
	factorial(1, 1) :- !.
	
	factorial(N, R) :- factoriall(N, 1, R).
	
	factoriall(1, A, A) :- !.
	factoriall(N, A, R) :- N1=N-1, NextA=A*N, factoriall(N1, NextA, R).
    
goal
	factorial(-3,R).
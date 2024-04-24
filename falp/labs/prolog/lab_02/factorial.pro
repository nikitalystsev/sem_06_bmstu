domains 
	number=integer
predicates
	factorial(number, number)
	factoriall(number, number, number)
clauses
	factoriall(0, A, A) :- !.
	factoriall(N, A, R) :- N1=N-1, NextA=A*N, factoriall(N1, NextA, R).
    
    	factorial(N, R) :- factoriall(N, 1, R).

goal
	factorial(5,R).
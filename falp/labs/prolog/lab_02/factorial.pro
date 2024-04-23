domains 
	number=integer
predicates
	factorial(number, number)
clauses
	factorial(0, 1) :- !.
	factorial(1, 1) :- !.
	factorial(N, R) :- New_N = N - 1, factorial(New_N, R1), R = N * R1.

goal
	factorial(5,R).
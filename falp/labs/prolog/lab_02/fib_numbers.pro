predicates
	fib(integer,integer)
	fibb(integer,integer,integer,integer)
 
clauses
	fibb(1,C,_,C):- !.
	fibb(N,C,P,F):- N1=N-1,C1=C+P,P1=C,fibb(N1,C1,P1,F).
 
	fib(N,F):-fibb(N,0, 1,F).
goal
	fib(1,R).


	
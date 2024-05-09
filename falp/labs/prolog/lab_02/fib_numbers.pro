predicates
	fib(integer,integer)
	fibb(integer,integer,integer,integer)
 
clauses
	fib(1, 0) :- !.
	fib(2, 1) :- !.
	fib(3, 1) :- !.
	
	fib(N,F):-fibb(N,0, 1,F).
	
	fibb(1,C,_,C):- !.
	fibb(N,C,P,F):- N1=N-1,C1=C+P,fibb(N1,C1,C,F).
 
goal
	fib(5,R).


	
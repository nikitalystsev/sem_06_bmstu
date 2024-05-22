domains
    	ilist = integer*.
    	els = a(integer); l(ilist); s(clist).
    	clist = els*.   
  
predicates
    	max(ilist, integer).
    	proc(clist, clist).    

clauses      
    	max([T], T).
    	max([H|T], ResMax) :- max(T,ResMax), H <= ResMax.
    	max([H|T], H) :- max(T,ResMax), H > ResMax.
    	
    	proc([], []).
   	proc([a(I)|T], [a(I)|R]) :- proc(T, R).
    	proc([l(L)|T], [a(Max)|R]) :- max(L, Max), `proc(T, R).
    	proc([s(C)|T], [s(Stuct)|R]) :- proc(C, Stuct), proc(T, R).
    
 goal
 	proc([a(1), a(2), l([8, 12]), s([a(3), l([12, 13]), s([a(1), l([6, 7])])])], R).


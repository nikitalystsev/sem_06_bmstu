domains
    	list = integer*.

predicates
	len(list, integer)
    	lenn(list, integer, integer)
	
	sum(list, integer)
	summ(list, integer, integer)
	
	sum_odd(list, integer)
	summ_odd(list, integer, integer)
	
	filter_greater_than(list, integer, list)
	
	delete_one(list, integer, list)
	
	delete_all(list, integer, list)
	
	append(list, list, list)
	
clauses
    	lenn([], Len, Len).
    	lenn([_ | T], Cnt, Len) :- Cnt1 = Cnt  + 1, lenn(T, Cnt1, Len).
	len(L, Len) :- lenn(L, 0, Len).
	
	summ([], Sum, Sum).
    	summ([H | T], Curr, Sum) :- Curr1 = Curr + H, summ(T, Curr1, Sum).
	sum(L, Sum) :- summ(L, 0, Sum).
	
	summ_odd([], SumOdd, SumOdd).
	summ_odd([H], Curr, SumOdd) :- SumOdd = Curr + H.
    	summ_odd([H1, _ | T], Curr, SumOdd) :- Curr1 = Curr + H1, summ_odd(T, Curr1, SumOdd).
	sum_odd(L, SumOdd) :- summ_odd(L, 0, SumOdd).
	
	filter_greater_than([], _, []).
	filter_greater_than([H | T], Num, R) :- H <= Num, filter_greater_than(T, Num, R).
	filter_greater_than([H | T1], Num, [H | T2]) :- H > Num, filter_greater_than(T1, Num, T2).
	
	delete_one([], _, []).
  	delete_one([Num | T], Num, T) :- !. 
    	delete_one([H | T], Num, [H | T2]) :- delete_one(T, Num, T2).
    	
    	delete_all([], _, []).
	delete_all([Num | T], Num, R) :- delete_all(T, Num, R), !.
	delete_all([H | T], Num, [H | T1]) :- delete_all(T, Num, T1).
	
    	append([], L, L).
    	append([H1 | T1], L, [H1 | T3]) :- append(T1, L, T3).
    	
goal
    	% len([1, 2, 3, 4], Len).
   	% sum([1, 2, 3, 4], Sum).
   	% sum_odd([17, 1, 13, 2], SumOdd).
   	% filter_greater_than([1, 2, 3, 4], 2, R).
   	% delete_one([1, 2, 3, 3, 4], 3, R).
   	% delete_all([1, 2, 3, 3, 4], 3, R).
   	append([1, 2], [3, 4, 5], R).
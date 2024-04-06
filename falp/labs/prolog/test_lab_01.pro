  ad = address(symbol, symbol, integer, integer).

predicates
  pb(symbol, string, ad).
  at(symbol, symbol, symbol, integer, string).

clauses
  pb(ivanov, "+79037912453", address(moscow, main, 1, 1)).
  pb(sidorov, "+79034567832", address(moscow, main, 1, 2)).
  pb(hotov, "+903821374981", address(spb, main, 3, 4)).
  pb(ivanov, "+1938410194", address(moscow, main, 1, 1)).
  pb(sidorov, "+932841909841099", address(moscow, main, 1, 2)).
  pb(sidorov, "+4919943124", address(moscow, main, 1, 2)).
  
  at(ivanov, honda, white, 8923492, "213949034").
  at(ivanov, hundai, red, 9134802, "92340191").
  at(ivanov, mers, black, 29034810, "93401348901").
  at(sidorov, mers, white, 91034811, "934109483").
  at(sidorov, opel, yellow, 91328401, "039410901").
  
goal
  at(Surname, honda, white, _, _), pb(Surname, X, address(Y, _, _, _)).


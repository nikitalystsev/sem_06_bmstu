domains
	% phonebook
	surname = symbol
	phone = string
	
	% address
	city, street = symbol
	num_house, num_flat = integer
	addr = address(city, street, num_house, num_flat)
	
	% depositors
	bank = symbol
	account, amount = integer.
	
	% property
	area, floors, price = integer
	brand, color = symbol
	number = string
	name = string
	
	property = car(name, brand, color, price, number);
    		   building(name, price, area, floors);
    	 	   site(name, price, area);
                   water_vehicle(name, price, brand, color).
predicates
	phonebook(surname, phone, addr)
	owner(surname, property)
	depositor(surname, bank, account, amount)
	
	properties_by_surname(surname, name)
	
clauses
	phonebook(lystsev, "8(931)402-25-94", address(arkhangelsk, voskresenskaya, 5, 32)).
	phonebook(voloshenko, "8(964)291-56-88", address(mirnyy, galushino, 2, 134)).
	phonebook(sidorov, "8(921)672-17-05", address(arkhangelsk, varavino, 7, 13)).
	phonebook(lystseva, "8(960)003-29-16", address(arkhangelsk, tverskaya, 46, 27)).
	phonebook(lystseva, "8(921)670-75-54", address(arkhangelsk, tverskaya, 46, 27)).
	phonebook(lystseva, "8(921)488-54-89", address(arkhangelsk, tverskaya, 46, 27)).
	phonebook(malyshev, "8(945)567-19-94", address(moscow, tsvetnoy_boulevard, 17, 45)).
	phonebook(frolova, "8(934)396-15-47", address(saintPetersburg, altai, 34, 96)).
	phonebook(shcherbakova, "8(915)711-23-17", address(saint_petersburg, altai, 34, 98)).
	
	depositor(lystsev, sberbank, 34566, 10).
	depositor(lystsev, vtb, 59321, 17).
	depositor(voloshenko, tinkoff, 14468, 56).
	depositor(lystseva, sberbank, 45221, 453).
	depositor(malyshev, pochtabank, 83412, 454).
	depositor(frolova, sberbank, 43545, 67).
	depositor(shcherbakova, sberbank, 76864, 32).
	
	owner(lystsev, car("strange", nissan, black, 3000000, "M704XC790")).
	owner(lystsev, site("farm", 3000000, 3000)).
	owner(lystsev, water_vehicle("jet_ski", 500000, honda, black)).
	
	owner(shcherbakova, car("pinkie", mercedes, ping, 5000000, "P777AA774")).
	owner(shcherbakova, building("equestria", 10000000, 6000, 4)).
	
	owner(frolova, car("D", audi, burgundy, 2500000, "S042GB562")).
	owner(frolova, building("house", 5000000, 234, 2)).
	
	owner(lystseva, car("crossover", mitsubishi, grey, 1500000, "F001VS148")).
	owner(lystseva, site("farm2", 1000000, 150)).
	
	owner(sidorov, car("F", mazda, black, 3500000, "W042BM342")). 
  	owner(sidorov, water_vehicle("cruiser", 150000, yamaha, red)).
  	
 	
	properties_by_surname(Surname, Name) :- owner(Surname, car(Name, _, _, _, _));
						owner(Surname, building(Name, _, _, _));
						owner(Surname, site(Name, _, _));
						owner(Surname, water_vehicle(Name, _, _, _)).
							
 goal
 	properties_by_surname(lystsev, Name).
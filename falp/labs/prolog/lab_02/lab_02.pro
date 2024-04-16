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
	
	property = car(brand, color, price, number);
    		   building(price, area, floors);
    	 	   site(price, area);
                   water_vehicle(price, brand, color).
predicates
	phonebook(surname, phone, addr)
	owner(surname, property)
	depositor(surname, bank, account, amount)
	
	% conjunctive rule
	search_rule(brand, color, surname, city, phone)
	
	
clauses
	phonebook(lystsev, "8(931)402-25-94", address(arkhangelsk, voskresenskaya, 5, 32)).
	phonebook(voloshenko, "8(964)291-56-88", address(mirnyy, galushino, 2, 134)).
	phonebook(sidorov, "8(921)672-17-05", address(arkhangelsk, varavino, 7, 13)).
	phonebook(lystseva, "8(960)003-29-16", address(arkhangelsk, tverskaya, 46, 27)).
	phonebook(lystseva, "8(921)670-75-54", address(arkhangelsk, tverskaya, 46, 27)).
	phonebook(lystseva, "8(921)488-54-89", address(arkhangelsk, tverskaya, 46, 27)).
	phonebook(malyshev, "8(945)567-19-94", address(moscow, tsvetnoyBoulevard, 17, 45)).
	phonebook(frolova, "8(934)396-15-47", address(saintPetersburg, altai, 34, 96)).
	phonebook(shcherbakova, "8(915)711-23-17", address(saint_petersburg, altai, 34, 98)).
	
	depositor(lystsev, sberbank, 34566, 10).
	depositor(lystsev, vtb, 59321, 17).
	depositor(voloshenko, tinkoff, 14468, 56).
	depositor(lystseva, sberbank, 45221, 453).
	depositor(malyshev, pochtabank, 83412, 454).
	depositor(frolova, sberbank, 43545, 67).
	depositor(shcherbakova, sberbank, 76864, 32).
	
	ovner(lystsev, car(nissan, black, 3000000, "M704XC790")).
	ovner(lystsev, site(3000000, 3000)).
	ovner(lystsev, water_vehicle(500000, honda, black)).
	
	ovner(shcherbakova, car(mercedes, ping, 5000000, "P777AA774")).
	ovner(shcherbakova, building(10000000, 6000, 4)).
	
	ovner(frolova, car(audi, burgundy, 2500000, "S042GB562")).
	ovner(frolova, building(5000000, 234, 2)).
	
	ovner(lystseva, car(mitsubishi, grey, 1500000, "F001VS148")).
	ovner(lystseva, site(1000000, 150)).
	
	ovner(sidorov, car(mazda, black, 3500000, "W042BM342")). 
  	ovner(sidorov, water_vehicle(150000, yamaha, red)).
  	
  	search_rule(Brand, Color, Surname, City, Phone) :- phonebook(Surname, Phone, address(City, _, _, _)), car(Surname, Brand, Color, _, _).
 	

 goal
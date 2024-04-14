domains
	% person
	surname = string
	phone = string
	
	% address
	city = string
	street = string
	num_house = integer
	num_flat = integer
	addr = address(city, street, num_house, num_flat)
	
	% car
	brand = string
	color = string
	cost = integer
	number = string
	
	% human
	sex = string
predicates
	person(surname, phone, addr)
	car(surname, brand, color, cost, number)
	
	% conjunctive rule
	search_rule(brand, color, surname, city, phone)
	
	human(surname, sex)
  	family(surname, surname)
  	grandson_car(brand, color, surname, surname, sex)
	
clauses
 	human("Lystsev", "Male").
  	human("Voloshenko", "Male").
  	human("Sidorov", "Male").
  	human("Lystseva", "Female").
  	human("Malyshev", "Male").
  	human("Frolova", "Female").
  	human("Shcherbakova", "Female").
  	
	person("Lystsev", "8(931)402-25-94", address("Arkhangelsk", "Voskresenskaya", 5, 32)).
	person("Voloshenko", "8(964)291-56-88", address("Mirnyy", "Galushino", 2, 134)).
	person("Sidorov", "8(921)672-17-05", address("Arkhangelsk", "Varavino", 7, 13)).
	person("Lystseva", "8(960)003-29-16", address("Arkhangelsk", "Tverskaya", 46, 27)).
	person("Lystseva", "8(921)670-75-54", address("Arkhangelsk", "Tverskaya", 46, 27)).
	person("Lystseva", "8(921)488-54-89", address("Arkhangelsk", "Tverskaya", 46, 27)).
	person("Malyshev", "8(945)567-19-94", address("Moscow", "Tsvetnoy Boulevard", 17, 45)).
	person("Frolova", "8(934)396-15-47", address("SaintPetersburg", "Altai", 34, 96)).
	person("Shcherbakova", "8(915)711-23-17", address("SaintPetersburg", "Altai", 34, 98)).
	
	car("Lystsev", "Nissan", "black", 3000000, "M704XC790").
	car("Lystsev", "Mazda", "blue", 4000000, "H982FN846").   
  	car("Shcherbakova", "mercedes", "ping", 5000000, "P777AA774").   
  	car("Frolova", "audi", "burgundy", 2500000, "S042GB562").   
  	car("Lystseva", "Mitsubishi", "grey", 1500000, "F001VS148"). 
  	car("Sidorov", "Mazda", "black", 3500000, "W042BM342").   
  	car("Lystseva", "Volkswagen", "white", 2400000, "G042VS174"). 
  	
  	search_rule(Brand, Color, Surname, City, Phone) :- person(Surname, Phone, address(City, _, _, _)), car(Surname, Brand, Color, _, _).
 	
 	family("Lystsev", "Lystseva").
  	family("Lystseva", "Shcherbakova").
  	family("Sidorov", "Voloshenko").
  	family("Frolova", "Malyshev").

  	grandson_car(Brand, Color, Grandson, Grandparent, Line) :- car(Grandson, Brand, Color, _, _), family(Grandson, X), 
  								   family(X, Grandparent), human(Grandparent, Line).

 goal
 	% person("Sidorov", _, address("Arkhangelsk", _, _, _)).
 	% person(Surname, _, address("SaintPetersburg", _, _, _)).
 	% car("Lystsev", Brand, _, _, _).
 	% car(Surname, Brand, "burgundy", _, Number).
 	
 	% search_rule("Mazda", "black", Surname, City, Phone).
 	
 	grandson_car(_, "black", _, Grandparent, "Female").
import tkinter.messagebox

def oid_decoder(qr_splitted_content: list[str], fixture_class) -> tuple[list[str], bool]:
	
	eng_level = qr_splitted_content[2]
	option_code = qr_splitted_content[14].upper()
	left_or_right_harness = qr_splitted_content[3]

	file_path = fr'/home/lear/App/modul_lists/modulelist.{eng_level}'
	file_path2 = fr'/home/lear/App/modul_lists/Modulelist.{eng_level}'

	lenght = len(option_code) + 1
	modullist_content = []
	moduls_called = []
	return_to_class = []
	dict = {}
	
	try:
		file = open(file_path, "r").readlines()
	except FileNotFoundError:
		try:
			file = open(file_path2, "r").readlines()
		except FileNotFoundError:
			tkinter.messagebox.showerror("Greska", f"Nije pronadjena modul lista za {eng_level} inz. nivo")
			return 0
			
			
	for line in file:
		if line[0:3] == 'BOF' or line[0:3] == 'EOF':
			pass
		else:
			modullist_content.append(line.strip())

	for line in modullist_content:
		line_content_splited = line.split(";")
		
		if line_content_splited[1] in dict:
			dict[line_content_splited[1]][line_content_splited[2]] = line_content_splited[3]
			
		elif line_content_splited[1] == str(lenght):
			if left_or_right_harness == line_content_splited[0] and line_content_splited[2] == eng_level:
				moduls_called.append(line_content_splited[3])
			else:
				pass
				
		else:
			dict[line_content_splited[1]] ={line_content_splited[2]:line_content_splited[3]}

	for num, string in enumerate(option_code):
		if string != 'X':
			moduls_called.append(dict[str(num+1)][string])

	return_code = True
	
	for fixture in fixture_class:
	
		fixture.set_active_fixture_false()
		for modul in moduls_called:
			if modul in fixture.module and not fixture.active_fixture:
				fixture.active_fixture = True
				fixture.color = "green"
				return_to_class.append(modul)
			elif modul in fixture.module and fixture.active_fixture:
				tkinter.messagebox.showerror("Greska", f"Fikstura: {fixture.name} ne moze istovreme biti pozvana od strane dva modula!")
				return_code = False
			else:
				pass

			
	return return_to_class, return_code

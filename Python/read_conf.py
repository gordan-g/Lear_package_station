import tkinter.messagebox
from classes import Fixture


def check_split_lenght(value: str) -> str:
	return value.strip() if len(value.split(",")) == 3 else "None" == value

def read_config_file() -> list[Fixture] | int:
	fixture_class = []
	file_path = fr'/home/lear/App/conf.txt'
	
	try:
		file = open(file_path, "r")
		file_content = file.readlines()
	except FileNotFoundError:
		tkinter.messagebox.showerror("Greska", "Nije moguce otvoriti 'conf.txt' file na lokaciji: /home/lear/App")
		return 0
		
	lines_content = [check_split_lenght(line) for line in file_content]
	file.close()

	config_read_status = check_config_file_syntax(lines_content)

	if config_read_status == 1:
		for line in lines_content:
			line_splitted_content = line.split(",")
			fixture_class.append(Fixture(line_splitted_content[0], int(line_splitted_content[1]), line_splitted_content[2].split(":")))
		return fixture_class
		
	elif config_read_status == 2:
		return 1
		
	else:
		return 0


def check_config_file_syntax(config_file_content: list) -> int:
	
	if len(config_file_content) == 1:
		if config_file_content[0]:
			return 2
		else:
			tkinter.messagebox.showerror("Greska", "Ukoliko nemate fikstura na pakovanje u konfiguracioni file unesite 'None'")
			return 0
	
	elif len(config_file_content) > 8:
		tkinter.messagebox.showerror("Greska", "Maksimalan broj fikstura je 8!")
		return 0
	
	else:
		for line in config_file_content:

			try: #Dakle unutar liste imamo False, sto znaci lose konfigurisan file
				iterator = line.split(',')
			except AttributeError:
				tkinter.messagebox.showerror("Greska", "Lose konfigurisan conf.txt file!")
				return 0
			
			if not isinstance(int(iterator[1]), int): #Ovde proveravamo da li je kacenje konfigurisano kao broj, ako nije nailazimo na gresku.
				tkinter.messagebox.showerror("Greska", "Kacenje na RPI mora biti brojcana vrednost")
				return 0
			
			elif int(iterator[1]) <2 or int(iterator[1]) > 27: #Ovde se ogranicava to da kacenje samo moze da ide od GPIO 2 do 27!
				tkinter.messagebox.showerror("Greska", "Fikstura se moze konfigursati samo na GPIO 2-27!")
				return 0
			
			elif iterator[2][0] == " ": #Proverava da li naziv modula pocinje sa praznim mestom, odnosno da li je posle zareza stavljen razmak.
				tkinter.messagebox.showerror("Greska", "Posle zareza ne sme da ide razmak!")
				return 0

		return 1
		

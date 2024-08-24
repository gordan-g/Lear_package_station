import tkinter as tk
from math import ceil, floor
from classes import Harness, Fixture

main_entry = None
stage = 0

def test_engine(fixtures: Fixture, harness: Harness, main_gui_entry: tk.Entry) -> None:	
	global main_entry
	test_gui = tk.Toplevel()
	test_gui.title("Testing")
	test_gui.configure(background="#C1CDCD")
	test_gui.attributes('-fullscreen', True)
	test_gui.bind('<Return>', lambda event: run_test(fixtures, harness, test_gui))

	main_entry = main_gui_entry
	lenght = len(fixtures)
	coordinates = define_picture_coordinates(lenght)
	
	for number, fixture in enumerate(fixtures):
		fixture.instantiate_label(test_gui)
		fixture.place_label_on_screen(coordinates[number])

	labela = tk.Label(test_gui, text="Zelenim oznaceni moduli trebaju biti aktivirani!", bg='#C1CDCD', font=("Arial", 40))
	labela.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
	test_gui_button = tk.Button(test_gui, text="Zatvori program", command=test_gui.destroy, width=30, height=3)
	test_gui_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)


def run_test(fixtures: Fixture, harness: Harness, gui: tk.Toplevel) -> None:
	flag = False
	for fixture in fixtures:
		
		if fixture.read_state() != fixture.active_fixture:
			flag = True
			if fixture.color == "#C1CDCD":
				fixture.color = "red"
			else:
				pass
				
		elif fixture.color == "red":
			fixture.color = "#C1CDCD"
			
		else:
			pass
	
	if flag:
		pass
	else:
		gui.destroy()
		empty_test(fixtures, harness)
		
def empty_test(fixtures: Fixture, harness: Harness) -> None:

	empty_test = tk.Toplevel()
	empty_test.title("Empty test")
	empty_test.configure(background="#C1CDCD")
	empty_test.bind('<Return>', lambda event: check_empty())

	for fixture in fixtures:
		fixture.instantiate_label(empty_test)

	def check_empty():
		global stage
		counter = 0
		flag = False
		
		for fixture in fixtures:
			fixture.remove_label_from_screen()
			if fixture.read_state() == True:
				fixture.empty_test_nok = True
				flag = True
				counter +=1
			else:
				pass
					
		if flag:
			coordinates = define_picture_coordinates(counter)
			increment = 0
			for fixture in fixtures:	
				if fixture.empty_test_nok == True:
					fixture.empty_test_nok = False
					fixture.color = "red"
					fixture.place_label_on_screen(coordinates[increment])
					increment +=1

					
		else:
			harness.write_log()
			harness.print_label()
			main_entry.config(state="normal")
			main_entry.delete(0, tk.END)
			empty_test.destroy()
			stage = 0

	empty_labela = tk.Label(empty_test, text="Empty test, press enter to continue!", font=("Arial", 30))
	empty_labela.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
	empty_test.attributes('-fullscreen', True)
	empty_test.after(500, check_empty)
	
def define_picture_coordinates(number: int) -> list[list[int,int]]:

    coordinates = []
    if number > 4:
        rely = 0.35
        relx = 0.2

        for _ in range(4):
            coordinates.append([rely, relx])
            relx = round(relx + 0.2, 1)

        rely = 0.65
        relx = round(0.5 - (number - 4) * 0.1 + 0.1, 1)

        for _ in range(number-4):
            coordinates.append([rely, relx])
            relx = round(relx + 0.2, 1)

    else:
        rely = 0.5
        relx = round(0.5 - number % 8 * 0.1 + 0.1, 1)

        for _ in range(number%8):
            coordinates.append([rely, relx])
            relx = round(relx + 0.2, 1)

    return coordinates


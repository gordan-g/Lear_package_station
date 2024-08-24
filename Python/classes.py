from gpiozero import Button
import datetime
from oid_decoder import oid_decoder
import tkinter as tk
import subprocess

class Fixture:
	def __init__(self, name: str, pin: int, module: list):
		self.name = name 
		self.pin = pin
		self.module = module
		self.active_fixture = False
		self.button = Button(self.pin)
		self._color = "#C1CDCD"
		self.empty_test_nok = False
		self.first_time_instantiated = True
	
	@property
	def color(self):
		return self._color
		
	@color.setter
	def color(self, colour):
		if colour == "green":
			self._color = colour
		else:
			self._color = colour
			self.labela.config(bg = colour)
	
	def read_state(self) -> bool:
		 return self.button.is_pressed
		 
	def instantiate_label(self, root) -> None:
		
		try:
			self.imgobj = tk.PhotoImage(file=fr'/home/lear/App/Picture/{self.name.replace("/", "_")}.png')
		except Exception:
			self.imgobj = tk.PhotoImage(file=fr'/home/lear/App/Picture/no_image.png')
			
		self.labela = tk.Label(root, image=self.imgobj, text=self.name, compound="top", background=self.color, font=('Arial 24'))
		
	def place_label_on_screen(self, coordinates: list[int, int]) -> None:
		self.labela.place(relx=coordinates[1], rely=coordinates[0], anchor=tk.CENTER)
		
	def remove_label_from_screen(self) -> None:
		self.labela.place_forget()
		
	def set_active_fixture_false(self) -> None:
		self.active_fixture = False
	
class Harness:
	
	def __init__(self, fyon: str, working_order:str, option_code: str, modules_called: list[str] = "None", testable: bool = True):
		self.fyon = fyon
		self.working_order = working_order
		self.option_code = option_code
		self.modules_called = modules_called
		self.testable = testable
	
	@classmethod
	def instantiate_class(cls, qr_splitted_content: list[str], fixture_class: list[Fixture]):
		modules_called, return_code = oid_decoder(qr_splitted_content, fixture_class)
		return cls(qr_splitted_content[4], qr_splitted_content[1], qr_splitted_content[14], modules_called, return_code)
		
	def write_log(self) -> None:
		
		path = "/home/lear/App/Logs/{}".format(self.fyon)
			
		label ="""
Working order: {}
Vreme zavrsenog testiranja: {}
Fyon: {}
Pozvani moduli: {}
		""".format(self.working_order, datetime.datetime.now(), self.fyon, self.modules_called)
		
		file = open(path, 'w')
		file.write(label)
		file.close()

	def print_label(self) -> None:

		label ="""
N
A715,325,2,5,1,1,N,"PACKAGING STATION"
b330,60,Q,m2,"PACK@{}@{}@!{}"
P1
		""".format(self.fyon, self.option_code, self.working_order)
		
		file = open("/home/lear/App/labela", 'w')
		file.write(label)
		file.close()
		subprocess.run(["lp", "/home/lear/App/labela"])


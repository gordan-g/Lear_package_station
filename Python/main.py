import tkinter as tk
import tkinter.messagebox
import read_conf
import testing
from classes import Harness

fixture_class = None
harness_class = None
sheet = None
error_occured = False

def check_labels() -> None:
	global sheet, harness_class, error_occured

	if testing.stage == 0 and not error_occured:
		
		if len(sheet := oid_input.get().split("@")) == 16 and sheet[0] == 'LJS':
			oid_input.delete(0, tk.END)
			input_labela.config(text="Skeniraj elektro nalepnicu")
			testing.stage += 1
			
		else:
			tkinter.messagebox.showinfo("Error", "Skenirani OID nije u dobrom formatu!")
			oid_input.delete(0, tk.END)
			
	elif testing.stage == 1 and fixture_class == "NO FIXTURE":
		electro_label = oid_input.get().split('@')

		if electro_label[2] == sheet[4]:
			testing.stage = 2
			oid_input.delete(0, tk.END)
			input_labela.config(text="Skeniraj OID sheet")
			harness_class = Harness(fyon = sheet[4], working_order = sheet[1], option_code = sheet[14])
			harness_class.write_log()
			harness_class.print_label()
			testing.stage = 0
			
		else:
			tkinter.messagebox.showerror("Greska", "Sheet i elektro nalepnica se ne poklapaju")
			oid_input.delete(0, tk.END)
			
	elif testing.stage == 1:
		electro_label = oid_input.get().split('@')
		
		if electro_label[2] == sheet[4]:
			testing.stage = 2
			input_labela.config(text="Skeniraj OID sheet")
			oid_input.config(state="disabled")
			harness_class = Harness.instantiate_class(sheet, fixture_class)
			
			if harness_class.testable:
				testing.test_engine(fixture_class, harness_class, oid_input)
			else:
				input_labela.config(text="Skeniraj elektro nalepnicu")
				oid_input.config(state="normal")
				oid_input.delete(0, tk.END)
				error_occured = True
			
		else:
			tkinter.messagebox.showerror("Greska", "Sheet i elektro nalepnica se ne poklapaju")
			oid_input.delete(0, tk.END)
			
	elif error_occured:
		oid_input.delete(0, tk.END)
		tkinter.messagebox.showerror("Greska", "Zatvoriti program i rekonfigurisati config file!")
		
	else:
		pass

package = tk.Tk()
package.title("Package")
package.configure(background="#C1CDCD")
package.bind('<Return>', lambda event: check_labels())

def run_configuration_file() -> None:
	global fixture_class, error_occured
	
	return_value = read_conf.read_config_file()
	
	if return_value != 0:
		fixture_class = "NO FIXTURE" if return_value == 1 else return_value
	else:
		error_occured = True

input_labela = tk.Label(package, text="Skeniraj OID sheet", font=("Arial", 24))
input_labela.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

oid_input = tk.Entry(package, width=100, font=('Arial 24'))
oid_input.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
oid_input.focus_set()

close_button = tk.Button(package, text="Zatvori program", command=lambda: package.destroy(), width=30, height=3)
close_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

package.attributes('-fullscreen', True)
package.after(300, run_configuration_file)
package.mainloop()

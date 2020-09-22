from tkinter import *
from PIL import ImageTk,Image
import sqlite3

root = Tk()
root.title("Create new windows")
root.iconbitmap(r"Assets\idea_head.ico")

'''
# create table
cur.execute(""" CREATE TABLE addresses(
	first_name text,
	last_name text,
	address text,
	city text,
	state text,
	zipcode integer)
	""")'''

# create a function to edit a record
def save():

	# create a database or connect to one
	conn = sqlite3.connect('address_bool.db')
	cur = conn.cursor()

	# insert into table
	cur.execute("""UPDATE addresses SET 
		first_name = :first,
		last_name = :last,
		address = :address,
		city = :city,
		state = :state,
		zipcode = :zipcode

		WHERE oid = :oid """,
				{
					"first":first_name_editor.get(),
					"last":last_name_editor.get(),
					"address":address_editor.get(),
					"city":city_editor.get(),
					"state":state_editor.get(),
					"zipcode":zipcode_editor.get(),
					"oid":delete_entry.get()

				})

	# commit changes
	conn.commit()
	# clsoe connection
	conn.close()
	# close the window
	editor.destroy()

def edit():
	global editor
	editor = Tk()
	editor.title("Create new windows")
	editor.iconbitmap(r"Assets\idea_head.ico")


	#create global boxes
	global first_name_editor
	global last_name_editor
	global address_editor
	global city_editor
	global state_editor
	global zipcode_editor

	# create boxex
	
	first_name_editor = Entry(editor, width=30)
	first_name_editor.grid(row=0, column=1, padx=20,pady=(10,0))
	last_name_editor = Entry(editor, width=30)
	last_name_editor.grid(row=1, column=1, padx=20)
	address_editor = Entry(editor, width=30)
	address_editor.grid(row=2, column=1, padx=20)
	city_editor = Entry(editor, width=30)
	city_editor.grid(row=3, column=1, padx=20)
	state_editor = Entry(editor, width=30)
	state_editor.grid(row=4, column=1, padx=20)
	zipcode_editor = Entry(editor, width=30)
	zipcode_editor.grid(row=5, column=1, padx=20)

	# create text box label
	first_name_label = Label(editor, text="Enter first name")
	first_name_label.grid(row=0, column=0,pady=(10,0))
	last_name_label = Label(editor, text="Enter last name")
	last_name_label.grid(row=1, column=0)
	address_label = Label(editor, text="Enter address")
	address_label.grid(row=2, column=0)
	city_label = Label(editor, text="Enter city")
	city_label.grid(row=3, column=0)
	state_label = Label(editor, text="Enter state")
	state_label.grid(row=4, column=0)
	zipcode_label = Label(editor, text="Enter zipcode")
	zipcode_label.grid(row=5, column=0)

	# save edited record
	save_button = Button(editor, text="Save record", command=save)
	save_button.grid(row=6, column=0, columnspan=2, pady=(2,5), padx=10, ipadx=80)

	# create a database or connect to one
	conn = sqlite3.connect('address_bool.db')
	cur = conn.cursor()

	selected_record = delete_entry.get()
	cur.execute("SELECT * FROM addresses WHERE oid = " + selected_record)
	records = cur.fetchall()

	# loop through results
	for record in records:
		first_name_editor.insert(0, record[0])
		last_name_editor.insert(1, record[1])
		address_editor.insert(2, record[2])
		city_editor.insert(3, record[3])
		state_editor.insert(4, record[4])
		zipcode_editor.insert(5, record[5])

	# commit changes
	conn.commit()
	# clsoe connection
	conn.close()

# Create a function to delete a record
def delete():
	
	# create a database or connect to one
	conn = sqlite3.connect('address_bool.db')
	cur = conn.cursor()

	cur.execute("DELETE from addresses WHERE oid= " + delete_entry.get())

	# commit changes
	conn.commit()
	# clsoe connection
	conn.close()


def submit():
	# create a database or connect to one
	conn = sqlite3.connect('address_bool.db')
	cur = conn.cursor()

	# insert into table
	cur.execute("INSERT INTO addresses VALUES (:first_name,:last_name,:address,:city,:state,:zipcode)",
				{
					"first_name":first_name.get(),
					"last_name":last_name.get(),
					"address":address.get(),
					"city":city.get(),
					"state":state.get(),
					"zipcode":zipcode.get()
				})

	# commit changes
	conn.commit()
	# clsoe connection
	conn.close()

	# clear the entries
	first_name.delete(0, END)
	last_name.delete(0, END)
	address.delete(0, END)
	city.delete(0, END)
	state.delete(0, END)
	zipcode.delete(0, END)

def query():
	# create a database or connect to one
	conn = sqlite3.connect('address_bool.db')
	cur = conn.cursor()

	# query the database
	cur.execute("SELECT *, oid FROM addresses")
	# fetchall fetches all the records
	# fetchone fetches top record
	# fetchone(50) fetches first 50 records
	records = [str(x)+"\n" for x in cur.fetchall()]

	print_label = Label(root, text=" ".join(records))
	print_label.grid(row = 8, column=0, columnspan=2)

	# commit changes
	conn.commit()
	# clsoe connection
	conn.close()
	pass

# create boxex
first_name = Entry(root, width=30)
first_name.grid(row=0, column=1, padx=20,pady=(10,0))
last_name = Entry(root, width=30)
last_name.grid(row=1, column=1, padx=20)
address = Entry(root, width=30)
address.grid(row=2, column=1, padx=20)
city = Entry(root, width=30)
city.grid(row=3, column=1, padx=20)
state = Entry(root, width=30)
state.grid(row=4, column=1, padx=20)
zipcode = Entry(root, width=30)
zipcode.grid(row=5, column=1, padx=20)
delete_entry = Entry(root, width=30)
delete_entry.grid(row=9,column=1)

# create text box label
first_name_label = Label(root, text="Enter first name")
first_name_label.grid(row=0, column=0,pady=(10,0))
last_name_label = Label(root, text="Enter last name")
last_name_label.grid(row=1, column=0)
address_label = Label(root, text="Enter address")
address_label.grid(row=2, column=0)
city_label = Label(root, text="Enter city")
city_label.grid(row=3, column=0)
state_label = Label(root, text="Enter state")
state_label.grid(row=4, column=0)
zipcode_label = Label(root, text="Enter zipcode")
zipcode_label.grid(row=5, column=0)
Delete_record = Label(root, text="Select a record")
Delete_record.grid(row=8, column=0, columnspan=2, pady=(10,5))
delete_label = Label(root, text="select a record")
delete_label.grid(row=9, column=0)

# create submit button
submit_button = Button(root, text="Submit", command=submit)
submit_button.grid(row=6,column=0,columnspan=2,pady=(10,3),padx=10,ipadx=100)

# Create quary button
query_button = Button(root, text="show records", command=query)
query_button.grid(row=7, column=0, columnspan=2, pady=(3,5), padx=10, ipadx=85)

# create a delete button
delete_button = Button(root, text="delete record", command=delete)
delete_button.grid(row=10, column=0, columnspan=2, pady=(5,2), padx=10, ipadx=83)

# create an update button
edit_button = Button(root, text="update record", command=edit)
edit_button.grid(row=11, column=0, columnspan=2, pady=(2,5), padx=10, ipadx=80)

root.mainloop()
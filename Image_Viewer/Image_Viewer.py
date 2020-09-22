from PIL import ImageTk
from tkinter import filedialog
from tkinter import *
import PIL
import os

# Create root window
root = Tk()
root.title("Image Viewer")

# get current working directiory 
initial_dir = os.getcwd()

# resizing while keeping aspect ratio
def resize(temp_image):
	temp_image = PIL.Image.open(temp_image)
	width, height = temp_image.size
	if width>1100:
		new_height = int((1100/width)*height)
		temp_image = temp_image.resize((1100,new_height))
		width, height = temp_image.size
	if height>1000:
		new_width = int((1000/height)*width)
		temp_image = temp_image.resize((new_width,1000))
	return temp_image

# Function "Flow" which dictates the forward and backward buttons
def Flow(image_number):
	global Image_window
	global image_label
	global button_forward
	global button_back
	global temp_image

	# remove image from my_label 
	image_label.place_forget()

	# load the next image and put it on label widget
	temp_image = ImageTk.PhotoImage(resize(Images_dir[image_number-1]))
	width, height = temp_image.width(), temp_image.height()
	image_label = Label(Image_window, image=temp_image)

	# update the buttons with next and previous image
	button_forward = Button(Image_window, text=">>", bg="black", fg="white",
		width=10, height=10, relief=FLAT, command=lambda: Flow(image_number+1))
	button_back = Button(Image_window, text="<<", bg="black", fg="white",
		width=10, height=10, relief=FLAT, command=lambda: Flow(image_number-1))

	# make the respective buttons disabled at last and first iamge
	if image_number==len(Images_dir):
		button_forward = Button(Image_window, text=">>", bg="black", fg="white",
			width=10, height=10, relief=FLAT, state=DISABLED)
	if image_number==1:
		button_back = Button(Image_window, text="<<", bg="black", fg="white",
			width=10, height=10, relief=FLAT, state=DISABLED)

	# Place the widgets on the window
	image_label.place(x=640-(width//2), y=500-(height//2))
	button_back.place(x=0, y=432)
	button_forward.place(x=1200, y=432)

# function for selecting directory and updating displayed one
def browse_dir():
	global directory_show
	directory = directory_show.get()
	directory = filedialog.askdirectory(initialdir=directory).replace("/", "\\")
	directory_show.delete(0, END)
	directory_show.insert(0, directory)
	
# fucniton for button "View images" open a new window 
# and displays images in the new window
def show_images():
	# setting widget variables as global
	global Image_window
	global image_label
	global button_forward
	global button_back
	global Images_dir
	global temp_image

	# get current directory from directory_show Entry widget 
	# and filter all non - image files from the directory
	# we can any other image format later by here
	# also encoding is done to deal with images with special 
	# charecters in its name absolute directories of all images 
	# are stored in a list "Image_dir"
	directory = directory_show.get()
	files = os.listdir(directory)
	files = [x for x in files if any([x.encode("utf-8").endswith(b".jpeg"), 
			x.encode("utf-8").endswith(b".png"),
			x.encode("utf-8").endswith(b".jpg"),
			x.encode("utf-8").endswith(b".JPG"),
			])]
	Images_dir = [os.path.join(directory,x) for x in files]

	# Create a second window for displaying images
	Image_window = Toplevel()
	Image_window.title("image Viewer")
	Image_window.geometry("1280x1024")
	Image_window.config(bg="black")

	# load first image and resize the image if it is greater than 1100,1000
	# read image and place it at exactly the center of the screen
	temp_image = ImageTk.PhotoImage(resize(Images_dir[0]))
	width, height = temp_image.width(), temp_image.height()
	image_label = Label(Image_window, image=temp_image)
	image_label.place(x=640-(width//2), y=500-(height//2))

	# create button widgets
	button_back = Button(Image_window, text="<<", bg="black", fg="white",
		width=10, height=10, relief=FLAT, state=DISABLED)
	button_forward = Button(Image_window, text=">>", bg="black", fg="white",
		width=10, height=10, relief=FLAT, command=lambda: Flow(2))

	# place those buttons
	button_back.place(x=0, y=432)
	button_forward.place(x=1200, y=432)


# Some Widgets on the main Window
instruct = Label(root, text="select directory to view images", font = ('calibri', 14, 'bold'))
directory_show = Entry(width = 70, borderwidth=5)
directory_show.insert(0, initial_dir)
browse_button = Button(root, text="Browse", width=10, command=browse_dir)
button = Button(root, text="View images", width=50, height = 2,
			 relief=GROOVE , font = ('calibri', 14, 'bold'),command=show_images)

# Put widgets on screen
instruct.grid(row=0, column=0, columnspan=2, pady=(10, 5))
directory_show.grid(row=1, column=0, pady=(5, 10), sticky=W)
browse_button.grid(row=1, column=1, pady=(5, 10))
button.grid(row=2, column=0,columnspan=2)

root.mainloop()

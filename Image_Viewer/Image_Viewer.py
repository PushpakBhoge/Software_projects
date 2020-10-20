from PIL import ImageTk 
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import PIL
import os

# Create root window
root = Tk()
root.title("Image Viewer")

# get current working directiory 
initial_dir = os.getcwd()

# resizing while keeping aspect ratio
def resize(temp_image, percentile = 0.9):
	global Scr_width
	global Scr_height

	hor_scale = int(Scr_width*percentile)
	ver_scale = int(Scr_height*percentile)

	temp_image = PIL.Image.open(temp_image)
	width, height = temp_image.size
	if width>hor_scale:
		new_height = int((hor_scale/width)*height)
		temp_image = temp_image.resize((hor_scale,new_height))
		width, height = temp_image.size
	if height>ver_scale:
		new_width = int((ver_scale/height)*width)
		temp_image = temp_image.resize((new_width,ver_scale))
	return temp_image

# Function "Flow" which dictates the forward and backward buttons
def Flow(image_number):
	global Image_window
	global image_label
	global temp_image
	global Images_dir
	global files

	# remove image from my_label 
	image_label.place_forget()

	# load the next image and put it on label widget
	temp_image = ImageTk.PhotoImage(resize(Images_dir[image_number-1]))
	width, height = temp_image.width(), temp_image.height()
	image_label = Label(Image_window, image=temp_image)	

	# Place the widgets on the window
	image_label.place(x=(Scr_width//2)-(width//2), y=(Scr_height//2)-(height//2))

	# update image name over title
	Image_window.title(files[image_number-1])

	# update the buttons with next and previous image
	button_back = Button(Image_window, text="<<", bg="black", fg="white",
		width=10, height=10, relief=FLAT, command=lambda: Flow(image_number-1))
	button_forward = Button(Image_window, text=">>", bg="black", fg="white",
		width=10, height=10, relief=FLAT, command=lambda: Flow(image_number+1))

	# make the respective buttons disabled at last and first iamge
	if image_number==len(Images_dir):
		button_forward.config(state = DISABLED)
	if image_number==1:
		button_back.config(state = DISABLED)

	button_back.place(x=0, y=(Scr_height//2)-80)
	button_forward.place(x=Scr_width-80, y=(Scr_height//2)-80)

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
	global files
	global Images_dir

	# get current directory from directory_show Entry widget 
	# and filter all non - image files from the directory
	# we can any other image format later by here
	# also encoding is done to deal with images with special 
	# charecters in its name absolute directories of all images 
	# are stored in a list "Image_dir"
	directory = directory_show.get()

	# Check if the directory is valid if not
	# Show alert message
	try:
		files = os.listdir(directory)
	except:
		messagebox.showinfo("Alert", "Invalid directory")
		return None


	files = [x for x in files if any([x.encode("utf-8").endswith(b".jpeg"), 
			x.encode("utf-8").endswith(b".png"),
			x.encode("utf-8").endswith(b".jpg"),
			x.encode("utf-8").endswith(b".JPG"),
			])]
	Images_dir = [os.path.join(directory,x) for x in files]
	
	# handling No images indirectory case
	if len(Images_dir)<1:
		messagebox.showinfo("Alert","No images found in this directory")
		return None

	# Get current Screen resolution
	# 10 % of the screen height is excluded to accomodate Start menu
	global Scr_width
	global Scr_height
	Scr_width = root.winfo_screenwidth()
	Scr_height = int(root.winfo_screenheight()*0.9)

	# Create a second window for displaying images
	Image_window = Toplevel()
	Image_window.geometry("{}x{}".format(Scr_width,Scr_height))
	Image_window.config(bg="black")

	# Create image place holder for putting images and 
	# inititat flow of images
	image_label = Label(Image_window)
	Flow(1)


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

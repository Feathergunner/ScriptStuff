import Tkinter as tk
from Tkinter import *
from PIL import Image, ImageTk
import os

def load_tk_image():
	img = Image.open("lenna.jpg")
	img_tk = ImageTk.PhotoImage(img)
	return img_tk

def get_screenshot():
	os.system("import -window root screen_capture.png")
	img = Image.open("screen_capture.png")
	#img_tk = ImageTk.PhotoImage(img)
	return img

class Application(tk.Frame):
	def __init__(self, master=None):		
		self.tk = Tk()
		self.frame = Frame(self.tk, width=200, height=100)
		
		#self.img_tk = load_tk_image()
		self.img = get_screenshot()
		self.img_tk = ImageTk.PhotoImage(self.img)
		self.panel = Label(self.frame, image = self.img_tk)
		
		self.state = False
		self.tk.bind("<F11>", self.toggle_fullscreen)
		self.toggle_fullscreen()
	
	def toggle_fullscreen(self, event=None):
		self.state = not self.state
		self.tk.attributes("-fullscreen", self.state)
		
		if self.state:
			self.panel.pack()
			self.frame.pack()
		else:
			self.panel.pack_forget()
			self.frame = Frame(self.tk)
			self.frame.pack()
			
		return "break"
	
app = Application()
app.mainloop()

#size = app.img.size
#r,g,b = app.img.split()

#print size
#print list(r.getdata())
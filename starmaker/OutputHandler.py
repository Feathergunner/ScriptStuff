import matplotlib.pyplot as plt
import matplotlib.collections as clt
from matplotlib.colors import colorConverter
from datetime import date, timedelta
import json

import os.path

class OutputHandler:
	dirname = 'defaultdir'
	filename = 'defaultfile'
	filepath = ''
	background = 'white'
	dpi_val = 100.0
	dim_x = 3000
	dim_y = 3000

	dimensions = [-100,100,-100,100]

	is_initialized = False
	file_is_initialized = False
	is_plotted = False

	def set_dpi(self, dpi):
		self.dpi_val = dpi

	def set_img_size(self,x,y):
		self.dim_x = x
		self.dim_y = y

	def set_dimensions(self,dim):
		self.dimensions = dim

	def set_background(self, bgcolor):
		self.background = bgcolor

	def init_outputfile(self, name):
		self.dirname = "stars_" + date.isoformat(date.today())
		if not os.path.exists(self.dirname):
			os.makedirs(self.dirname+"/")

		self.filename = name
		self.filepath = self.dirname+"/"+self.filename+".png"

		while os.path.isfile(self.filepath):
			self.filename +="_"
			self.filepath = self.dirname+"/"+self.filename+".png"

		self.file_is_initialized = True

	def init_output(self):
		self.fig = plt.figure(facecolor=self.background)
		plt.axis('off')
		self.ax = self.fig.gca()
		self.ax.set_autoscale_on(False)
		self.ax.set_aspect('equal')

		self.is_initialized = True

	def plt_collection(self, collection, plot_every_frame=False, frame_number=0):
		if self.is_initialized:
			self.ax.add_collection(collection)
			self.ax.plot()
			self.ax.axis(self.dimensions)

			self.is_plotted = True

			if (plot_every_frame):
				orig_name = self.filename
				name_ending = str(frame_number).zfill(8)
				new_name = orig_name + "-" + name_ending
				self.init_outputfile(new_name)
				self.save_to_file(True)
				self.init_outputfile(orig_name)
				self.file_is_initialized = False

	def save_to_file(self, keep_plt=False):
		print ("save plt to file...")
		if self.is_initialized and self.file_is_initialized and self.is_plotted:
			self.fig.set_size_inches(self.dim_x/self.dpi_val, self.dim_y/self.dpi_val)

			plt.savefig(self.filepath, dpi=self.dpi_val, facecolor=self.background)
			if (not keep_plt):
				plt.close()

	def show_plot(self):
		if self.is_initialized and self.is_plotted:
			plt.show()
			plt.close()

	def save_line_data(self, lines, linecolors, linethicknesses, index):
		db_filename = self.dirname+"/"+"db_"+self.filename+"_"+str(int(index))
		with open(db_filename, 'w') as outfile:
			json.dump([lines, linecolors, linethicknesses], outfile)

	def plt_collections_from_files(self, number_of_files, plot_every_frame=False):
		print ("plt_collections_from_files")
		frame_number = 1
		for i in range(1,int(number_of_files+1)):
			db_filename = self.dirname+"/"+"db_"+self.filename+"_"+str(i)
			if os.path.isfile(db_filename):
				with open(db_filename) as dbfile:
					data = json.load(dbfile)
					segments = clt.LineCollection(data[0], colors=data[1], linewidths=data[2], antialiaseds=0)
					if (plot_every_frame):
						self.set_img_size(500,500)
						self.plt_collection(segments, True, frame_number)
						frame_number += 1
					else:
						self.plt_collection(segments)
				os.remove(db_filename)

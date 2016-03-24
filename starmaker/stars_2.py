import matplotlib.pyplot as plt
import matplotlib.collections as clt
from matplotlib.colors import colorConverter
import math
import os.path
import numpy as np
from datetime import date, timedelta
import random
import re
import json

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

	def plt_collection(self, collection):
		if self.is_initialized:
			self.ax.add_collection(collection)
			self.ax.plot()
			self.ax.axis(self.dimensions)

			self.is_plotted = True

	def save_to_file(self):
		if self.is_initialized and self.file_is_initialized and self.is_plotted:
			self.fig.set_size_inches(self.dim_x/self.dpi_val, self.dim_y/self.dpi_val)

			plt.savefig(self.filepath, dpi=self.dpi_val, facecolor=self.background)
			plt.close()

	def show_plot(self):
		if self.is_initialized and self.is_plotted:
			plt.show()
			plt.close()

	def save_line_data(self, lines, linecolors, linethicknesses, index):
		db_filename = self.dirname+"/"+"db_"+self.filename+"_"+str(index)
		with open(db_filename, 'w') as outfile:
			json.dump([lines, linecolors, linethicknesses], outfile)

	def plt_collections_from_files(self, number_of_files):
		for i in range(1,number_of_files+1):
			db_filename = self.dirname+"/"+"db_"+self.filename+"_"+str(i)
			if os.path.isfile(db_filename):
				with open(db_filename) as dbfile:
					data = json.load(dbfile)
					segments = clt.LineCollection(data[0], colors=data[1], linewidths=data[2], antialiaseds=0)
					self.plt_collection(segments)
				os.remove(db_filename)

def parse_list(textarray):
	content = re.split(r'[\[\]]',textarray)
	if len(content) < 3:
		print 'Error! Wrong format in init file: '+textarray
		print 'Note: should be a list ['+textarray+']'
		return
	
	values = re.split(r'\s*,\s*',content[1])
	if len(values) == 1 and len(values[0]) == 0:
		return [0.0]
	else:
		return [float(v) for v in values]

def parse_bool(textbool):
	if textbool == 'True' or textbool == 'true' or textbool == '1':
		return True
	else:
		return False

def load_init(filename):
	initfile = open(filename)
	init={}

	options1 = [
		'raynumber',
		'raylength',
		'raywidth'
	]
	options2_float = [
		'start',
		'vlocal'
	]
	options2_list = [
		'vglobal',
		'vray'
	]

	options_color = [
		'r',
		'g',
		'b',
		'a'
	]

	identifieres_single_float = [
		'iterations',
		'out_dim_x',
		'out_dim_y'
	]

	identifieres_bool = [
		'centerstar',
		'savetofile',
		'color_normalize'
	]

	bg_colors = [
		'black',
		'white'
	]

	for line in initfile:
		if line[0] != '#' and len(line) > 1:
			terms = re.split(r'\s*=\s*',line)
			value = re.split(r'\s*',terms[1])[0]

			if terms[0] in identifieres_single_float:
				init[terms[0]] = float(value)

			if terms[0] == 'background':
				if value in bg_colors:
					init[terms[0]] = value
				else:
					print "Error: unidentified background color: "+value

			if terms[0] in identifieres_bool:
				init[terms[0]] = parse_bool(value)
			else:
				ident = re.split(r'_',terms[0])
				#print ident

				if ident[0] in options1:
					if ident[1] in options2_float:
						init[terms[0]] = float(value)
					elif ident[1] in options2_list:
						init[terms[0]] = parse_list(terms[1])
				elif ident[0] == 'color':
					if ident[1] in options_color:
						if ident[2] in options2_float:
							init[terms[0]] = float(value)
						elif ident[2] in options2_list:
							init[terms[0]] = parse_list(terms[1])

	return init

def get_noized_color(color, maxdelta, mindelta=0.0):
	for i in range(0,3):
		color[i] = get_noized_color_val(color[i], maxdelta, mindelta)
	return color

def get_noized_color_value(oldval, variation_bound, mindelta=0.0, delta_expectation=0.0):
	return norm_value(get_noized_value(oldval, variation_bound, mindelta, delta_expectation))

def get_noized_value(oldval, variation_bound, mindelta=0.0, delta_expectation=0.0):
	variation = np.random.uniform(mindelta, variation_bound)
	if random.randrange(0,10) > 5:
		variation *= -1
	return oldval + variation + delta_expectation

def norm_color(r,g,b):
	u = max(r,g,b)*2.0
	l = min(r,g,b)/2.0
	if l<0:
		l=0
	d = u-l
	if d != 0:
		r_new = (r-l)/d
		g_new = (g-l)/d
		b_new = (b-l)/d
	else:
		r_new = r
		g_new = g
		b_new = b
	if r_new>1:
		r_new = 1
	if g_new>1:
		g_new = 1
	if b_new>1:
		b_new = 1
	return [r_new, g_new, b_new]

# cut value to [0,1]
def norm_value(value, bound_l=0.0, bound_u=1.0):
	if value < bound_l:
		return bound_l
	elif value > bound_u:
		return bound_u
	return value

def get_new_color_value(oldval, vglobal, depth, vray, raynumber, vlocal, mindelta=0.0):
	global_variation = vglobal[depth%len(vglobal)]
	ray_variation = vray[raynumber%len(vray)]
	random_variation = np.random.uniform(mindelta, vlocal)
	if random.randrange(0,10) > 5:
		random_variation *= -1
	return norm_value(oldval + global_variation + ray_variation + random_variation)

def write_linecollection_to_file(filename, collection, dimensions, background='white', dim_x = 3000, dim_y = 3000):
	oh = OutputHandler()

	oh.init_output()
	oh.init_outputfile(filename)
	oh.set_background(background)

	oh.plt_collection(collection)

	oh.set_img_size(dim_x, dim_y)
	oh.set_dimensions(dimensions)
	oh.save_to_file()

def print_linecollection(collection, dimensions, background='white'):
	oh = OutputHandler()

	oh.set_background(background)
	oh.init_output()
	oh.plt_collection(collection)
	oh.set_dimensions(dimensions)
	oh.show_plot()

def create_starname(init_dict):
	#TO DO
	starname = 'default'

	return starname

###################################################################
# A function that creates star as specified by the init_dict
###################################################################
# startlength: 		inital length of rays
# lengthfactor:		factor by which length of rays is shortenend in each iteration

# startrays:		initial number of rays
# rayvariation:		variation in number of rays per iteration

# startwidth: 		initial width of rays
# widthvariation:	variation in width of rays per iteration

# col_start:		[r,g,b,a]: initial color of rays
# col_var_bound:	bounds to random variation of colorvariation per iteration

# safe:			if True, star is saved as image
# middlestar:		if True, each iteration also draws a star at each startpoint
#def printstar_nonrek_colorvariation(startlength, lengthfactor, startrays, rayvariation, startwidth, widthvariation, col_start, col_var_bound, save, middlestar=False):
def printstar_nonrek_colorvariation(init_dict):
	# init:
	startlength 	= init_dict['raylength_start']
	startrays 		= init_dict['raynumber_start']
	startwidth 		= init_dict['raywidth_start']
	col_start 		= [init_dict['color_r_start'], init_dict['color_g_start'], init_dict['color_b_start'], init_dict['color_a_start']]

	# global modifiing rules:
	vlength_global 	= init_dict['raylength_vglobal']
	num_vlg = len(vlength_global)

	vnumber_global 	= init_dict['raynumber_vglobal']
	num_vng = len(vnumber_global)

	vwidth_global 	= init_dict['raywidth_vglobal']
	num_vwg = len(vwidth_global)

	vcolor_global 	= [init_dict['color_r_vglobal'], init_dict['color_g_vglobal'], init_dict['color_b_vglobal'], init_dict['color_a_vglobal']]

	# global-by-ray modifiing rules:
	vlength_ray 	= init_dict['raylength_vray']
	num_vlr = len(vlength_ray)

	vnumber_ray		= init_dict['raynumber_vray']
	num_vnr = len(vnumber_ray)

	vwidth_ray		= init_dict['raywidth_vray']
	num_vwr = len(vwidth_ray)

	vcolor_ray 	= [init_dict['color_r_vray'], init_dict['color_g_vray'], init_dict['color_b_vray'], init_dict['color_a_vray']]

	# local modifiing rules:	
	vcolor_local 	= [init_dict['color_r_vlocal'], init_dict['color_g_vlocal'], init_dict['color_b_vlocal'], init_dict['color_a_vlocal']]

	# color normalization:
	opt_norm_color  = init_dict['color_normalize']

	# other parameters:
	middlestar 		= init_dict['centerstar']
	maxiter 		= init_dict['iterations']
	save 			= init_dict['savetofile']
	background		= init_dict['background']

	currentdate = date.today()

	oh = OutputHandler()
	oh.init_output()

	# create starname:
	starname_1 = startrays+startlength+startwidth
		
	max_length_global = max(num_vlg, num_vng, num_vwg)
	starname_2 = [a+b+c for a,b,c in zip(
		vlength_global+[0]*(max_length_global-num_vlg),
		vnumber_global+[0]*(max_length_global-num_vng),
		vwidth_global+[0]*(max_length_global-num_vwg))
	]

	max_length_ray = max(num_vlr, num_vnr, num_vwr)
	starname_3 = [a+b+c for a,b,c in zip(
		vlength_ray+[0]*(max_length_ray-num_vlr),
		vnumber_ray+[0]*(max_length_ray-num_vnr),
		vwidth_ray+[0]*(max_length_ray-num_vwr))
	]

	starname_4 = [a+b+c+d for a,b,c,d in zip(
		col_start,
		vcolor_global[0],
		vcolor_ray[0],
		vcolor_local)
	]

	starname_5,k = re.sub(r'0*','',str(maxiter))

	starname = "star_"+str(starname_1)+str(starname_2)+str(starname_3)+str(starname_4)+str(maxiter)
	starname,k = re.subn(r'\.','',starname)
	starname,k = re.subn(r'[,\[\]0\s]*','',starname)

	print "name of star : "+starname

	oh.init_outputfile(starname)

	oh.set_background(background)

	savestepsize = 5000

	color_delta = 0.0
	color_delta_bound = vcolor_local[0]/2

	s = []

	lines = []
	linecolors = []
	linethicknesses = []

	xmin = 0
	xmax = 0
	ymin = 0
	ymax = 0

	# format of status:
	# [
	# 0:  depth
	# 1:  start_x,
	# 2:  start_y,
	# 3:  length,
	# 4:  angle,
	# 5:  number_of_rays,
	# 6:  linewidth,
	# 7:  [color_r, color_g, color_b, color_a],
	# 8:  [dr, dg, db]
	# ]
	status = [0, 0.0, 0.0, startlength, (1.5+(1.0/startrays))*math.pi, startrays, startwidth, [col_start[0], col_start[1], col_start[2], col_start[3]], [color_delta, color_delta, color_delta]]
	s.append(status)

	iteration = 0

	while len(s) > 0:		
		currentstatus = s.pop()
			
		iteration += 1
		if iteration%savestepsize == 0:
			print iteration

			if len(lines)>0:
				
				oh.save_line_data(lines, linecolors, linethicknesses, iteration/savestepsize)

				lines = []
				linecolors = []
				linethicknesses = []

		if iteration > maxiter:
			print "Maximum number of iterations reached. Stop."
			break

		rays = int(currentstatus[5])

		if currentstatus[3] >= 1 and currentstatus[5] >= 1 and currentstatus[5] <=50:

			delta_angle = 2*math.pi/rays

			color_current = currentstatus[7]

			nextlength = currentstatus[3] * vlength_global[currentstatus[0]%num_vlg]
			nextnumber = currentstatus[5] + vnumber_global[currentstatus[0]%num_vng]
			nextwidth  = currentstatus[6] + vwidth_global[currentstatus[0]%num_vwg]
			
			for i in range(0, rays):
				new_angle = currentstatus[4] + i*delta_angle
				end_x = currentstatus[1] + math.cos(new_angle)*currentstatus[3]
				end_y = currentstatus[2] - math.sin(new_angle)*currentstatus[3]

				xmin = min(xmin, end_x)
				xmax = max(xmax, end_x)
				ymin = min(ymin, end_y)
				ymax = max(ymax, end_y)

				new_color = [0,0,0,0]
				for c in range(4):
					new_color[c] = get_new_color_value(color_current[c], vcolor_global[c], currentstatus[0], vcolor_ray[c], i, vcolor_local[c], 0)

				if opt_norm_color:
					[nr, ng, nb] = norm_color(new_color[0], new_color[1], new_color[2])
				else:
					[nr, ng, nb] = new_color[0:3]

				lines.append([(currentstatus[1],currentstatus[2]), (end_x,end_y)])
				linecolors.append((nr, ng, nb, new_color[3]))
				linethicknesses.append(currentstatus[6])				

				s.append([
						currentstatus[0]+1,
						end_x,
						end_y,
						nextlength * vlength_ray[i%num_vlr],
						new_angle,
						nextnumber + vnumber_ray[i%num_vnr],
						nextwidth + vwidth_ray[i%num_vwr],
						[nr, ng, nb, new_color[3]]#,
					#	[new_dr, new_dg, new_db]
					])

			if middlestar:
				new_color = [0,0,0,0]
				for c in range(4):
					new_color[c] = get_new_color_value(color_current[c], vcolor_global[c], currentstatus[0], vcolor_ray[c], i, vcolor_local[c], 0)

				if opt_norm_color:
					[nr, ng, nb] = norm_color(new_color[0], new_color[1], new_color[2])
				else:
					[nr, ng, nb] = new_color[0:3]

				s.append([
						currentstatus[0]+1,
						currentstatus[1],
						currentstatus[2],
						nextlength,
						currentstatus[4],
						nextnumber,
						nextwidth,
						[nr, ng, nb, new_color[3]]#,
					#	[new_dr, new_dg, new_db]
					])

	print "iterations: " + str(iteration)

	oh.set_dimensions([xmin, xmax, ymin, ymax])

	oh.plt_collections_from_files(iteration/savestepsize)
	if (len(lines)>0):
		segments = clt.LineCollection(lines, colors=linecolors, linewidths=linethicknesses, antialiaseds=0)
		oh.plt_collection(segments)

	if save:
		print "Creating output image..."
		oh.set_img_size(init_dict['out_dim_x'], init_dict['out_dim_y'])
		oh.save_to_file()

	else:
		oh.show_plot()

init = load_init('init_test')

printstar_nonrek_colorvariation(init)

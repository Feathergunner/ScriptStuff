import matplotlib.pyplot as plt
import matplotlib.collections as clt
from matplotlib.colors import colorConverter
import math
import os.path
import numpy as np
from datetime import date, timedelta
import random
import re

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

	identifieres_bool = [
		'centerstar',
		'savetofile'
	]

	bg_colors = [
		'black',
		'white'
	]

	for line in initfile:
		if line[0] != '#' and len(line) > 1:
			terms = re.split(r'\s*=\s*',line)
			value = re.split(r'\s*',terms[1])[0]

			if terms[0] == 'iterations':
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

def write_linecollection_to_file(filename, collection, dimensions, background='white'):
	if not os.path.isfile(filename):
		fig = plt.figure()
		plt.axis('off')
		#ax = plt.axes()
		ax = fig.gca()
		ax.add_collection(collection)
		ax.set_autoscale_on(False)
		ax.plot()
		
		ax.axis(dimensions)
		fig.set_size_inches(10,10)

		plt.savefig(filename, dpi=300, facecolor=background)
		plt.close()
		return True
	else:
		return False

def print_linecollection(collection, dimensions, background='white'):
	fig = plt.figure(facecolor=background)
	plt.axis('off')
	ax = plt.axes()
	ax.add_collection(collection)
	ax.set_autoscale_on(False)
	ax.plot()

	ax.axis(dimensions)
	fig.set_size_inches(8,8)

	plt.show()
	plt.close()


###################################################################
# A function that creates star with QUADRATIC random colorvariation
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
	lengthfactor 	= init_dict['raylength_vglobal']
	number_of_lengthfactors = len(lengthfactor)

	rayvariation 	= init_dict['raynumber_vglobal']
	number_of_rayvariations = len(rayvariation)

	widthvariation 	= init_dict['raywidth_vglobal']
	number_of_widthvariations = len(widthvariation)

	color_vglobal 	= [init_dict['color_r_vglobal'], init_dict['color_g_vglobal'], init_dict['color_b_vglobal'], init_dict['color_a_vglobal']]

	# global-by-ray modifiing rules:

	color_vray 	= [init_dict['color_r_vray'], init_dict['color_g_vray'], init_dict['color_b_vray'], init_dict['color_a_vray']]

	# local modifiing rules:	
	color_vlocal 	= [init_dict['color_r_vlocal'], init_dict['color_g_vlocal'], init_dict['color_b_vlocal'], init_dict['color_a_vlocal']]

	#print color_vglobal
	#print color_vray
	#print color_vlocal

	# other parameters:
	middlestar 		= init_dict['centerstar']
	maxiter 		= init_dict['iterations']
	save 			= init_dict['savetofile']
	background		= init_dict['background']

	currentdate = date.today()
	dicname = "stars_" + date.isoformat(currentdate)

	color_delta = 0.0
	color_delta_bound = color_vlocal[0]/2

	'''
	print ("startlength    : %.2f" % startlength)
	print ("lengthfactor   : %.2f" % lengthfactor)
	print ("startrays      : %.2f" % startrays)
	print ("rayvariation   : %.2f" % rayvariation)
	print ("startwidth     : %.2f" % startwidth)
	print ("widthvariation : %.2f" % widthvariation)
	print ("col_start      : [%.2f, %.2f, %.2f, %.2f]" % (col_start[0], col_start[1], col_start[2], col_start[3]))
	'''

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
		if iteration%10000 == 0:
			print iteration

		if iteration > maxiter:
			print "Too big"
			break

		rays = int(currentstatus[5])

		if currentstatus[3] >= 1 and currentstatus[5] >= 1 and currentstatus[5] <=10:

			delta_angle = 2*math.pi/rays

			color_current = currentstatus[7]
			#colordelta_current = currentstatus[8]			

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
					new_color[c] = get_new_color_value(color_current[c], color_vglobal[c], currentstatus[0], color_vray[c], i, color_vlocal[c], 0)
				'''
				new_r = get_noized_color_value(color_current[0], col_var_bound, 0, colordelta_current[0])
				new_g = get_noized_color_value(color_current[1], col_var_bound, 0, colordelta_current[1])
				new_b = get_noized_color_value(color_current[2], col_var_bound, 0, colordelta_current[2])
				new_a = norm_value(get_noized_color_value(color_current[3], col_var_bound))
				'''

				[nr, ng, nb] = norm_color(new_color[0], new_color[1], new_color[2])

				'''
				new_dr = norm_value(get_noized_value(colordelta_current[0], color_delta_bound/2), -color_delta_bound, color_delta_bound)
				new_dg = norm_value(get_noized_value(colordelta_current[1], color_delta_bound/2), -color_delta_bound, color_delta_bound)
				new_db = norm_value(get_noized_value(colordelta_current[2], color_delta_bound/2), -color_delta_bound, color_delta_bound)
				'''

				lines.append([(currentstatus[1],currentstatus[2]), (end_x,end_y)])
				linecolors.append((nr, ng, nb, new_color[3]))
				linethicknesses.append(currentstatus[6])

				s.append([
						currentstatus[0]+1,
						end_x,
						end_y,
						currentstatus[3]*lengthfactor[currentstatus[0]%number_of_lengthfactors],
						new_angle,
						currentstatus[5] + rayvariation[currentstatus[0]%number_of_rayvariations],
						currentstatus[6] + widthvariation[currentstatus[0]%number_of_widthvariations],
						[nr, ng, nb, new_color[3]]#,
					#	[new_dr, new_dg, new_db]
					])

			if middlestar:
				new_color = [0,0,0,0]
				for c in range(4):
					new_color[c] = get_new_color_value(color_current[c], color_vglobal[c], currentstatus[0], color_vray[c], i, color_vlocal[c], 0)

				[nr, ng, nb] = norm_color(new_color[0], new_color[1], new_color[2])

				'''
				new_dr = norm_value(get_noized_value(colordelta_current[0], color_delta_bound/2), -color_delta_bound, color_delta_bound)
				new_dg = norm_value(get_noized_value(colordelta_current[1], color_delta_bound/2), -color_delta_bound, color_delta_bound)
				new_db = norm_value(get_noized_value(colordelta_current[2], color_delta_bound/2), -color_delta_bound, color_delta_bound)
				'''

				s.append([
						currentstatus[0]+1,
						currentstatus[1],
						currentstatus[2],
						currentstatus[3]*lengthfactor[currentstatus[0]%number_of_lengthfactors],
						currentstatus[4],
						currentstatus[5] + rayvariation[currentstatus[0]%number_of_rayvariations],
						currentstatus[6] + widthvariation[currentstatus[0]%number_of_widthvariations],
						[nr, ng, nb, new_a]#,
					#	[new_dr, new_dg, new_db]
					])

	print "iterations: " + str(iteration)

	segments = clt.LineCollection(lines, colors=linecolors, linewidths=linethicknesses, antialiaseds=0)
	
	if save:
		starname = "star_" + str(startrays) + "_" + str(rayvariation) + "_%.2f_" % startlength + str(lengthfactor) + "_" + str(startwidth) + "_" + str(widthvariation) + "_[%.2f, %.2f, %.2f, %.2f]_rand" % (col_start[0], col_start[1], col_start[2], col_start[3])
		if not os.path.exists(dicname):
			os.makedirs(dicname+"/")
		while not write_linecollection_to_file(dicname+"/"+starname + ".png", segments, [xmin, xmax, ymin, ymax], background):
			starname += "_"
	else:
		print_linecollection(segments, [xmin, xmax, ymin, ymax], background)

init = load_init('init_star')
#print init

printstar_nonrek_colorvariation(init)
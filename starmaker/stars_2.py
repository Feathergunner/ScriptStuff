import matplotlib.pyplot as plt
import matplotlib.collections as clt
from matplotlib.colors import colorConverter
import math
import os.path
import numpy as np
from datetime import date, timedelta
import random
import re

def load_init(filename):
	initfile = open(filename)
	init={}

	legal_identifieres_float = [
		'raynumber_start', 'raynumber_variation',
		'raylength_start', 'raylength_varfactor',
		'raywidth_start', 'raywidth_variation',
		'color_r_start', 'color_g_start', 'color_b_start', 'color_a_start',
		'iterations'
	]
	legal_identifieres_bool = [
		'centerstar',
		'savetofile'
	]

	for line in initfile:
		if line[0] != '#':
			terms = re.split(r'\s*=\s*',line)

			if terms[0] in legal_identifieres_float:
				init[terms[0]] = float(re.split(r'\s*',terms[1])[0])

			if terms[0] in legal_identifieres_bool:
				init[terms[0]] = bool(re.split(r'\s*',terms[1])[0])
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
	r_new = (r-l)/d
	g_new = (g-l)/d
	b_new = (b-l)/d
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
	startlength 	= init_dict['raylength_start']
	lengthfactor 	= init_dict['raylength_varfactor']
	startrays 		= init_dict['raynumber_start']
	rayvariation 	= init_dict['raynumber_variation']
	startwidth 		= init_dict['raywidth_start']
	widthvariation 	= init_dict['raywidth_variation']
	col_start 		= [init_dict['color_r_start'], init_dict['color_g_start'], init_dict['color_b_start'], init_dict['color_a_start']]
	col_var_bound 	= 0.2
	middlestar 		= init_dict['centerstar']
	maxiter 		= init_dict['iterations']
	save 			= init_dict['savetofile']

	currentdate = date.today()
	dicname = "stars_" + date.isoformat(currentdate)

	color_delta = 0.0
	color_delta_bound = col_var_bound/2

	print ("startlength    : %.2f" % startlength)
	print ("lengthfactor   : %.2f" % lengthfactor)
	print ("startrays      : %.2f" % startrays)
	print ("rayvariation   : %.2f" % rayvariation)
	print ("startwidth     : %.2f" % startwidth)
	print ("widthvariation : %.2f" % widthvariation)
	print ("col_start      : [%.2f, %.2f, %.2f, %.2f]" % (col_start[0], col_start[1], col_start[2], col_start[3]))

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
	# 0:  start_x,
	# 1:  start_y,
	# 2:  length,
	# 3:  angle,
	# 4:  number_of_rays,
	# 5:  lengthfactor,
	# 6:  linewidth,
	# 7:  [color_r, color_g, color_b, color_a],
	# 8:  [dr, dg, db]
	# ]
	status = [0.0,0.0, startlength, (1.5+(1.0/startrays))*math.pi, startrays, lengthfactor, startwidth, [col_start[0], col_start[1], col_start[2], col_start[3]], [color_delta, color_delta, color_delta]]
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

		rays = int(currentstatus[4])

		if currentstatus[2] >= 1 and currentstatus[4] >= 1 and currentstatus[4] <=10:

			delta_angle = 2*math.pi/rays

			color_current = currentstatus[7]
			colordelta_current = currentstatus[8]			

			for i in range(0, rays):
				new_angle = currentstatus[3] + i*delta_angle
				end_x = currentstatus[0] + math.cos(new_angle)*currentstatus[2]
				end_y = currentstatus[1] - math.sin(new_angle)*currentstatus[2]

				xmin = min(xmin, end_x)
				xmax = max(xmax, end_x)
				ymin = min(ymin, end_y)
				ymax = max(ymax, end_y)

				new_r = get_noized_color_value(color_current[0], col_var_bound, 0, colordelta_current[0])
				new_g = get_noized_color_value(color_current[1], col_var_bound, 0, colordelta_current[1])
				new_b = get_noized_color_value(color_current[2], col_var_bound, 0, colordelta_current[2])
				new_a = norm_value(get_noized_color_value(color_current[3], col_var_bound))

				[nr, ng, nb] = norm_color(new_r, new_g, new_b)
	
				new_dr = norm_value(get_noized_value(colordelta_current[0], color_delta_bound/2), -color_delta_bound, color_delta_bound)
				new_dg = norm_value(get_noized_value(colordelta_current[1], color_delta_bound/2), -color_delta_bound, color_delta_bound)
				new_db = norm_value(get_noized_value(colordelta_current[2], color_delta_bound/2), -color_delta_bound, color_delta_bound)

				lines.append([(currentstatus[0],currentstatus[1]), (end_x,end_y)])
				linecolors.append((new_r, new_g, new_b, new_a))
				linethicknesses.append(currentstatus[6])

				s.append([
						end_x,
						end_y,
						currentstatus[2]*currentstatus[5],#*math.pow(currentstatus[5],i+1),
						new_angle,
						currentstatus[4] + rayvariation,
						currentstatus[5],
						currentstatus[6] + widthvariation,
						[nr, ng, nb, new_a],
						[new_dr, new_dg, new_db]
					])

			if middlestar:
				new_r = get_noized_color_value(color_current[0], col_var_bound, 0, colordelta_current[0])
				new_g = get_noized_color_value(color_current[1], col_var_bound, 0, colordelta_current[1])
				new_b = get_noized_color_value(color_current[2], col_var_bound, 0, colordelta_current[2])
				new_a = norm_value(get_noized_color_value(color_current[3], col_var_bound))

				[nr, ng, nb] = norm_color(new_r, new_g, new_b)

				new_dr = norm_value(get_noized_value(colordelta_current[0], color_delta_bound/2), -color_delta_bound, color_delta_bound)
				new_dg = norm_value(get_noized_value(colordelta_current[1], color_delta_bound/2), -color_delta_bound, color_delta_bound)
				new_db = norm_value(get_noized_value(colordelta_current[2], color_delta_bound/2), -color_delta_bound, color_delta_bound)

				s.append([
						currentstatus[0],
						currentstatus[1],
						currentstatus[2]*currentstatus[5],#*math.pow(currentstatus[5],i+1),
						currentstatus[3],
						currentstatus[4] + rayvariation,
						currentstatus[5],
						currentstatus[6] + widthvariation,
						[nr, ng, nb, new_a],
						[new_dr, new_dg, new_db]
					])

	print "iterations: " + str(iteration)

	segments = clt.LineCollection(lines, colors=linecolors, linewidths=linethicknesses, antialiaseds=0)
	
	if save:
		starname = "star_" + str(startrays) + "_" + str(rayvariation) + "_%.2f_" % startlength + str(lengthfactor) + "_" + str(startwidth) + "_" + str(widthvariation) + "_[%.2f, %.2f, %.2f, %.2f]_rand" % (col_start[0], col_start[1], col_start[2], col_start[3])
		if not os.path.exists(dicname):
			os.makedirs(dicname+"/")
		while not write_linecollection_to_file(dicname+"/"+starname + ".png", segments, [xmin, xmax, ymin, ymax], 'white'):
			starname += "_"
	else:
		print_linecollection(segments, [xmin, xmax, ymin, ymax], 'black')


init = load_init('init_star')

print init

printstar_nonrek_colorvariation(init)
#printstar_nonrek_colorvariation(startlength, lengthfactor, startrays, rayvariation, width, widthvariation, color, c_v, write_to_file, middlestar)

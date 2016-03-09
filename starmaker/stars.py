import matplotlib.pyplot as plt
import matplotlib.collections as clt
from matplotlib.colors import colorConverter
import math
import os.path
import numpy as np
from datetime import date, timedelta
import random

def get_noized_color(color, maxdelta, mindelta=0.0):
	for i in range(0,3):
		color[i] = get_noized_color_val(color[i], maxdelta, mindelta)
	return color

def get_noized_color_val(cval, maxdelta, mindelta=0.0):
	col_var = np.random.uniform(mindelta, maxdelta)
	if random.randrange(0,10) > 5:
		col_var *= -1
	return get_new_color_value(cval, col_var)

def get_new_color_value(oldval, delta):
	newval = oldval+delta
	if newval < 0:
		newval = 0
	elif newval > 1:
		newval = 1

	return newval

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
# A function that creates star with user-defined colorvariation
###################################################################
def printstar_nonrek_variable(startlength, lengthfactor, startrays, rayvariation, startwidth, widthvariation, col_start, col_var, save):
	currentdate = date.today()
	dicname = "stars4_" + date.isoformat(currentdate)
	maxiter = 500000

	print ("startlength    : %.2f" % startlength)
	print ("lengthfactor   : %.2f" % lengthfactor)
	print ("startrays      : %.2f" % startrays)
	print ("rayvariation   : %.2f" % rayvariation)
	print ("startwidth     : %.2f" % startwidth)
	print ("widthvariation : %.2f" % widthvariation)
	print ("col_start      : [%.2f, %.2f, %.2f, %.2f]" % (col_start[0], col_start[1], col_start[2], col_start[3]))
	print ("col_var        : [%.2f, %.2f, %.2f, %.2f]" % (col_var[0], col_var[1], col_var[2], col_var[3]))
	s = []

	# initialization:
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
	# 5:  lengthfactor (factor by with length of rays is manipulated in each iteration,
	# 6:  linewidth,
	# 7:  color: red,
	# 8:  color: green,
	# 9:  color: blue,
	# 10: color: alpha
	# ]

	# initial status:
	status = [0.0,0.0, startlength, (1.5+(1.0/startrays))*math.pi, startrays, lengthfactor, startwidth, col_start[0], col_start[1], col_start[2], col_start[3]]
	s.append(status)

	iteration = 0

	while len(s) > 0:
		iteration += 1

		if iteration%10000 == 0:
			print iteration

		if iteration > maxiter:
			print "Too big"
			break
		
		currentstatus = s.pop()

		rays = int(currentstatus[4])

		if currentstatus[2] >= 1 and currentstatus[4] >= 1 and currentstatus[4] <=8:

			delta_angle = 2*math.pi/rays

			for i in range(0, rays):
				new_angle = currentstatus[3] + i*delta_angle
				end_x = currentstatus[0] + math.cos(new_angle)*currentstatus[2]
				end_y = currentstatus[1] - math.sin(new_angle)*currentstatus[2]

				xmin = min(xmin, end_x)
				xmax = max(xmax, end_x)
				ymin = min(ymin, end_y)
				ymax = max(ymax, end_y)

				lines.append([(currentstatus[0],currentstatus[1]), (end_x,end_y)])
				linecolors.append((currentstatus[7], currentstatus[8], currentstatus[9], currentstatus[10]))
				linethicknesses.append(currentstatus[6])

				s.append([
						end_x,
						end_y,
						currentstatus[2]*currentstatus[5],
						new_angle,
						currentstatus[4] + rayvariation,
						currentstatus[5],
						currentstatus[6] + widthvariation,
						get_new_color_value(currentstatus[7], col_var[0]),
						get_new_color_value(currentstatus[8], col_var[1]),
						get_new_color_value(currentstatus[9], col_var[2]),
						get_new_color_value(currentstatus[10], col_var[3])
					])

	segments = clt.LineCollection(lines, colors=linecolors, linewidths=linethicknesses, antialiaseds=0)
	
	if save:
		starname = "star_" + str(startrays) + "_" + str(rayvariation) + "_%.2f_" % startlength + str(lengthfactor) + "_" + str(startwidth) + "_" + str(widthvariation) + "_[%.2f, %.2f, %.2f, %.2f]_[%.2f, %.2f, %.2f, %.2f]" % (col_start[0], col_start[1], col_start[2], col_start[3], col_var[0], col_var[1], col_var[2], col_var[3])
		if not os.path.exists(dicname):
			os.makedirs(dicname+"/")
		while not write_linecollection_to_file(dicname+"/"+starname + ".png", segments, [xmin, xmax, ymin, ymax], 'black'):
			starname += "_"
	else:
		print_linecollection(segments, [xmin, xmax, ymin, ymax], 'black')


###################################################################
# A function that creates star with random colorvariation
###################################################################
def printstar_nonrek_colorvariation(startlength, lengthfactor, startrays, rayvariation, startwidth, widthvariation, col_start, col_var_bounds, save, middlestar=False):
	currentdate = date.today()
	dicname = "stars_" + date.isoformat(currentdate)
	maxiter = 500000

	col_variation = 0.08
	alpha_variation = -0.05

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
	# 7:  color_r,
	# 8:  color_g,
	# 9:  color_b,
	# 10: color_a
	# ]
	status = [0.0,0.0, startlength, (1.5+(1.0/startrays))*math.pi, startrays, lengthfactor, startwidth, col_start[0], col_start[1], col_start[2], col_start[3]]
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

			for i in range(0, rays):
				new_angle = currentstatus[3] + i*delta_angle
				end_x = currentstatus[0] + math.cos(new_angle)*currentstatus[2]
				end_y = currentstatus[1] - math.sin(new_angle)*currentstatus[2]

				xmin = min(xmin, end_x)
				xmax = max(xmax, end_x)
				ymin = min(ymin, end_y)
				ymax = max(ymax, end_y)


				new_r = get_noized_color_val(currentstatus[7], col_var_bounds[0], col_var_bounds[0]/2)
				new_g = get_noized_color_val(currentstatus[8], col_var_bounds[1], col_var_bounds[1]/2)
				new_b = get_noized_color_val(currentstatus[9], col_var_bounds[2], col_var_bounds[2]/2)
				new_a = get_new_color_value(currentstatus[10], col_var_bounds[3])

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
						new_r,
						new_g,
						new_b,
						new_a
					])

			if middlestar:
				new_r = get_noized_color_val(currentstatus[7], col_var_bounds[0], col_var_bounds[0]/2)
				new_g = get_noized_color_val(currentstatus[8], col_var_bounds[1], col_var_bounds[1]/2)
				new_b = get_noized_color_val(currentstatus[9], col_var_bounds[2], col_var_bounds[2]/2)
				new_a = get_new_color_value(currentstatus[10], col_var_bounds[3])

				s.append([
						currentstatus[0],
						currentstatus[1],
						currentstatus[2]*currentstatus[5],#*math.pow(currentstatus[5],i+1),
						currentstatus[3],
						currentstatus[4] + rayvariation,
						currentstatus[5],
						currentstatus[6] + widthvariation,
						new_r,
						new_g,
						new_b,
						new_a
					])

	print "iterations: " + str(iteration)

	segments = clt.LineCollection(lines, colors=linecolors, linewidths=linethicknesses, antialiaseds=0)
	
	if save:
		starname = "star_" + str(startrays) + "_" + str(rayvariation) + "_%.2f_" % startlength + str(lengthfactor) + "_" + str(startwidth) + "_" + str(widthvariation) + "_[%.2f, %.2f, %.2f, %.2f]_rand" % (col_start[0], col_start[1], col_start[2], col_start[3])
		if not os.path.exists(dicname):
			os.makedirs(dicname+"/")
		while not write_linecollection_to_file(dicname+"/"+starname + ".png", segments, [xmin, xmax, ymin, ymax], 'black'):
			starname += "_"
	else:
		print_linecollection(segments, [xmin, xmax, ymin, ymax], 'black')

# the length of the rays in the first iteration:
startlength = 200
# the factor by which the lengths get modified in each step (shoul be within [0,1) )
lengthfactor = 0.5
# the number of rays at the first iteration (int):
startrays = 6
# the total variation of the number of rays per iteration (does not need to be integer):
rayvariation = -0.5
# the linewidth in first iteration:
width = 3
# the variation of the linewidth per iteration:
widthvariation = -1
# a list with four elements defining the color of the zeroth iteration (r,g,b,a):
color = [0.5, 0.5, 0.5, 1]
# color variation per iteration, or bounds to the random color variation (depending on which method is used)
c_v = 0.1
a_v = 0.0
color_variation = [c_v, c_v, c_v, a_v]
# a bool describing if the output should be written to a file or shown (True = write to file):
write_to_file = True
# set to true to activate an additional recursive star added at the center of each star:
middlestar = True

printstar_nonrek_colorvariation(startlength, lengthfactor, startrays, rayvariation, width, widthvariation, color, color_variation, write_to_file, middlestar)
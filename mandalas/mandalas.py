import matplotlib.pyplot as plt
import matplotlib.collections as clt
import numpy as np
import math
import os.path
import random
from datetime import date
import sys

# creates a list of (x,y)-tuples that define a relativly smooth circle when plotted
def create_circle(center_x, center_y, r):
	x = []
	y = []
	circle = []
	for t in np.arange(0, 2*math.pi+0.1, 0.1):
		x = center_x + r*math.cos(t)
		y = center_y + r*math.sin(t)
		circle.append((x,y))
	return circle

# creates a list of (x,y)-tuples that define equally distant points on a circle
def get_regular_positions_on_circle(center_x, center_y, r, number_of_points):
	points = []
	stepwidth = (2*math.pi)/number_of_points

	for t in np.arange(0, 2*math.pi+stepwidth, stepwidth):
		points.append([center_x + r*math.cos(t), center_y + r*math.sin(t)])

	return points

# creates an image file based on a lineCollection
# @param mandala_collection		a lineCollection. All lines have to be within [-100,100] x [-100,100]
# @param filename 				a string containing a legal file name i.e. with fileending (preferably .png)
def save_mandala(mandala_collection, filename):
	fig = plt.figure(facecolor='white')

	plt.axis('off')
	ax = fig.gca()
	ax.add_collection(mandala_collection)
	ax.set_autoscale_on(False)
	ax.plot()
	ax.axis([-100,100,-100,100])
	if not os.path.isfile(filename):
		fig.set_size_inches(8,8)
		fig.savefig(filename, dpi=300)
	else:
		print "Filename already used!"

	plt.close()

# plots a lineCollection
# @param mandala_collection		a lineCollection. All lines have to be within [-100,100] x [-100,100]
def plot_mandala(madala_collection):
	fig = plt.figure(facecolor='white')

	plt.axis('off')
	ax = fig.gca()
	ax.add_collection(segments)
	ax.set_autoscale_on(False)
	ax.plot()
	ax.axis([-100,100,-100,100])
	plt.plot()
	plt.show()

	plt.close()

# Creates a random mandala
# @param complexity 	an int describing the upper bound for some randomly chosen parameters that influence the complexity of the mandala
#
# @return 				a lineCollection with all line segments that make the mandala. LineCollection can be used for functions plot_mandala or save_mandala
def create_mandala_rand(complexity):
	if complexity < 4:
		complexity = 4
	mandala = []
	mandala.append(create_circle(0,0,100))
	random.seed()

	number_of_levels = random.randrange(3,complexity)
	number_of_symmetries = random.randrange(3,complexity)
	if complexity < 6:
		complexity = 6

	points_per_sym = random.randrange(4,complexity-1)

	points_per_level = number_of_symmetries * points_per_sym

	rad_of_levels = [0]
	pts = [get_regular_positions_on_circle(0,0,0,points_per_level)]
	medium_differene_between_levels = 100.0/(number_of_levels-1)
	for level in range(1,number_of_levels-1):
		lowerbound = int(level*medium_differene_between_levels)
		upperbound = int(lowerbound + medium_differene_between_levels*0.9)

		thislevel_radius = random.randrange(lowerbound, upperbound)

		rad_of_levels.append(thislevel_radius)
		pts.append(get_regular_positions_on_circle(0,0,thislevel_radius, points_per_level))
	rad_of_levels.append(100)
	pts.append(get_regular_positions_on_circle(0,0,100, points_per_level))

	#for i in range(0, number_of_levels):
	#	print "Radius of level "+str(i) + " is: " + str(rad_of_levels[i])

	current_active_points = set()

	for level in range(0, number_of_levels-1):
		#print "Current level: " + str(level)
		if len(current_active_points) == 0:
			for i in range(0, points_per_sym/2):
				if random.randrange(0,6*points_per_sym) > 3+points_per_sym:
					current_active_points.add(i)
					current_active_points.add(-i)

		#print "Active points: " + str(current_active_points)

		if random.randrange(0,10) > 6:
			mandala.append(create_circle(0,0,rad_of_levels[level]))

		this_pts = pts[level]
		next_pts = pts[level+1]

		next_active_points = set()
		if len(current_active_points) < points_per_sym-1:
			if random.randrange(0,points_per_sym-len(current_active_points)) > (2*points_per_sym)/3.0:
				rad = min(rad_of_levels[level], 100-rad_of_levels[level+1])
				for p in this_pts:
					for i in range(0,number_of_symmetries):
						mandala.append(create_circle(p[0], p[1], rad))

		for p in current_active_points:
			if p >= 0:
				nextpoint_diff = random.randrange(0, int(points_per_sym/2))
				next_active_points.add((p+nextpoint_diff)%points_per_sym)
				next_active_points.add((p-nextpoint_diff)%points_per_sym)
				next_active_points.add((-p+nextpoint_diff)%points_per_sym)
				next_active_points.add((-p-nextpoint_diff)%points_per_sym)
				for i in range(0, number_of_symmetries):
					mandala.append((this_pts[((i*points_per_sym)+p)%points_per_level], next_pts[((i*points_per_sym)+p+nextpoint_diff)%points_per_level]))
					mandala.append((this_pts[((i*points_per_sym)+p)%points_per_level], next_pts[((i*points_per_sym)+p-nextpoint_diff)%points_per_level]))
					mandala.append((this_pts[((i*points_per_sym)-p)%points_per_level], next_pts[((i*points_per_sym)-p+nextpoint_diff)%points_per_level]))
					mandala.append((this_pts[((i*points_per_sym)-p)%points_per_level], next_pts[((i*points_per_sym)-p-nextpoint_diff)%points_per_level]))

		current_active_points = next_active_points


	print "Created random mandala with:"
	print "levels: " + str(number_of_levels)
	print "symmetries: " + str(number_of_symmetries)
	print "points per symmetry: " + str(points_per_sym)
	print current_active_points

	return mandala

def create_massive_mandalas(number):
	currentdate = date.today()
	dicname = "mandalas_" + date.isoformat(currentdate)
	if not os.path.exists(dicname):
		os.makedirs(dicname+"/")
	else:
		counter = 2
		while os.path.exists(dicname+"_"+str(counter)):
			counter += 1
		dicname = dicname+"_"+str(counter)
		os.makedirs(dicname+"/")

	for i in range(1, number+1):
		print i
		filename = dicname+"/mandala_"+str(i)+".png"
		segments = clt.LineCollection(create_mandala_rand(10), colors='black')
		save_mandala(segments, filename)

number_of_mandalas = 50

if len(sys.argv) > 1:
	try:
		int(sys.argv[1])
		number_of_mandalas = int(sys.argv[1])
	except:
		print "First parameter has to be integer!"

print "number: "+str(number_of_mandalas)

create_massive_mandalas(number_of_mandalas)
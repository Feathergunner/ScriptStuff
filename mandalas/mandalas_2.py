import matplotlib.pyplot as plt
import matplotlib.collections as clt
import numpy as np
import math
import os.path
import random
from datetime import date
import sys

class MandalaSliceLevel:
	total_number_of_slices  = 0
	radius 					= 0
	number_of_points 		= 0
	# list of tuples [index, radius (in points)] of circles contained on this level
	circles 		 		= [[]]
	# list for points, is 0 if there is no circle at point, otherwise index of circle
	circle_at_points 		= []

	def init(num_slices, rad, num_points):
		total_number_of_slices = num_slices
		radius = rad
		number_of_points = num_points
		circle_at_points = [0]*number_of_points

	def change_radius(delta):
		rad += dist
		min_dist = get_min_dist()
		if rad < min_dist:
			rad = min_dist

	def get_min_dist():
		# compute minimum distance to neighboring levels (needed if circle is containd on this level)
		maxrad = 0
		for c in circles:
			if c[1] > maxrad:
				maxrad = c[1]
		maxrad_absolut = maxrad * 2 * math.pi /(number_of_points * total_number_of_slices)
		return maxrad_absolut

	def get_points_lower():
		points = []
		# compute list of coordinates of points on upper level
		p = 0
		while p < number_of_points:
			if circle_at_points[p] == 0:
				# compute regular position on slice
				points.append((0,0))
				p += 1
			else:
				# append first point like normal point:
				points.append((0,0))
				p += 1
				# append other points:
				# get center of circle, compute point on lower half:
				center = circles[circle_at_points[p]][0]
				radius = circles[circle_at_points[p]][1]
				num_of_inner_circlepoints = 2*radius-1
				# approximate angle between first and last point of cycle:
				total_angle = 180 * (dist / (2*radius*dist_between_points))
				for p_i in range(1,num_of_inner_circlepoints+1):
					cur_angle = 270 - (total_angle)/2) + p_i * (total_angle / num_of_inner_circlepoints)
					# add point at center + position at current angle
					p += 1
		return points

	def get_points_upper():
		# compute list of coordinates of points on upper level
		points = []
		
		p = 0
		while p < number_of_points:
			if circle_at_points[p] == 0:
				# compute regular position on slice
				points.append((0,0))
				p += 1
			else:
				# append first point like normal point:
				points.append((0,0))
				p += 1
				# append other points:
				# get center of circle, compute point on lower half:
				center = circles[circle_at_points[p]][0]
				radius = circles[circle_at_points[p]][1]
				num_of_inner_circlepoints = 2*radius-1
				# approximate angle between first and last point of cycle:
				total_angle = 180 * (dist / (2*radius*dist_between_points))
				for p_i in range(1,num_of_inner_circlepoints+1):
					cur_angle = 90 - (total_angle)/2) + p_i * (total_angle / num_of_inner_circlepoints)
					# add point at center + position at current angle
					p += 1
		return points

	# no check for overlapping circles:
	def add_circle(point_index, radius_in_points):
		if (point_index - radius_in_points >= 0) and (point_index + radius_in_points < number_of_points):
			circles.append([point_index, radius_in_points])
			for p in (point_index - radius_in_points, point_index + radius_in_points +1):
				circle_at_points[p] = len(circles)

	def change_circle_size(point_index, new_radius):
		for c in range (0, len(circles)):
			if circles[c][0] == point_index:
				circles[c][1] = new_radius
				for p in (point_index - radius_in_points, point_index + radius_in_points +1):
					circle_at_points[p] = c


class MandalaSlice:
	number_of_levels = 0
	levels = []
	lines  = []

	def plot():


class MandalaCreater:
	# a list of lists of points, each list contains the equidistant points of a level
	pts=[[]]

	# a lists of tupels of points, describing all lines of the mandala
	mandala = []

	diameter             = 0
	number_of_levels     = 0
	number_of_symmetries = 0
	number_of_points     = []
	rad_of_levels        = []

	current_active_points    = set()
	current_level_to_compute = 0

	def init(diam, num_of_l, num_of_s):
		diameter = diameter
		number_of_levels = num_of_l
		number_of_symmetries = num_of_s
		number_of_points[0] = 1
		rad_of_levels[0] = 0
		current_level_to_compute = 1
		current_active_points.add(0)
		pts.append((0,0))

	def init_all_levels(num_of_p, rad_of_l):
		number_of_points += num_of_p
		rad_of_levels += rad_of_l


	def init_all_random(diam, complexity):
		if complexity < 4:
			complexity = 4
		random.seed()

		num_of_l = random.randrange(3,complexity)
		num_of_s = random.randrange(3,complexity)

		init(diam, num_of_l, num_of_s)

		if complexity < 6:
			complexity = 6

		points_per_sym = random.randrange(4,complexity-1)

		points_per_level = number_of_symmetries * points_per_sym

		num_of_p = [points_per_level]*number_of_levels

		rad_of_l = []

		medium_differene_between_levels = (float(diameter))/(number_of_levels-1)
		for level in range(1,number_of_levels-1):
			lowerbound = int(level*medium_differene_between_levels)
			upperbound = int(lowerbound + medium_differene_between_levels*0.9)

			thislevel_radius = random.randrange(lowerbound, upperbound)

			rad_of_l.append(thislevel_radius)

		rad_of_l.append(diameter)

		init_levels(num_of_p, rad_of_l)

	def init_next_level_generic():


	def add_next_step():
		if (current_level_to_compute < number_of_levels):
			if (current_level_to_compute <= len(rad_of_levels)+1):
				next_active_points = set()
				# if current level = 0
					# only one current_active_point
					# lines from center to points of next level
				# else

				if (current_level_to_compute == 0):
					next_points = number_of_points[1]/number_of_symmetries
					pts.append(get_regular_positions_on_circle(0, 0, rad_of_levels[1], number_of_points[1]))
					for i in range(3):
						nextpoint_diff = random.randrange(0, int(next_points/2))
						next_active_points.append((next_points/2)-nextpoint_diff)
						next_active_points.append((next_points/2)+nextpoint_diff)
					for p in next_active_points:
						for s in range(number_of_symmetries):
							mandala.append((pts[0][0],pts[1][s*next_points+p])

			else
				print "Error: No points for next level defined"

	def plot():
		mandala_collection = clt.LineCollection(m, colors='black')
		fig = plt.figure(facecolor='white')

		plt.axis('off')
		ax = fig.gca()
		ax.add_collection(madala_collection)
		ax.set_autoscale_on(False)
		ax.plot()
		ax.axis([-diam, diam, -diam, diam])
		plt.plot()
		plt.show()

		plt.close()


# moves a mandala in direction(dx, dy)
def move_mandala(mandala, dx, dy):
	new_mandala = []
	for line in mandala:
		new_line = []
		for point in line:
			new_point = (point[0] + dx, point[1] + dy)
			new_line.append(new_point)
		new_mandala.append(new_line)
	return new_mandala
	
#rotates a mandala by angle phi at 0,0
def rot_mandala(mandala, phi):
	new_mandala = []
	for line in mandala:
		new_line = []
		for point in line:
			new_point = (point[0]*math.cos(phi) - point[1]*math.sin(phi), point[0]*math.sin(phi) + point[1]*math.cos(phi))
			new_line.append(new_point)
		new_mandala.append(new_line)
	return new_mandala
	
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
def save_mandala(mandala_collection, diam, filename):
	fig = plt.figure(facecolor='white')

	plt.axis('off')
	ax = fig.gca()
	ax.add_collection(mandala_collection)
	ax.set_autoscale_on(False)
	ax.plot()
	ax.axis([-diam, diam, -diam, diam])
	if not os.path.isfile(filename):
		fig.set_size_inches(10,10)
		fig.savefig(filename, dpi=300)
	else:
		print "Filename already used!"

	plt.close()

# plots a lineCollection
# @param mandala_collection		a lineCollection. All lines have to be within [-100,100] x [-100,100]
def plot_mandala(madala_collection, diam):
	fig = plt.figure(facecolor='white')

	plt.axis('off')
	ax = fig.gca()
	ax.add_collection(madala_collection)
	ax.set_autoscale_on(False)
	ax.plot()
	ax.axis([-diam, diam, -diam, diam])
	plt.plot()
	plt.show()

	plt.close()
	
# Creates a mandala with given parameters
def create_mandala(diameter, number_of_levels, number_of_symmetries, points_per_sym, points_per_level, rad_of_levels, pts):
	random.seed()
	
	mandala = []
	mandala.append(create_circle(0,0,diameter))
	
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
				rad = min(rad_of_levels[level], diameter-rad_of_levels[level+1])
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
	#print current_active_points

	return mandala, current_active_points
	

# Creates a random mandala
# @param complexity 	an int describing the upper bound for some randomly chosen parameters that influence the complexity of the mandala
#
# @return 				a lineCollection with all line segments that make the mandala. LineCollection can be used for functions plot_mandala or save_mandala
def create_mandala_rand(complexity, diameter):
	if complexity < 4:
		complexity = 4
	random.seed()

	number_of_levels = random.randrange(3,complexity)
	number_of_symmetries = random.randrange(3,complexity)
	if complexity < 6:
		complexity = 6

	points_per_sym = random.randrange(4,complexity-1)

	points_per_level = number_of_symmetries * points_per_sym

	rad_of_levels = [0]
	pts = [get_regular_positions_on_circle(0,0,0,points_per_level)]
	medium_differene_between_levels = (float(diameter))/(number_of_levels-1)
	for level in range(1,number_of_levels-1):
		lowerbound = int(level*medium_differene_between_levels)
		upperbound = int(lowerbound + medium_differene_between_levels*0.9)

		thislevel_radius = random.randrange(lowerbound, upperbound)

		rad_of_levels.append(thislevel_radius)
		pts.append(get_regular_positions_on_circle(0,0,thislevel_radius, points_per_level))
	rad_of_levels.append(diameter)
	pts.append(get_regular_positions_on_circle(0,0,diameter, points_per_level))

	return create_mandala(diameter, number_of_levels, number_of_symmetries, points_per_sym, points_per_level, rad_of_levels, pts)


def create_multiple_mandalas(number):
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
		m, p = create_mandala_rand(10, 100)
		segments = clt.LineCollection(m, colors='black')
		save_mandala(segments, 100, filename)

# creates a massive mandala with sub-mandalas
def create_massive_mandala(size):
	random.seed()
	
	# init parameters:
	number_of_levels      = 3
	number_of_symmetries  = 3
	points_per_sym        = [0]*number_of_levels
	points_per_level      = [0]*number_of_levels
	base_number_of_points = 3
	rad_of_levels         = [0]*number_of_levels
	rad_of_levels.append(size)
	
	# init mandala:
	pts = [[[0,0]]]
	mandala = []
	mandala.append(create_circle(0,0,size))
	
	# init points for each level:
	for level in range(1,number_of_levels):
		points_per_level[level] = base_number_of_points+(4*level)
		thislevel_radius = level*(size/number_of_levels)
		pts.append(get_regular_positions_on_circle(0,0,thislevel_radius, points_per_level[level]))
		
	#print pts
		
	# create submandala:
	submandala, outer_points = create_mandala_rand(10, size/(2*number_of_levels+1))
	
	# create mandala:
	for l in submandala:
		mandala.append(l)
	for level in range(1,number_of_levels):
		# create submandala:
		submandala, outer_points = create_mandala_rand(6, size/(2*number_of_levels+1))
		for p_i in range(0, points_per_level[level]):
			p = pts[level][p_i]
			#print "add mandala at position"
			#print p
			angle = (float(p_i)/points_per_level[level])*2*math.pi
			tmp_submandala = rot_mandala(submandala, angle)
			tmp_submandala = move_mandala(tmp_submandala, p[0], p[1])
			for line in tmp_submandala:
				mandala.append(line)
	
	return mandala

def create_massive_mandalas_spec_1(size):
	random.seed()
	
	# init parameters:
	number_of_levels      = 3
	#number_of_symmetries  = 3
	#points_per_sym        = [0]*(number_of_levels+1)
	points_per_level      = [0]*number_of_levels
	rad_of_levels         = [0]*number_of_levels
	rad_of_levels.append(size)
	
	# init mandala:
	pts = [[[0,0]]]
	mandala = []
	mandala.append(create_circle(0,0,size))
	
	# init points for each level:
	points_per_level[1] = 10
	rad_of_levels[1]    = float(3)/4*size
	pts_level_1 = get_regular_positions_on_circle(0,0,rad_of_levels[1], points_per_level[1]) 
	pts.append(pts_level_1)

	'''
	points_per_level[2] = 6
	rad_of_levels[2]    = float(7)/8*size
	pts_level_2 = get_regular_positions_on_circle(0,0,rad_of_levels[2], points_per_level[2])
	pts.append(pts_level_2)
	'''

	# level 0:
	confirmed = False
	while(not confirmed):
		submandala, outer_points = create_mandala_rand(10, size/2)
		segments = clt.LineCollection(submandala, colors='black')
		plot_mandala(segments, size/2)
		t = input("Use this for level 0? [yes: 1 / no: 0] ")
		if (t > 0):
			confirmed = True

	for line in submandala:
		mandala.append(line)
	
	# level 1:
	confirmed = False
	while(not confirmed):
		submandala, outer_points = create_mandala_rand(6, size/5)
		segments = clt.LineCollection(submandala, colors='black')
		plot_mandala(segments, size/5)
		t = input("Use this for level 1? [yes: 1 / no: 0] ")
		if (t > 0):
			confirmed = True

	for point in range(0, points_per_level[1]):
		p = pts[1][point]
		angle = (float(point)/points_per_level[1])*2*math.pi
		tmp_submandala = rot_mandala(submandala, angle)
		tmp_submandala = move_mandala(tmp_submandala, p[0], p[1])
		for line in tmp_submandala:
			mandala.append(line)

	'''
	# level 2:
	submandala, outer_points = create_mandala_rand(5, size/10)
	for point in range(0, points_per_level[2]):
		p = pts[2][point]
		angle = (float(point)/points_per_level[2])*2*math.pi
		tmp_submandala = rot_mandala(submandala, angle)
		tmp_submandala = move_mandala(tmp_submandala, p[0], p[1])
		for line in tmp_submandala:
			mandala.append(line)
	'''

	return mandala

number_of_mandalas = 50

if len(sys.argv) > 1:
	try:
		int(sys.argv[1])
		number_of_mandalas = int(sys.argv[1])
	except:
		print "First parameter has to be integer!"

if (number_of_mandalas > 0):
	print "number: "+str(number_of_mandalas)
	create_multiple_mandalas(number_of_mandalas)
else:
	size = 300
	print "create single massive mandala"
	m = create_massive_mandalas_spec_1(size)
	filename = "mm_test.png"
	segments = clt.LineCollection(m, colors='black')
	#plot_mandala(segments, size)
	save_mandala(segments, size, filename)
		

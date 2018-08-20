import matplotlib.collections as clt

import math
import os.path
import numpy as np
from datetime import date, timedelta
import random
import re

import OutputHandler as outh

GLOBAL_SAVESTEPSIZE = 5000

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
	oh = outh.OutputHandler()

	oh.init_output()
	oh.init_outputfile(filename)
	oh.set_background(background)

	oh.plt_collection(collection)

	oh.set_img_size(dim_x, dim_y)
	oh.set_dimensions(dimensions)
	oh.save_to_file()

def print_linecollection(collection, dimensions, background='white'):
	oh = outh.OutputHandler()

	oh.set_background(background)
	oh.init_output()
	oh.plt_collection(collection)
	oh.set_dimensions(dimensions)
	oh.show_plot()

def create_starname(init_dict):
	#TO DO
	starname = 'default'

	return starname

def get_init_by_date():
    today = date.today()
    y = today.year
    m = today.month
    d = today.day
    return get_init_by_triple(y,m,d)

def get_init_by_triple(a,b,c):
    init = {}

    # numbers of rays:
    raynumber_start = (a + 5*c)%3 + (b*c)%3 + (a+b+c)%2 + 2.0
    init['raynumber_start'] = raynumber_start


    length_ray_cycle_1 = min(int(raynumber_start), (a+(3*c))%5 + 1)
    length_ray_cycle_2 = min(int(raynumber_start), (a+(11*b))%((7*c)%4+1) + 2)

    # base: iid in ~[0.05 , 0.5] times a factor depending on initial number of rays
    raynumber_vglobal_base = (((31*b+29*c)%11 + 1.0) / 22.0) * (3.5 / raynumber_start)**(0.5)

    raynumber_vray_base = [0.0]*length_ray_cycle_2
    for i in range(length_ray_cycle_2):
    	raynumber_vray_base[i] += float((i*c)%5 + (a*b+c)%3)/((23*b+17*c)%10+12)

    # move factor depending on initial number of rays:
    if raynumber_start <= 2.5:
    	init['raynumber_vglobal'] = [raynumber_vglobal_base + 0.4]
    	init['raynumber_vray']    = [x*1.2 for x in raynumber_vray_base]
    elif raynumber_start <= 3.5:
    	init['raynumber_vglobal'] = [raynumber_vglobal_base - 0.1]
    	init['raynumber_vray']    = [(x - 0.15)*1.2 for x in raynumber_vray_base]
    elif raynumber_start <= 4.5:
    	init['raynumber_vglobal'] = [(raynumber_vglobal_base - 0.25)]
    	init['raynumber_vray']    = [x - 0.25 for x in raynumber_vray_base]
    elif raynumber_start <= 5.5:
    	init['raynumber_vglobal'] = [raynumber_vglobal_base - 0.4]
    	init['raynumber_vray']    = [x - 0.3 for x in raynumber_vray_base]
    elif raynumber_start <= 6.5:
    	init['raynumber_vglobal'] = [raynumber_vglobal_base - 0.55]
    	init['raynumber_vray']    = [x - 0.4 for x in raynumber_vray_base]
    else:
    	init['raynumber_vglobal'] = [raynumber_vglobal_base - 0.8]
    	init['raynumber_vray']    = [x - 0.5 for x in raynumber_vray_base]

    #print "raynumber_vglobal: " + str(init['raynumber_vglobal'])
    #print "raynumber_vray:"
    #print (init['raynumber_vray'])

    medium_var_raynumber = init['raynumber_vglobal'][0] + (sum(init['raynumber_vray']) / length_ray_cycle_2)

    #print "medium_var_raynumber: " + str(medium_var_raynumber)

    # lengths of rays:
    init['raylength_start'] = 100.0
    raylength_vglobal_base = 0.6-((float((7*b+3*c)%10))/100) * (3.5 / raynumber_start)
    init['raylength_vglobal'] = [raylength_vglobal_base]

    init['raylength_vray'] = [1.0]*length_ray_cycle_1
    for i in range(length_ray_cycle_1):
    	init['raylength_vray'][i] -= 1.0/((i+1)*((a+3*b)%7) + (abs(7*c-b))%5 + 15)

    medium_var_raylength = (sum(init['raylength_vray']) * init['raylength_vglobal'][0]) / length_ray_cycle_1

    #print "medium_var_raylength: " + str(medium_var_raylength)
    #print "raylength_vglobal pre-fit: " +str(init['raylength_vglobal'][0])

    diff = -1
    if medium_var_raynumber > 0:
    	diff = 0
    elif medium_var_raynumber > -0.5:
    	diff = max(abs(medium_var_raynumber)**(1.8), abs(medium_var_raynumber)*0.25)

    if diff == 0:
    	if medium_var_raylength + medium_var_raynumber > 1.0:
    		diff += init['raylength_vglobal'][0]*0.1
    	elif medium_var_raylength + medium_var_raynumber > 0.5:
    		diff += (medium_var_raylength + medium_var_raynumber - 0.5)*1.1

    if diff > 0:
    	#print "diff: " + str(diff)
    	init['raylength_vglobal'][0] -= diff

    #print "raylength_vglobal post-fit: " +str(init['raylength_vglobal'][0])

    # widths of rays (constant):
    init['raywidth_start'] = 0.5
    init['raywidth_vglobal'] = [0.0]
    init['raywidth_vray'] = [0.0]

    # colors:
    init['color_r_start'] = 1.0/((a+7)%5+2.5)
    init['color_g_start'] = 1.0/((a+11)%5+2.5)
    init['color_b_start'] = 1.0/((a+13)%5+2.5)
    init['color_a_start'] = 1.0
    #init['col_var_bound'] = 

    init['color_r_vglobal'] = [0.0]
    init['color_g_vglobal'] = [0.0]
    init['color_b_vglobal'] = [0.0]
    init['color_a_vglobal'] = [0.0]

    init['color_r_vray'] = [0.0]
    init['color_g_vray'] = [0.0]
    init['color_b_vray'] = [0.0]
    init['color_a_vray'] = [0.0]

    init['color_r_vlocal'] = 1.0/((a+b+5*c)%5 + 4.5)
    init['color_g_vlocal'] = 1.0/((a+3*b+c)%5 + 4.5)
    init['color_b_vlocal'] = 1.0/((2*a+b+c)%5 + 4.5)
    init['color_a_vlocal'] = 0.0

    init['color_normalize'] = True

    init['savetofile'] = True
    init['centerstar'] = False
    if raynumber_start < 6 and (17*c*b%3) == 0:
        init['centerstar'] = True
    init['background'] = 'black'
    init['iterations'] = 100000.0

    init['out_dim_x'] = 1500
    init['out_dim_y'] = 1500
    init['starname']  = "star_triple_" + str(a) + "-" + str(b) + "-" + str(c)

    return init
    

###################################################################
# A function that creates star as specified by the init_dict
###################################################################
# startlength: 		inital length of locals
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
def printstar_nonrek_colorvariation(init_dict, create_video=False):
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

	'''
	print "Init:"
	print "startrays: "+str(startrays)
	print "raynumber_vglobal:" + str(vnumber_global)
	print "raynumber_vray:"
	print (vnumber_ray)
	print "raylength_vglobal:" + str(vlength_global)
	print "raylength_vray:"
	print (vlength_ray)
	print "col_start:"
	print (col_start)
	print "vcolor_local:"
	print (vcolor_local)
	'''

	currentdate = date.today()

	oh = outh.OutputHandler()
	oh.set_background(background)
	oh.init_output()

	# create starname:
	if 'starname' in init_dict:
		starname = init_dict['starname']
	else:
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

	print ("name of star : "+starname)

	if (not create_video):
		savestepsize = GLOBAL_SAVESTEPSIZE
		oh.init_outputfile(starname)
	else:
		savestepsize = 10
		oh.init_outputfile("star_vid")

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
			print (iteration)

			if len(lines)>0:
				
				oh.save_line_data(lines, linecolors, linethicknesses, iteration/savestepsize)

				lines = []
				linecolors = []
				linethicknesses = []

		if iteration > maxiter:
			print ("Maximum number of iterations reached. Stop.")
			break

		rays = int(currentstatus[5])

		if currentstatus[3] >= 1 and currentstatus[5] >= 2 and currentstatus[5] <=10:

			delta_angle = 2*math.pi/rays

			color_current = currentstatus[7]

			nextlength = currentstatus[3] * vlength_global[currentstatus[0]%num_vlg]
			nextnumber = currentstatus[5] + vnumber_global[currentstatus[0]%num_vng]
			nextwidth  = currentstatus[6] + vwidth_global[currentstatus[0]%num_vwg]
			
			for i in range(0, rays):
				new_angle = currentstatus[4] + i*delta_angle
				#if rays == 2:
				#	new_angle += delta_angle/2
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

	if not create_video:
		print ("iterations: " + str(iteration))

	oh.set_dimensions([xmin, xmax, ymin, ymax])

	oh.plt_collections_from_files(iteration/savestepsize, create_video)
	if (len(lines)>0):
		segments = clt.LineCollection(lines, colors=linecolors, linewidths=linethicknesses, antialiaseds=0)
		oh.plt_collection(segments)

	if save:
		print ("Creating output image...")
		oh.set_img_size(init_dict['out_dim_x'], init_dict['out_dim_y'])
		oh.save_to_file()

	else:
		oh.show_plot()

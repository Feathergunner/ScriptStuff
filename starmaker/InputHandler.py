
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
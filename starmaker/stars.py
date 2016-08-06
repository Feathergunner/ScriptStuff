
import sys
import StarMaker

import InputHandler as ih

if len(sys.argv)>1:
	init_file = sys.argv[1]
else:
	init_file = 'Init/test'

init = ih.load_init(init_file)

#init = StarMaker.get_init_by_date()

StarMaker.printstar_nonrek_colorvariation(init)
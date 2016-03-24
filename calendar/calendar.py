#!usr/bin/python

import os
import re
from subprocess import call

class calendar_constructor:
	inputfilename = "data.txt"

	year = 0
	first_day_of_months = [0,0,0,0,0,0,0,0,0,0,0,0]
	days_of_months = [31,28,31,30,31,30,31,31,30,31,30,31]

	holiday = [[],[],[],[],[],[],[],[],[],[],[],[]]
	public_holiday = [[],[],[],[],[],[],[],[],[],[],[],[]]
	birthdays = [{},{},{},{},{},{},{},{},{},{},{},{}]

	names_of_month_de = ['Januar', 'Februar', 'Maerz', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
	names_of_days_de = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']

	year_is_initialized = False

	scalefactor = 0.7
	dx = 1
	dy = 1

	endcode =[]

	def init_year(self):
		yz = self.year%100
		yh = self.year/100

		jzz = yz+yz/4
		jhh = (3-(yh%4))*2

		is_leap = 0
		if self.year%4 == 0:
			if not self.year%100 == 0:
				is_leap = 1
			elif self.year%2000 == 0:
				is_leap = 1

		self.first_day_of_months[0] = (0+jzz + jhh - is_leap)%7
		self.first_day_of_months[1] = (3+jzz + jhh - is_leap)%7
		self.first_day_of_months[2] = (3+jzz + jhh)%7
		self.first_day_of_months[3] = (6+jzz + jhh)%7
		self.first_day_of_months[4] = (1+jzz + jhh)%7
		self.first_day_of_months[5] = (4+jzz + jhh)%7
		self.first_day_of_months[6] = (6+jzz + jhh)%7
		self.first_day_of_months[7] = (2+jzz + jhh)%7
		self.first_day_of_months[8] = (5+jzz + jhh)%7
		self.first_day_of_months[9] = (0+jzz + jhh)%7
		self.first_day_of_months[10] = (3+jzz + jhh)%7
		self.first_day_of_months[11] = (5+jzz + jhh)%7

		if is_leap > 0:
			self.days_of_months[1] = 29

		self.year_is_initialized = True

	def init_files(self):
		if not os.path.exists("tex"):
			os.makedirs("tex/")

		self.templatefile = open('calendar_template.tex')

		self.outputfilename = "calendar_"+str(self.year)+".tex"
		self.outputfile = open("tex/"+self.outputfilename, 'w')

	def init_extern_data(self):
		keywords = ['Holiday:Personal', 'Holiday:Public', 'Anniversary']

		# mode defines which input is read:
		# 0: undefined
		# 1: holidays
		# 2: public holidays
		# 3: birthdays and anniversaries
		current_mode = 0

		current_month = 0

		if os.path.isfile(self.inputfilename):
			self.inputfile = open(self.inputfilename)
			for line in self.inputfile:
				if line[0] == '+':
					words = re.split(r'\+',line)
					key = re.sub('\s+','',words[1])
					if key == keywords[0]:
						current_mode = 1
					elif key == keywords[1]:
						current_mode = 2
					elif key == keywords[2]:
						current_mode = 3
					else:
						current_mode = 0
						print "Error! Undefined mode: "+key

				elif line[0] == 'm' or line[0] == 'M':
					terms = re.split(r':', line)
					value = int(re.sub('\s+','',terms[1]))
					current_month = value

				elif line[0] != '#' and line != '\n':
					if current_month>0 and current_month <= 12:
						terms = re.split(r':', line)
						values = re.split(r'-', terms[0])

						vals = []
						if len(values)==1:
							vals.append(int(re.sub('\s+','',values[0])))
						else:
							bound_l,k = re.subn('\s+','',values[0])
							bound_u,k = re.subn('\s+','',values[1])

							for i in range(int(bound_l), int(bound_u)+1):
								vals.append(i)

						if current_mode == 1:
							self.holiday[current_month-1] += vals
						elif current_mode == 2:
							self.public_holiday[current_month-1] += vals
						elif current_mode == 3:
							for v in vals:
								self.birthdays[current_month-1][v] = terms[1]
					#else:
					#	print "Error! Month not specified."

		else:
			print "Error! No inputfile data.txt found!"


	def init_calendar(self):
		self.init_extern_data()

		linecounter = 0
		for line in self.templatefile:
			linecounter += 1
			if (linecounter < 10):
				self.outputfile.write(line)
			if linecounter == 10:
				self.outputfile.write("{\\huge "+str(self.year)+"}\\\\[0.3cm]\n")
			if linecounter == 11:
				self.outputfile.write(line)
			if linecounter > 11:
				self.endcode.append(line)

	def get_code_weekdays(self,y):
		code_weekdays = []
		start_y = self.scalefactor * (y+6)
		for day in range(7):
			code_weekdays.append("\\node[anchor=east] at (-"+str(self.scalefactor)+","+str(start_y-self.scalefactor*day)+"){\\textbf{"+str(self.names_of_days_de[day][:2])+"}};\n")
		return code_weekdays

	def get_code_day(self, month, weekday, day, x, y):
		scaled_x = self.scalefactor * x
		scaled_y = self.scalefactor * y
		circlesize = self.scalefactor*0.45
		fillcolor = ""

		if day in self.holiday[month]:
			fillcolor = "[fill=blue!30]"
		if weekday > 4:
			fillcolor = "[fill=gray!30]"
		if day in self.public_holiday[month]:
			fillcolor = "[fill=green!40]"

		code = "\\draw"+fillcolor+" ("+str(scaled_x)+","+str(scaled_y)+") circle ("+str(circlesize)+");\n"
		code += "\\draw ("+str(scaled_x)+","+str(scaled_y)+") node{"+str(day)+"};\n"

		if day in self.birthdays[month]:
			code += "\\draw[orange, very thick] ("+str(scaled_x)+","+str(scaled_y)+") circle ("+str(self.scalefactor*0.35)+");"

		return code

	def construct_month(self, month, pos_x, pos_y):
		monthcode = []
		monthcode.append("\\node at ("+str(self.scalefactor*(pos_x+2.5))+","+str(self.scalefactor*(pos_y+7))+") {\\Large\\textsc{"+self.names_of_month_de[month]+"}};\n")

		for i in range(self.days_of_months[month]):
			day = i+1
			weekday = self.first_day_of_months[month]+i

			day_x = pos_x + (weekday/7)*self.dx
			day_y = pos_y + (6-(weekday%7))*self.dy

			monthcode.append(self.get_code_day(month, weekday%7, day, day_x, day_y))

		return monthcode

	def print_calendar(self, year):
		self.year = year
		self.init_year()
		self.init_files()
		self.init_calendar()

		calendar_code = []

		for row in range(4):
			pos_y = 25.5-row * 8.5
			for wd in self.get_code_weekdays(pos_y):
				calendar_code.append(wd)

			pos_x = 0
			for column in range(3):
				month = row*3+column
				calendar_code.append(self.construct_month(month, pos_x, pos_y))
				pos_x += (self.first_day_of_months[month]+self.days_of_months[month])/7+2

		for m in calendar_code:
			for l in m:
				self.outputfile.write(l)

		for line in self.endcode:
			self.outputfile.write(line)

		self.outputfile.close()

		self.create_pdf()

	def create_pdf(self):
		os.chdir("tex/")
		call(["pdflatex", self.outputfilename])

cc = calendar_constructor()
cc.print_calendar(2016)


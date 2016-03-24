#!usr/bin/python

#import sys
import os
#import re
from subprocess import call

class calendar_constructor:
	year = 0
	first_day_of_months = [0,0,0,0,0,0,0,0,0,0,0,0]
	days_of_months = [31,28,31,30,31,30,31,31,30,31,30,31]

	names_of_month_de = ['Januar', 'Februar', 'Maerz', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
	names_of_days_de = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']

	year_is_initialized = False
	input_is_initialized = False

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

		self.first_day_of_months[0] = (1+jzz + jhh - is_leap)%7
		self.first_day_of_months[1] = (4+jzz + jhh - is_leap)%7
		self.first_day_of_months[2] = (4+jzz + jhh)%7
		self.first_day_of_months[3] = (7+jzz + jhh)%7
		self.first_day_of_months[4] = (2+jzz + jhh)%7
		self.first_day_of_months[5] = (5+jzz + jhh)%7
		self.first_day_of_months[6] = (7+jzz + jhh)%7
		self.first_day_of_months[7] = (3+jzz + jhh)%7
		self.first_day_of_months[8] = (6+jzz + jhh)%7
		self.first_day_of_months[9] = (1+jzz + jhh)%7
		self.first_day_of_months[10] = (4+jzz + jhh)%7
		self.first_day_of_months[11] = (6+jzz + jhh)%7

		if is_leap > 0:
			self.days_of_months[1] = 29

		self.year_is_initialized = True

	def init_files(self):
		if not os.path.exists("tex"):
			os.makedirs("tex/")

		inputfilename = "data.txt"

		if os.path.isfile(inputfilename):
			this.inputfile = open(inputfilename)
			self.input_is_initialized = True
		else:
			print "Error! No inputfile data.txt found!"

		self.templatefile = open('calendar_template.tex')

		self.outputfilename = "calendar_"+str(self.year)+".tex"
		self.outputfile = open("tex/"+self.outputfilename, 'w')

	def init_calendar(self):
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

	def get_code_day(self, day, x, y):
		scaled_x = self.scalefactor * x
		scaled_y = self.scalefactor * y
		circlesize = self.scalefactor*0.45
		code = "\\draw ("+str(scaled_x)+","+str(scaled_y)+") circle ("+str(circlesize)+");\n"
		code += "\\draw ("+str(scaled_x)+","+str(scaled_y)+") node{"+str(day)+"};\n"
		return code

	def construct_month(self, month, pos_x, pos_y):
		monthcode = []
		monthcode.append("\\node at ("+str(self.scalefactor*(pos_x+2.5))+","+str(self.scalefactor*(pos_y+7))+") {\\Large\\textsc{"+self.names_of_month_de[month]+"}};\n")

		for i in range(self.days_of_months[month]):
			day = i+1
			weekday = self.first_day_of_months[month]+i

			day_x = pos_x + (weekday/7)*self.dx
			day_y = pos_y + (6-(weekday%7))*self.dy

			#print "day: " +str(i) + ", weekday: "+ str(weekday) + ", day_x/day_y: ("+str(day_x)+"/"+str(day_y)+")"

			monthcode.append(self.get_code_day(day, day_x, day_y))

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


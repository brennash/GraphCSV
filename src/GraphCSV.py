#!/usr/bin/env python
#################################################################################
#																				#																		#
# GraphCSV converts CSV input files into a HTML file containing all CSS and 	#
# JavaScript inline. 															#
#																				#
# @author Shane Brennan															#
# @date 20160716																#
#################################################################################

import csv
import math
import sys
import os
import datetime
import time
import re
import json
import datetime
import collections
import logging
import random
from sets import Set
from dateutil.relativedelta import relativedelta
from optparse import OptionParser
from logging.handlers import RotatingFileHandler

class GraphCSV:
	
	def __init__(self, ignoreHeaderFlag, lineChartFlag, inputFilename):
		
		# Set the flags to generate the chart options
		self.ignoreHeaderFlag = ignoreHeaderFlag
		
		# Instantiate the chart object
		self.chart            = Chart(lineChartFlag)
		
		# Parse the CSV input and update the chart
		self.processCSV(inputFilename)
		
		# Output the NVD3 chart as HTML
		html = self.chart.generateHTML()
		print html


	def processCSV(self, inputFilename):
		""" Process the CSV input and convert the input data into 
		    a valid NVD3 chart. 
		"""
		inputFile  = open(inputFilename, 'r')
		inputCSV   = csv.reader(inputFile)

		try:
			index = 0
			for row in inputCSV:
				if len(row) != 3:
					raise InputException('Input not in three-column CSV format')
				if self.ignoreHeaderFlag:
					if index > 0:
						category = row[0]
						xPos     = row[1]
						yPos     = row[2]
						self.chart.addElement(category, xPos, yPos)
				else:
					category = row[0]
					xPos     = row[1]
					yPos     = row[2]
					self.chart.addElement(category, xPos, yPos)
				index += 1
		except InputException, err:
			print 'Error: ', err.msg
 			exit

class Chart:
	def __init__(self, lineChartFlag):
		# Assign a random name to the chart
		self.chartName       =  'chart_' + ''.join(random.choice('1234567890') for i in range(6))
		self.xFormat         = None
		self.lineChartFlag    = lineChartFlag
		
		# Setup the chart elements and categories
		self.categoryList    = []
		self.categoryNames   = Set()

	def addElement(self, categoryName, xPos, yPos):
		""" Adds an element to the category and elements list.
		"""
		if self.xFormat is None:
			self.xFormat = self.getFormat(xPos)
		
		if categoryName in self.categoryNames:
			index    = self.getIndex(categoryName)
			category = self.categoryList[index]
			category.add(categoryName, xPos, yPos)
			self.categoryList[index] = category
		else:
			category = Category(categoryName, xPos, yPos)
			self.categoryList.append(category)
			self.categoryNames.add(categoryName)

	def getIndex(self, categoryName):
		""" Returns the index of a category matching the provided name.
		"""
		for index, category in enumerate(self.categoryList):
			if category.getName() == categoryName:
				return index
		return -1

	def getFormat(self, value):
		date1  = re.compile('[0-9]{4}[-/]{1}[0-9]{2}[-/]{1}[0-9]{2}')
		date2  = re.compile('[0-9]{2}[-/]{1}[0-9]{2}[-/]{1}[0-9]{4}')
		date3  = re.compile('20[0-9]{1}[0-9]{1}[0-1]{1}[0-9]{1}[0-3]{1}[0-9]{1}')
		float1 = re.compile('[0-9]+.[0-9]+')
		
		if date1.match(value):
			return '%Y-%m-%d'
		elif date2.match(value):
			return '%d-%m-%Y'
		elif date3.match(value):
			return '%Y%m%d'
		elif float1.match(value):
			return '%.2f'
		else:
			return '%.0f'

	def generateHTML(self):
		""" Generate HTML from the provided CSV.
		"""
		html = "<!DOCTYPE html>\n"
		html += "<html lang=\"en\">\n"
		html += "<!--- HEAD ---->\n"
		html += "<head>\n"
		html += "  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"/>\n"
		html += "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1, maximum-scale=1.0\"/>\n"
		html += "  <title>Grapher v1.0 Dashboard</title>\n"
		html += "  <link href=\"https://fonts.googleapis.com/icon?family=Material+Icons\" rel=\"stylesheet\">\n"
		html += "  <link href=\"http://materializecss.com/css/ghpages-materialize.css\" type=\"text/css\" rel=\"stylesheet\" media=\"screen,projection\"/ >\n"
		html += "  <link href=\"http://nvd3.org/assets/css/nv.d3.css\" rel=\"stylesheet\" type=\"text/css\">\n"
		html += "  <script src=\"http://nvd3.org/assets/lib/d3.v3.js\" charset=\"utf-8\"></script>\n"
		html += "  <script src=\"http://nvd3.org/assets/js/nv.d3.js\"></script>\n"
		html += "  <script src=\"http://nvd3.org/assets/js/data/stream_layers.js\"></script>\n"
		html += "</head>\n"
		html += "<!--- BODY ---->\n"
		html += "<body>\n\n"

		html += '<div id="{0}" style="height: 300px;"><svg></svg></div>\n'.format(self.chartName)

		html +=  "<!-- Script of Priority Tasks -->\n"
		html += "<script>\n"

		if self.lineChartFlag:
			html += "<script>\n"
			html += "\tvar chart = nv.models.stackedAreaChart()\n"
			html += "\t\t.margin({right: 100})\n"
			html += "\t\t.x(function(d) { return parseDate(d.x); } )\n"
			html += "\t\t.useInteractiveGuideline(true)\n"
			html += "\t\t.rightAlignYAxis(true)\n"
			html += "\t\t.transitionDuration(500)\n"
			html += "\t\t.showControls(true)\n"
			html += "\t\t.clipEdge(true);\n"

			if '%Y' in self.xFormat:                               
				html += "\tvar parseDate = d3.time.format(\"{0}\").parse;\n".format(self.xFormat)
				html += "\tchart.xAxis.tickFormat(function(d) {\n"
				html += "\treturn d3.time.format('{0}')(new Date(d))\n".format(self.xFormat)
			else:
				html += "\tchart.xAxis.tickFormat(d3.format(',.2f'));\n"
				
			html += "\t});\n"
			html += "\tchart.yAxis.tickFormat(d3.format(',.2f'));\n"
		else:
			html += "\tvar chart = nv.models.multiBarChart()\n"
			html += "\t\t.reduceXTicks(false)\n"
			html += "\t\t.rotateLabels(30)\n"
			html += "\t\t.showControls(false)\n"
			html += "\t\t.stacked(true)\n"
			html += "\t\t.groupSpacing(0.1);\n\n"

		html += "d3.select('#{0} svg').datum([\n".format(self.chartName)

		for categoryName in self.categoryNames:
			index      = self.getIndex(categoryName)
			category   = self.categoryList[index]

			jsonOutput = category.getJSON()
			jsonOutput = jsonOutput.replace('\n','')

			jsonOutput = re.sub(r'\s+', ' ', jsonOutput)
			jsonOutput = re.sub(r'"key"', '\n\tkey', jsonOutput)
			jsonOutput = re.sub(r'"color"', '\n\tcolor', jsonOutput)
			jsonOutput = re.sub(r'"values"', '\n\tvalues', jsonOutput)
			jsonOutput = re.sub(r'{ "x"', '\n\t{ x', jsonOutput)
			jsonOutput = re.sub(r'} ]}', '}\n\t]\n}', jsonOutput)

			html += jsonOutput
			html += ',\n'

		html = html[:-2]
		html += '\n'

		html += "]).transition().duration(500).call(chart);\n"
		html += "</script>\n"
		html += "</body>\n"
		html += "</html>\n"

		# Now clean up some of the formatting
		html = html.replace('"x"','x')
		html = html.replace('"y"','y')
		html = html.replace('"key"','key')
		html = html.replace('"color"','color')
		html = html.replace('"values"','values')

		return html
		

class Category:

	def __init__(self, categoryName, xPos, yPos):
		self.name                   = categoryName
		self.categoryDict           = collections.OrderedDict()
		self.categoryDict['key']    = categoryName
		self.categoryDict['color']  = "#%06x" % random.randint(0, 0xFFFFFF)
		coordDict                   = collections.OrderedDict()
		coordDict['x']              = xPos
		coordDict['y']              = float(yPos)
		valuesList                  = [ coordDict ]
		self.categoryDict['values'] = valuesList

	def add(self, name, xPos, yPos):
		if self.name == name:
			coordDict      = collections.OrderedDict()
			coordDict['x'] = xPos
			coordDict['y'] = float(yPos)
			valuesList = self.categoryDict['values']
			valuesList.append(coordDict)
			self.categoryDict['values'] = valuesList
		else:
			print 'UNMATCHED', self.categoryDict['key'], name
			exit(1)

	def getName(self):
		return self.categoryDict['key']

	def getColour(self):
		return self.categoryDict['color']

	def getJSON(self):
		jsonValue = json.dumps(self.categoryDict, indent=4)
		return jsonValue


class InputException(Exception):
	""" Define a custom exception for non-standard CSV inputs.
	"""
	def __init__(self, arg):
		self.msg = arg

		
def main(argv):
	parser = OptionParser(usage="Usage: Grapher <filename>")

	parser.add_option("-i", "--ignore",
		action="store_true",
		dest="ignoreHeaderFlag",
		default=False,
		help="Ignore the header in the CSV")

	parser.add_option("-l", "--linechart",
		action="store_true",
		dest="lineChartFlag",
		default=False,
		help="Create a line chart.")

	(options, filename) = parser.parse_args()

	if len(filename) != 1:
		print parser.print_help()
		exit(1)
	elif not os.path.isfile(filename[0]):
		print parser.print_help()
		print "Input file does not exist"
		exit(1)

	check = GraphCSV(options.ignoreHeaderFlag, options.lineChartFlag, filename[0])
		
if __name__ == "__main__":
    sys.exit(main(sys.argv))

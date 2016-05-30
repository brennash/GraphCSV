#################################################################################
#																				#
# GraphCSV converts CSV input files into a HTML file containing all CSS and 	#
# JavaScript inline. 															#
#																				#
# @author Shane Brennan															#
# @date 20160530																#
#################################################################################

import csv

class GraphCSV:

	def __init__(self, chartName, csvFilename):

		self.checkCSVData(csvFilename)

		widthPixels = 700
		heightPixels = 400

		conciseChartName = self.getConciseName(chartName)

		html = '<!DOCTYPE html>\n'
		html += '<html meta-charset="utf-8">\n'
		html += '<head><title>{0} - by GraphCSV</title></head>'.format(chartName)
		html += '<script src = "http://d3js.org/d3.v3.js"></script>\n'
		html += '<script src = "http://cdnjs.cloudflare.com/ajax/libs/nvd3/1.1.15-beta/nv.d3.js"></script>\n'
		html += '<link rel = "stylesheet" href = "http://cdnjs.cloudflare.com/ajax/libs/nvd3/1.1.15-beta/nv.d3.css">\n'

		html += '<h1>{0}</h1>\n'.format(chartName)
		html += '<div id = "{0}">\n'.format(conciseChartName)
		html += '<svg style=\'width:{0}px;height:{1}px\'> </svg>\n'.format(widthPixels, heightPixels)
		html += '</div>\n'

		html += '<script>\n'
		html += 'd3.csv("data/region_roi_type_all.csv",function(err,data){\n'
		html += 'var dataToPlot = Object.keys(data[0]).filter(function(k){return k!="date"})\n'
		html += '.map(function(k){\n'
		html += 'return {"key":k,"values":data.map(function(d){\n'
		html += 'return {\n'
		html += '"x":d3.time.format("%Y-%m").parse(d.date),\n'
		html += '"y":+d[k]\n'
		html += '}\n'
		html += '})\n'
		html += '}\n'
		html += '})\n'
		html += 'nv.addGraph(function() {\n'
		html += 'var chart = nv.models.multiBarChart()\n'
		html += '.transitionDuration(350)\n'
		html += '.reduceXTicks(false)\n'
		html += '.rotateLabels(0)\n'  
		html += '.showControls(true)\n'
		html += '.groupSpacing(0.1)\n'
		html += ';\n'
		html += 'chart.color(['#7DC242','#A0C6E9','#B1D78A','#C6DE89','#5F8AC7','#B2D235','#469638','#04003F','#004B1C','#004687','#4099D4','#002961']);\n'
		html += 'chart.xAxis.tickFormat(d3.time.format(\'%b-%Y\'));\n'
		html += 'chart.yAxis.tickFormat(d3.format(\',.1f\'));\n'
		html += 'd3.select(\'#{0} svg\')\n'.format(conciseChartName)
		html += '.datum(dataToPlot)\n'
		html += '.call(chart);\n'
		html += 'nv.utils.windowResize(chart.update);\n'
		html += 'return chart;\n'
		html += '});\n'
		html += '})\n'
		html += '</script>\n'

		html += '</body>\n'
		html += '</html>\n'

		
		print html
		
	def getConciseName(self, chartName):
		conciseChartName = chartName.lower().replace(' ', '_')
		return conciseChartName
		
	def checkCSVFilename(self, csvFilename):
		if not os.path.exists(csvFilename):
			print 'Error - Cannot file filename {0}'.format(csvFilename)
			return False
		elif not os.path.isfile(csvFilename):
			print 'Error - Cannot file filename {0}'.format(csvFilename)
			return False
		else:
			csvFile = open(csvFilename, 'rb')
			reader = csv.reader(csvFile)
			sniffer = csv.Sniffer()
    		if not sniffer.has_header(reader):
				print 'Error - CSV {0} has no header set'.format(csvFilename)
				return False  
			else:
				index = 0
				headerElements = 0
				for row in reader:
					if index == 0: 
						headerElements = len(row)	
					else:
						if len(row) != headerElements:
							print 'Error - row {0} has different number of row elements'.format(len(row))
							return False
					index += 1
				
				if index == 1:
					print 'Error - CSV has only header row and no data'.format(len(row))
					return False
		return True
			
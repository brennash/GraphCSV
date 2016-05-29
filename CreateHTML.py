#!/usr/bin/env python
import sys
import os
import time
import re
import datetime
from graph_csv.GraphCSV import GraphCSV
from dateutil.relativedelta import relativedelta
from optparse import OptionParser

def main(argv):
	parser = OptionParser(usage="Usage: CreateHTML [-n|--name chart-name] <csv-file>")

	parser.add_option("-n", "--name",
		action="store", 
		dest="name",
		type="str",
		default="Chart",
		help="The name of the chart.")

	(options, filename) = parser.parse_args()

	if len(filename) != 1:
		print parser.print_help()
		exit(1)

	if not os.path.isfile(filename[0]):
		print parser.print_help()
		print 'Need to specify valid input file!'
		exit(1)

	application = GraphCSV(options.name, filename[0])
		
if __name__ == "__main__":
    sys.exit(main(sys.argv))

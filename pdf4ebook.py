#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyPdf import PdfFileWriter, PdfFileReader
import sys
import os
from optparse import OptionParser

usage = "usage:  %prog [-m] [margin] FILENAME"
parser = OptionParser(usage=usage)
parser.add_option("-m", "--margins", action="store", dest="margins", default=False, help="BUTTOM_XxBUTTOM_YxTOP_XxTOP_Y\ndefault=None")	
parser.add_option("-s", "--size", action="store", dest="size", default=False, help="WidthxHeight\ndefault=None")
parser.add_option("-f", "--format", action="store", dest="format", default=False, help="page format (a5, a6...)\ndefault=None")
parser.add_option("-O", "--orientation", action="store", dest="orient", default="p", help="page orientation (p, l)\ndefault=p")


format_to_size = {
	'A5' : [1749., 2481.],
	'A6' : [1200., 1800.]
}

def resize(page, size=[0, 0], format='A6', orient='p'):
	if format:
		size_t = format_to_size[format]
		if orient == 'l':
			size = [max(size_t), min(size_t)]
		else: size = [min(size_t), max(size_t)]
	sx = size[0] / float((page.mediaBox.getUpperRight_x() - page.mediaBox.getLowerLeft_x()))
	sy = size[1] / float((page.mediaBox.getUpperRight_y() - page.mediaBox.getLowerLeft_y()))
	page.scale(sx, sy)
	
	return page

def pdf4ebook(filename, margins=[], size=[], format='', orient='p'):	
	
	output = PdfFileWriter()
	input = PdfFileReader(file(filename,"rb"))
	
	
	for i in range(input.getNumPages()):
		page = input.getPage(i) 
		
		if len(margins) == 4:
			page.mediaBox.upperRight = ( 	
				page.mediaBox.getUpperRight_x() - margins[2],
				page.mediaBox.getUpperRight_y() - margins[3]
			)
			page.mediaBox.lowerLeft = ( 	
				margins[0] ,
				margins[1]
			)
		
		if len(size) == 2:
			page = resize(page, size=size)
		if format:
			page = resize(page, format=format, orient=orient)
			
		output.addPage(page)
		
	
	outputStream = file(filename.split(".pdf")[0]+"_s.pdf","wb")
	output.write(outputStream)
	outputStream.close()
	

if __name__ == '__main__':
	(options, args) = parser.parse_args()
	if len(args) == 1 and os.path.exists(args[0]):
		margins, size, format = [], [], ''
		if options.margins:
			margins = [ int(i) for i in options.margins.split('x') ]
		if options.size:
			size = [ int(i) for i in options.size.split('x') ]
		if options.format:
			format = options.format.upper()
		
		pdf4ebook(args[0], size=size, margins=margins, format=format,
			orient=options.orient)
			
	else: print('Try help: -h, --help')
	
	

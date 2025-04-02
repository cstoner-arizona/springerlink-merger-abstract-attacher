"""
This is a (slightly) modified version of the code written by Rohit Dwivedula
(rohitdwivedula). Modifications were made by Ariel Machini (arielmachini).
The modifications were made because the method get_abstract() wasn't working
as it was intended (it returned "ABSTRACT NOT FOUND ERROR" for all of the
articles). Also, (1) «fieldnames» were modified to match the Springer CSV
column names and (2) additional fields were included for the output CSV file.
If you have any questions, you can contact me at
arielmachini (at) protonmail (dot) com. Hope this is useful for you! :)

@author arielmachini
@email arielmachini@protonmail.com
@url https://gist.github.com/arielmachini/f6f299c69230e258f4e49ab9814b3087
"""

import requests 
from bs4 import BeautifulSoup
import csv
import argparse
import os

def get_abstract(url):
	r = requests.get(url) 
	soup = BeautifulSoup(r.content, 'html.parser')
	abstract = soup.find(id='Abs1-content')
	return abstract.p.text.replace('\n','')

if __name__ == "__main__":
	count = 0
	parser = argparse.ArgumentParser()
	parser.add_argument("infile", help="location of CSV search file") # input file CSV
	parser.add_argument("outfile", help="where should output be saved?")
	args = parser.parse_args()
	assert(args.infile != args.outfile)
	errors = []
	with open(args.infile) as csvfile:
		flag = False
		if os.path.exists(args.outfile):
			flag = True
			count+=1
			with open(args.outfile) as outfile:
				countfile = csv.DictReader(outfile)
				for row in countfile:
					count+=1
			print("upto row ", count, " processed already.")

		with open(args.outfile, 'a') as outfile:
			fieldnames = ['Item Title', 'Item DOI', 'Authors', 'Publication Year', 'Content Type', 'URL', 'Abstract']
			reader = csv.DictReader(csvfile)
			writer = csv.DictWriter(outfile, fieldnames=fieldnames)
			if not flag:
				writer.writeheader()
			row_count = 1
			for row in reader:
				if row_count >= count:
					publication = {}
					for field in fieldnames:
						if field != 'Abstract':
							publication[field] = row[field]
					try:
						publication['Abstract'] = get_abstract(row['URL'])
					except AttributeError:
						publication['Abstract'] = "ABSTRACT NOT FOUND ERROR"
						print("Error at row ", row_count+1)
						errors.append(row_count+1)
					writer.writerow(publication)
					print("Processed row #", row_count+1)
				row_count += 1
	print("Errors occured at ", len(errors), "places: ", errors)

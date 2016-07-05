import urllib.request
import csv
from bs4 import BeautifulSoup
import sys

def removeHTTPS(url):
	if url.startswith("https"):
		url = url.replace("https", "http", 1)
	if url.endswith('/'):
		url = url[:-1]
	return url

def httpStatus(url, result):
	try: 
		page = urllib.request.urlopen(url)
		newURL = page.geturl()
		result.append(newURL) # optional number 4: the FINAL new redirect (the one we need to use for sitemap)
		redirURL = removeHTTPS(newURL)
		if redirURL != url:
			result.append(redirURL) # optional number 5 (really not that needed) - how it is different from number 3
			return 399
		else:
			return page.getcode()
	except urllib.error.URLError as e:
		print("Error in " + url) 
		return e.code

def main():
	try:
		file = sys.argv[1]
		outcome = []
		with open(file, 'rt', encoding = 'utf-8', errors = 'ignore') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				if len(row) > 0:
					url = row[0].strip()
					result = []
					result.append(url) # Number 1 that goes in: it's merely just whitespace-removed
					if not url.startswith('http'):
						continue
					newURL = removeHTTPS(url) 
					result.append(newURL) # Number 3: remove the https and last slash. some websites have that issue
					status = httpStatus(newURL, result)
					result.insert(1, status) # Number 2: what the status is 
					outcome.append(result) 
		if len(sys.argv) < 3:
			finalName = "Full Case Next Set.csv"
		else: 
			finalName = sys.argv[2]
		with open(finalName, "w") as output:
			writer = csv.writer(output, lineterminator = "\n")
			for line in outcome:
				writer.writerow(line)
	except IOError:
		print("Cannot open " + sys.argv[1])

if __name__ == "__main__":
	if len(sys.argv) > 2:
		main()
	else:
		print("Input the first argument as file to check links, second as the name of output.")

# Final order is this:
# The matching column from SQL
# Status
# Any edits I had to use to try it
# (optional) What it was converted to/redirected to
# (optional) A redirected URL if it was severe


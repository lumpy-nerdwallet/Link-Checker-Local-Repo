import unicodecsv
import urllib2
import csv
from bs4 import BeautifulSoup
import sys
import io
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def permute(url):
	options = []
	options.append("http://www.travelnerd.com/" + url)
	options.append("http://www.travelnerd.com/" + url + '/')
	options.append("https://www.travelnerd.com/" + url)
	options.append("https://www.travelnerd.com/" + url + '/')
	options.append('http://www.nerdwallet.com/' + url + '/')
	options.append('https://www.nerdwallet.com/' + url)
	options.append('https://www.nerdwallet.com/' + url + '/')
	return options

def removeHTTPS(url):
	if url.startswith("https"):
		url = url.replace("https", "http", 1)
	if url.endswith('/'):
		url = url[:-1]
	return url

def httpStatus(url):
	result = []
	try: 
		page = urllib2.urlopen(url, context = ctx)
		newURL = page.geturl()
		result.append(url) # number 3: what I inserted in FINALLY
		result.append(newURL) # number 4: what I got out FINALLY
		redirURL = removeHTTPS(newURL)
		strippedURL = removeHTTPS(url)
		if redirURL != strippedURL:
			result.insert(0, 399) # number 2: error code
		else:
			result.insert(0, page.getcode()) # number 2: error code
		return result
	except urllib2.URLError as e:
		print "Error in " + url
		if hasattr(e, 'code'):
			result = [e.code] # number 2: error code
			return result
		else:
			result = [1] # number 2: error code
			return result

def main():
	try:
		file = sys.argv[1]
		outcome = []
		with open(file, 'rt') as csvfile:
			reader = unicodecsv.reader(csvfile, encoding = 'ISO-8859-1')
			for row in reader:
				if len(row) > 0:
					try: 
						url = row[0].encode('ISO-8859-1').strip()
					except UnicodeEncodeError as e:
						url = "Error String"
					result = []
					result.append(url) # Number 1 that goes in: original path
					if url == "Error String":
						continue
					permutes = permute(url)
					for permutation in permutes:
						status = httpStatus(permutation)
						if len(status) > 1: ## it worked
							result = result + status
							break
					if len(result) == 1:
						result.append(-1) # has failed
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

from sys import argv
import re
from collections import Counter


def tokenize_simple(text):
	return text.lower().split()

def tokenize_regex(text):
	return re.findall(r'\w+', text.lower())

def tokenize_nosplit(text):
	clean_text = text.decode('utf8').replace(u"\u2018", "'").replace(u"\u2019", "'")
	return re.findall(r'\b[\w\']+\b', clean_text.lower())

if __name__ == '__main__':

	if len(argv) != 2:
		raise Exception('Script requires a file to open.')

	script_filename, book_filename = argv

	with open(book_filename, 'r') as infile:
		file_text = infile.read()

	simple_tokens = tokenize_simple(file_text)
	token_counter = Counter(simple_tokens)

	def print_tokens():
		for tup in token_counter.most_common(32):
			print '%s: %s' % tup

	print "\n\nSIMPLE TOKENS"
	print_tokens()

	regex_tokens = tokenize_regex(file_text)
	token_counter = Counter(regex_tokens)

	print "\n\nREGEX TOKENS"
	print_tokens()

	nosplit_tokens = tokenize_nosplit(file_text)
	token_counter = Counter(nosplit_tokens)

	print "\n\nNOSPLIT TOKENS"
	print_tokens()






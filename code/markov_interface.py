from collections import defaultdict, Counter
from random import choice as rc
from random import random
import json

def make_model(tokens, order):
	# model = defaultdict(list)
	model = defaultdict(Counter)
	for i in range(len(tokens)-order):
		history = tuple(tokens[i:i+order])
		next_token = tokens[i+order]
		model[history][next_token] += 1
		# model[ tuple(history) ].append(next_token)
	# def normalize(counter):
		# s = float(sum(counter.values()))
		# return [ (t, cnt/s) for t, cnt in counter.iteritems() ]
	def order(counter):
		return sorted(counter.keys(), key=lambda t: counter[t])

	final_model = { hist:order(token_counter) for hist, token_counter in model.iteritems() }

	return final_model

def save_model(filename, model):
	new_model = { ','.join(k) : model[k] for k in model.keys() }
	with open(filename, 'w') as outjson:
		json.dump(new_model, outjson)

def load_model(filename):
	with open(filename, 'r') as injson:
		model = json.load(injson)
	new_model = { tuple(k.split(',')) : model[k] for k in model.keys() }
	return new_model

def generate(model, length, seed=False):
	if not seed:
		seed = rc(model.keys())
	elif not seed in model:
		raise Exception("Seed not in model!")

	result = list(seed)

	# def generate_token(history):
	# 	dist = model[history]
	# 	x = random()
	# 	for t,v in dist:
	# 		x-=v
	# 		if x <= 0:
	# 			return t

	def generate_token(history):
		candidates = model[history]

		if len(candidates) > 1:
			for i, c in enumerate(candidates):
				print '%i. %s' % (i+1, c)
			user_input = raw_input('> ')
			choice_ix = int(user_input) - 1
			return candidates[choice_ix]
		else:
			return candidates[0]

	for _ in range(length):
		print ' '.join(result)
		next_token = generate_token(seed)
		result.append(next_token)
		prior_tokens = list(seed)[1:]
		prior_tokens.append(next_token)
		seed = tuple(prior_tokens)

	return ' '.join(result)

if __name__ == '__main__':
	from sys import argv
	from tokenize import tokenize_nosplit

	if len(argv) != 3:
		raise Exception('Script requires a file to and an order.')

	script_filename, book_filename, order_str = argv

	with open(book_filename, 'r') as infile:
		book_text = infile.read()

	book_tokens = tokenize_nosplit(book_text)

	book_model = make_model(book_tokens, int(order_str))

	save_model(book_filename.replace('.txt', '.json'), book_model)

	print generate(book_model, 100)
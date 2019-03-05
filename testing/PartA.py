import sys
import os
import time

import codecs
from itertools import repeat as repeat

def hw1_filter():
	"""
	Generate a dictionary with unicode points as key 
	and a value that indicates allowed as 1, not allowed as 0
	Only called once per program run
	"""
	uppercase_filter = create_filter(65, 90, 1)
	lowercase_filter = create_filter(97, 122, 1)
	digit_filter = create_filter(48, 57, 1)

	uppercase_filter.update(lowercase_filter)
	uppercase_filter.update(digit_filter)
	return uppercase_filter

def create_filter(start, end, default_value):
	"""
	helper function
	"""
	end += 1
	dic = {
		x : y
		for x in xrange(start, end) 
		for y in repeat(default_value, (end - start))
	}
	return dic 

tok_filter = hw1_filter()

def tokenizer_counting(file_name, d, chunk_size=10000):
	"""
	Open input file
	Read in a chunk from the file, each chunk is 10Kb as default
	Retain the last word and determine if it is a standalone word according to the next chunk
	Call on tokenizer() to properly remove all illegal characters

	Complexity: Worst Case would be O(n), where n = 1 byte
	"""
	with codecs.open(file_name, encoding='UTF-8', mode='r', errors='ignore') as input_file:

		buf = u''
		start_index = 0
		last_ws_index = 0

		for chunk in iter(lambda:input_file.read(chunk_size), u''):
			chunk = buf + chunk #	Combining reminder & empty previous buf
			buf = u''			#	put the last whitespace seperated string of characters to the buffer ...
								#	... to make sure it is a complete word
			last_ws_index = find_last_ws(chunk)
			if last_ws_index >= 0: #	pass the chunk with complete whitespace seperated words to the tokenizer
				buf = chunk[last_ws_index:]
				tokenizer(chunk, 0, last_ws_index, tok_filter, d)

			else: #	chunk is a continous string with no whitespace, but may require the next chunk to form a complete word
				buf = chunk
		
		if not len(buf) == 0: #	meaning the reminder chunk is a complete word with no whitespace
				tokenizer(buf, last_ws_index, len(buf),tok_filter, d)
	
	return d

def find_last_ws(str):
	"""
	O(n), n is the number byte between the last whitespace to the end of str
	"""
	index = len(str) - 1

	for char in reversed(str):
	
		if not int(ord(char)) in tok_filter:
			return index

		else:
			index -= 1

	return -1

def tokenizer(str, str_start, str_end, tok_filter, d):
	"""
	Remove all and partition according to illegal characters
	Illegal characters are determined from tok_filter
	Passes each token to counting()

	Complexity: O(n), where n = 1 byte
	"""
	if len(str) > 0:
		start_index = str_start
		end_index = start_index
		word = u''

		for char in str:
			
			if end_index < str_end:

				if not int(ord(str[end_index])) in tok_filter: #find a the closest seperator

					if end_index > start_index:
						word = str[start_index : end_index] #	add to dictionary and count
						start_index = end_index + 1 # update index
						counting(d, word.lower())

					elif end_index == start_index:
						start_index = end_index + 1

					else:
						pass
				
				end_index += 1

		if end_index > start_index:
			word = str[start_index : end_index]
			counting(d, word.lower())

def counting(dict, item):
	"""
	Complexity: O(1) for insertion, retrival, update of item
	"""
	if item in dict:
		dict[item] += 1
		
	else:
		dict[item] = 1

def sorted_print(dict, reverse=False):
	"""
	Complexity: O(n), where n is the number of key:value pair in dict
	"""
	for key, val in sorted(dict.iteritems(), 
							reverse = False, 
							key = lambda x: (-x[1], x[0])):#(key, val): (val, key)):
		print("%s\t%d" % (key, val))

if __name__ == '__main__':
	"""
	Due to my version of reading files by chunk
	The worst case scenario would be O(2n)
	If every chunk read has no illegal characters, thus the entire chunk will be read twice
	Once during the initial check for the last occurance of a illegal characters, 
	and twice during the tokenization

	O(nlogn) for sorting and printing
	"""
	#marker_time = time.time()
	
	if len(sys.argv) == 2:
		file_name = sys.argv[1]

		results_dict= {}

		tokenizer_counting(file_name, results_dict)

		sorted_print(results_dict, reverse=True)

	#time_dif = time.time() - marker_time
	#print("%.10f" % time_dif)

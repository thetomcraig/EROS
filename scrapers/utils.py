import random

def read_source_into_sentence_list(source_file):
	"""
	Reads a text file and returns its contents as list of sentances
	Split at punctuations
	Ignores words with punctuation in them, like Mr. and Mrs.
	"""
	lines = []
	punctuations = [".", "!", "?"]
	ignored_words = ["Mr.", "Mrs."]
	with open(source_file, "r") as file:
		line = []
		for file_line in file:
			for word in file_line.split():
				line.append(word)
				if any(p in word for p in punctuations):
					if all(not i in word for i in ignored_words):					
						lines.append(line)
						line = []

	return lines

 

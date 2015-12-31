__author__ = 'Yao (Frank) Fan'

POSITIVE_WORDS_FILE = './word_list/positive-words.txt'
NEGATIVE_WORDS_FILE = './word_list/negative-words.txt'

def get_positive_words_from(filename):
	"""
	Returns: a set of positive words
	Please use the returned words as global set in your program, so that it would not call this function multiple times.
	"""
	my_set = set()
	with open(filename) as file:
		for line in file:
			if line[0] == ';':
				pass
			elif line[0] == '':
				pass
			else:
				words = line.split()
				if len(words) > 0:
					my_set.add(words[0])
	print(len(my_set))
	return my_set


def get_negative_words_from(filename):
	"""
	Returns: a set of negative words
	Please use the returned words as global set in your program, so that it would not call this function multiple times.
	"""
	my_set = set()
	with open(filename) as file:
		for line in file:
			if line[0] == ';':
				pass
			elif line[0] == '':
				pass
			else:
				words = line.split()
				if len(words) > 0:
					my_set.add(words[0])
	print(len(my_set))
	return my_set


def main():
	get_negative_words_from(POSITIVE_WORDS_FILE)
	get_positive_words_from(NEGATIVE_WORDS_FILE)


if __name__ == '__main__':
	main()
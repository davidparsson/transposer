#!/usr/bin/python
# encoding: utf-8
"""
transposer.py

See README.md for information.

Created by David Pärsson on 2011-08-13.
Excessively doctested due to education.
"""

import sys
import os
import re, getopt

key_list = [('A',), ('A#', 'Bb'), ('B',), ('C',), ('C#', 'Db'), ('D',),
            ('D#', 'Eb'), ('E',), ('F',), ('F#', 'Gb'), ('G',), ('G#', 'Ab')]

sharp_flat = ['#', 'b']
sharp_flat_preferences = {
	'A' : '#',
	'A#': 'b',
	'Bb': 'b',
	'B' : '#',
	'C' : 'b',
	'C#': 'b',
	'Db': 'b',
	'D' : '#',
	'D#': 'b',
	'Eb': 'b',
	'E' : '#',
	'F' : 'b',
	'F#': '#',
	'Gb': '#',
	'G' : '#',
	'G#': 'b',
	'Ab': 'b',
	}
abc_to_doremi_dictionary = {
	'A' : 'LA',
	'B' : 'SI',
	'C' : 'DO',
	'D' : 'RE',
	'E' : 'MI',
	'F' : 'FA',
	'G' : 'SOL',
	}
doremi_to_abc_dictionary = { 
	abc_to_doremi_dictionary[chord]: chord for chord in abc_to_doremi_dictionary
	}

key_regex_abc = re.compile(r"[ABCDEFG][#b]?")
key_regex_doremi = re.compile(r"(?:DO|RE|MI|FA|SOL|LA|SI|DO)[#b]?")

def get_index_from_key(source_key):
	"""Gets the internal index of a key
	>>> get_index_from_key('Bb')
	1
	"""
	for key_names in key_list:
		if source_key in key_names:
			return key_list.index(key_names)
	raise Exception("Invalid key: %s" % source_key)

def get_key_from_index(index, to_key):
	"""Gets the key at the given internal index.
	Sharp or flat depends on the target key.
	>>> get_key_from_index(1, 'Eb')
	'Bb'
	"""
	key_names = key_list[index % len(key_list)]
	if len(key_names) > 1:
		sharp_or_flat = sharp_flat.index(sharp_flat_preferences[to_key])
		return key_names[sharp_or_flat]
	return key_names[0]

def get_transponation_steps(source_key, target_key):
	"""Gets the number of half tones to transpose
	>>> get_transponation_steps('D', 'C')
	-2
	"""
	source_index = get_index_from_key(source_key)
	target_index = get_index_from_key(target_key)
	return target_index - source_index

def transpose_file(file_name, from_key, to_key, chord_style_in='abc', chord_style_out='abc'):
	"""Transposes a file from a key to another.
	>>> transpose_file('example.txt', 'D', 'E')
	'Rocking start, jazzy ending\\n| E | A B | Cm7#11/D# |\\n'
	"""
	direction = get_transponation_steps(from_key, to_key)
	result = ''
	try:
		for line in open(file_name):
			result += transpose_line(line, direction, to_key, chord_style_in, chord_style_out)
		return result
	except IOError:
		print("Invalid filename!")
		usage()

def transpose_line(source_line, direction, to_key, chord_style_in='abc', chord_style_out='abc'):
	"""Transposes a line a number of keys if it starts with a pipe. Examples:
	>>> transpose_line('| A | A# | Bb | C#m7/F# |', -2, 'C')
	'| G | Ab | Ab | Bm7/E |'

	Different keys will be sharp or flat depending on target key.
	>>> transpose_line('| A | A# | Bb | C#m7/F# |', -2, 'D')
	'| G | G# | G# | Bm7/E |'

	It will use the more common key if sharp/flat, for example F# instead of Gb.
	>>> transpose_line('| Gb |', 0, 'Gb')
	'| F# |'

	Lines not starting with pipe will not be transposed
	>>> transpose_line('A | Bb |', -2, 'C')
	'A | Bb |'
	"""
	if source_line[0] != '|':
		return source_line
	if chord_style_in == 'abc':
		source_chords = key_regex_abc.findall(source_line)
	elif chord_style_in == 'doremi':
		source_chords = key_regex_doremi.findall(source_line)
		source_chords = [chord_doremi_to_abc(chord) for chord in source_chords]
		source_line = key_regex_doremi.sub(lambda x: chord_doremi_to_abc(x.group()),source_line)
	else:
		raise Exception("Invalid input chord style: %s" % chord_style_in)
	return recursive_line_transpose(source_line, source_chords, direction, to_key, chord_style_out)
	
def chord_doremi_to_abc(x):
	"""Converts a chord from DO-RE-MI to A-B-C notation.
	>>> chord_doremi_to_abc('MIb')
	'Eb'
	"""
	sharp_flat = re.findall(r'[b\#]', x)
	clean_chord = re.sub(r'[b\#]','', x)
	translated_chord = doremi_to_abc_dictionary[clean_chord]
	for sf in sharp_flat:
		translated_chord += sf
	return translated_chord
	
def recursive_line_transpose(source_line, source_chords, direction, to_key, chord_style_out='abc'):
	if not source_chords or not source_line:
		return source_line
	source_chord = source_chords.pop(0)
	chord_index = source_line.find(source_chord)
	after_chord_index = chord_index + len(source_chord)
	return source_line[:chord_index] + \
		   transpose(source_chord, direction, to_key, chord_style_out) + \
		   recursive_line_transpose(source_line[after_chord_index:], source_chords, direction, to_key, chord_style_out)


def transpose(source_chord, direction, to_key, chord_style_out='abc'):
	"""Transposes a chord a number of half tones.
	Sharp or flat depends on target key.
	>>> transpose('C', 3, 'Bb')
	'Eb'
	"""
	source_index = get_index_from_key(source_chord)
	k = get_key_from_index(source_index + direction, to_key)
	if chord_style_out == 'abc':
		return k
	elif chord_style_out == 'doremi':
		return chord_abc_to_doremi(k)
	raise Exception("Invalid output chord style: %s" % chord_style_out)

def chord_abc_to_doremi(x):
	"""Converts a chord from A-B-C to DO-RE-MI notation.
	>>> chord_abc_to_doremi('Eb')
	'MIb'
	"""
	sharp_flat = re.findall(r'[b\#]', x)
	clean_chord = re.sub(r'[b\#]','', x)
	translated_chord = abc_to_doremi_dictionary[clean_chord]
	for sf in sharp_flat:
		translated_chord += sf
	return translated_chord

def is_abc(chord):
	"""Returns True if a chord is in the A-B-C notation.
	False is returned otherwise.
	>>> is_abc('Eb')
	True

	>>> is_abc('FA')
	False
	"""
	return re.sub(r'[b\#]', '', chord) in abc_to_doremi_dictionary

def is_doremi(chord):
	"""Returns True if a chord is in the DO-RE-MI notation.
	False is returned otherwise.
	>>> is_doremi('Eb')
	False

	>>> is_doremi('FA')
	True
	"""
	return re.sub(r'[b\#]', '', chord) in doremi_to_abc_dictionary


def usage():
	print('Usage:')
	print('python3 %s --from=Eb --to=F# --style-in=abc --style-out=doremi input_filename' % os.path.basename(__file__))
	sys.exit(2)

def main():
	from_key = 'C'
	to_key = 'C'
	chord_style_in = 'abc'
	chord_style_out = 'abc'
	file_name = None
	try:
		options, arguments = getopt.getopt(sys.argv[1:], 'f:t:', ['from=', 'to=', 'style-in=', 'style-out=', 'doctest'])
	except getopt.GetoptError as err:
		print(str(err))
		usage()
	for option, value in options:
		if option in ('-f', '--from'):
			from_key = value
			if is_doremi(from_key):
				from_key = chord_doremi_to_abc(from_key)
		elif option in ('-t', '--to'):
			to_key = value
			if is_doremi(to_key):
				to_key = chord_doremi_to_abc(to_key)
		elif option in ('-i', '--style-in'):
			chord_style_in = value
		elif option in ('-o', '--style-out'):
			chord_style_out = value
		elif option == '--doctest':
			import doctest
			doctest.testmod()
			exit()
		else:
			usage()
	
	if arguments:
		file_name = arguments[0]
	else:
		usage()
	
	result = transpose_file(file_name, from_key, to_key, chord_style_in, chord_style_out)

	if chord_style_in == 'abc':
		from_key_ = from_key
	elif chord_style_in == 'doremi':
		from_key_ = chord_abc_to_doremi(from_key)
	else:
		raise Exception("Invalid input chord style: %s" % chord_style_in)

	if chord_style_out == 'abc':
		to_key_ = to_key
	elif chord_style_out == 'doremi':
		to_key_ = chord_abc_to_doremi(to_key)
	else:
		raise Exception("Invalid output chord style: %s" % chord_style_out)
	
	print("Finished transposing from '%s' to '%s':" % (from_key_, to_key_))
	print(result)
	
if __name__ == '__main__':
	main()

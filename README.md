Transposer
==========

Transposing chords from one key to another

Usage
-----

To transpose chords, use transposer like this:
	python transposer.py --from=F# --to=Eb input.txt

The text file can contain anything - only lines starting with a vertical bar (`|`) will be transposed. On these lines, root notes must be in upper case while everything else should be in lower case.

Example
-------
The contents `input.txt`:
	Rocking start, weird ending
	| D | G A | Bbm7#11/Db |

Using `transposer --from=D --to=E input.txt` will produce the result
	Result (D -> E):
	Rocking start, weird ending
	| E | A B | Cm7#11/D# |


Transposer
==========

Transposing chords from one key to another

Usage
-----

To transpose chords, use transposer like this:

    python transposer.py --from=F# --to=Eb input.txt

Input files
-----------

The input file should be a plain text file, but can contain any text - only lines starting with a vertical bar (`|`) will be transposed. On these lines, root notes must be in upper case while everything else should be in lower case.

Example
-------
The contents of `example.txt`:

    Rocking start, jazzy ending
    | D | G A | Bbm7#11/Db |

Using `transposer --from=D --to=E example.txt` will produce the result

    Result (D -> E):
    Rocking start, jazzy ending
    | E | A B | Cm7#11/D# |


Testing
-------

Run unit tests using Python's doctest:

    python -m doctest -v transposer.py

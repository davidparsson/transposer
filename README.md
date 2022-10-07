Transposer 
==========

[![Build Status](https://github.com/bfrangi/transposer/workflows/CI/badge.svg)](https://github.com/bfrangi/transposer/actions?query=workflow%3ACI)

Transposing chords from one key to another and changing between Do-Re-Mi and A-B-C notations.

Usage
-----

To transpose chords, use transposer like this:

    python transposer.py --from=F# --to=Eb input.txt

Optional Parameters
----

You can also use the parameters `--style-in` and `--style-out` in order to choose Do-Re-Mi or A-B-C systems for the input and output.

For example, the following would take a sequence of chords in the Do-Re-Mi system and convert them to the A-B-C system without transposing:

    python transposer.py --from=D --to=Re --style-in=doremi --style-out=abc input.txt

`--from` and `--to` parameters can always be given in either system.

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

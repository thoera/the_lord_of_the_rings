# -*- coding: utf-8 -*-

"""
A script to parse The Lord of the Rings: The Return of the King.
Input file: the-return-of-the-king.txt
"""

import os
import codecs
import re

# Set the working directory.
os.chdir(r".\datasets\the_lord_of_the_rings")

# Read the script line by line.
def read_script(filename):
    # Open the file for reading.
    with open(filename, "r", encoding="CP1252") as infile:
        input_file = infile.read()  # Read the contents of the file into memory.
    # Return a list of the lines, breaking at line boundaries.
    full_text = input_file.splitlines()
    return full_text

script = read_script(r"the-return-of-the-king.txt")

# Create a text file of the dialogues.
file_output = codecs.open(r"dialogues_the-return-of-the-king.txt", "w", "utf-8")
file_output.write("Character|Dialogue")

for line in script:
    # If character name:
    if re.match("( ){23} (\w+)", line):
        # Remove parentheses, "V/O" and "O.S.".
        line = re.sub(" *(\(.+\)|V/0|O\.S\.*)", "", line)
        # Write to the new file.
        file_output.write("\n")
        file_output.write(line[24:] + "|")
    # If dialogue:
    if re.match("( ){11} (\w|\.+)", line):
        file_output.write(line[12:] + " ")

file_output.close()

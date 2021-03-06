# -*- coding: utf-8 -*-

"""
A script to parse The Lord of the Rings: The Two Towers.
Input file: the-two-towers.txt
"""

import os
import codecs
import re

# Set the working directory.
os.chdir(r".\datasets\the_lord_of_the_rings")

# Read the script line by line.
def read_script(filename):
    # Open the file for reading.
    with open(filename, "r", encoding="utf-8") as infile:
        input_file = infile.read()  # Read the contents of the file into memory.
    # Return a list of the lines, breaking at line boundaries.
    full_text = input_file.splitlines()
    return full_text

script = read_script(r"the-two-towers.txt")

# Create a text file of the dialogues.
file_output = codecs.open(r"dialogues_the-two-towers.txt", "w", "utf-8")
file_output.write("Character|Dialogue")

for line in script:
    # If character name:
    if re.match("( ){27} (\w+)", line):
        # Remove parentheses.
        line = re.sub(" *\(.+\)", "", line)
        # Write to the new file.
        file_output.write("\n")
        file_output.write(line[28:-2] + "|")
    # If dialogue:
    if re.match("( ){11} (\w|\.+)", line):
        file_output.write(line[12:] + " ")

file_output.close()

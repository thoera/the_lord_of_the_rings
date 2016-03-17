# -*- coding: utf-8 -*-

"""
A script to parse The Lord of the Rings: The Fellowship of the Ring.
Input file: the-fellowship-of-the-ring.txt
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

script = read_script(r"the-fellowship-of-the-ring.txt")

# Create a text file of the dialogues.
file_output = codecs.open(r"dialogues_the-fellowship-of-the-ring.txt", 
                          "w", "utf-8")
file_output.write("Character|Dialogue")

for line in script:
    # If character name:
    if re.match("( ){19} (\w+)", line):
        # Remove parentheses.
        line = re.sub(" *\(.+\)", "", line)
        # Write to the new file.
        file_output.write("\n")
        file_output.write(line[20:] + "|")
    # If dialogue:
    if re.match("( ){9} (\w|\.+)", line):
        file_output.write(line[10:] + " ")

file_output.close()

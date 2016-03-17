# -*- coding: utf-8 -*-

"""
A script to create an adjacency matrix based on the closeness 
of the words used by the 20 most talkative characters.
"""

import os
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from scipy.spatial.distance import squareform
from scipy.spatial.distance import pdist, jaccard
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# Set the working directory.
os.chdir(r".\datasets\the_lord_of_the_rings")

# Import the dialogues text files and the most talkative character file.
movie_1 = pd.read_table(r"dialogues_the-fellowship-of-the-ring.txt",
                        sep="|", header=0)

movie_2 = pd.read_table(r"dialogues_the-two-towers.txt",
                        sep="|", header=0)

movie_3 = pd.read_table(r"dialogues_the-return-of-the-king.txt",
                        sep="|", header=0)

top_20_by_movie = pd.read_table(r"top_20_by_movie.txt", sep=";", header=0)

# Bind the characters and the dialogues of the movies (two different vectors).
characters = pd.concat([movie_1["Character"], 
                        movie_2["Character"], 
                        movie_3["Character"]],
                        ignore_index=True)

dialogues = pd.concat([movie_1["Dialogue"], 
                       movie_2["Dialogue"], 
                       movie_3["Dialogue"]], 
                       ignore_index=True)

# Get the dialogues of the most talkative characters in a data frame.
dials_per_character = []

for name in top_20_by_movie["Character"]:
    dials_per_character.append({"Dialogue": " ".join(map(str, \
    dialogues[characters == name]))})

dials_per_character = pd.DataFrame(dials_per_character, 
                                   index=top_20_by_movie["Character"])


## Clean the dialogues.

# Convert the dialogues to lowercase.
dials_per_character["Dialogue"] = dials_per_character["Dialogue"].str.lower()

# Remove numbers and ponctuation.
dials_per_character["Dialogue"] = dials_per_character["Dialogue"]\
.str.replace("[^a-z\s]", " ")

# Remove stop words (words which are filtered out).
for word in stopwords.words("english"):
    dials_per_character["Dialogue"] = dials_per_character["Dialogue"]\
    .str.replace("".join(["\\b", word, "\\b"]), "")

# Replace extra whitespaces (two or more).
dials_per_character["Dialogue"] = dials_per_character["Dialogue"]\
.str.replace("(  +)", " ")

# Create a document-term matrix.
vectorizer = CountVectorizer()
doc_term_matrix = vectorizer.fit_transform(dials_per_character["Dialogue"])

# Convert it to a data frame.
doc_term_matrix = pd.DataFrame(doc_term_matrix.toarray(), 
                  columns = vectorizer.get_feature_names(),
                  index = dials_per_character.index)

# Get word count.
count_terms = doc_term_matrix.sum(axis=0).sort_values(ascending=False)

# Plot an histogram of the word count.

# Set the working directory (to save the plots).
os.chdir(r"..\..\scripts\the_lord_of_the_rings")

# ggplot style.
matplotlib.style.use("ggplot")

# Initialize the figure.
f = plt.figure()

# Plot.
ax = count_terms.plot(kind="hist", color="#348abd", bins=30, figsize=(15, 10))

# Remove tick lines in x and y axes.
plt.tick_params(
    axis="both",   # Changes apply to both axes.
    which="both",  # Both major and minor ticks are affected.
    top="off",     # Ticks along the top edge are off.
    right="off")   # Ticks along the right edge are off.

# Add labels.
plt.xlabel("\n# d'occurences", fontsize=14)
plt.ylabel("# de mots", fontsize=14)

# Save the figure.
# plt.savefig(r".\plots\histogram_words.pdf", bbox_inches="tight")

# A lot of words are used just a few times.
# To make things a little bit easier: keep only words >= 90% quantile frequency.
count_terms.quantile(q=0.9)

frequent_words = count_terms[count_terms >= count_terms.quantile(q=0.9)]

# Plot an histogram of the top 10% most frequent words.

# Initialize the figure.
f = plt.figure()

# Plot.
ax = frequent_words.plot(kind="hist", color="#348abd", 
                         bins=30, figsize=(15, 10))

# Remove tick lines in x and y axes.
plt.tick_params(
    axis="both",   # Changes apply to both axes.
    which="both",  # Both major and minor ticks are affected.
    top="off",     # Ticks along the top edge are off.
    right="off")   # Ticks along the right edge are off.

# Add labels.
plt.xlabel("\n# d'occurences", fontsize=14)
plt.ylabel("# de mots", fontsize=14)

# Save the figure.
# plt.savefig(r".\plots\histogram_top_words.pdf", bbox_inches="tight")

# Plot the top 30 most frequent words.

# Initialize the figure.
f = plt.figure()

# Plot.
ax = frequent_words[:30].plot(kind="bar", color="#348abd", figsize=(15, 10))

# Axis limits.
plt.ylim(ymin=0, ymax=200)

# Remove tick lines in x and y axes.
plt.tick_params(
    axis="both",   # Changes apply to both axes.
    which="both",  # Both major and minor ticks are affected.
    top="off",     # Ticks along the top edge are off.
    right="off",   # Ticks along the right edge are off.
    bottom="off")  # Ticks along the bottom edge are off.

# Add labels.
plt.ylabel("# d'occurences", fontsize=14)

# Save the figure.
# plt.savefig(r".\plots\barplot_top_30_words.pdf", bbox_inches="tight")


## Adjacency matrix based on the most frequent words.
"""
We use two different methods. We get the same network between the characters 
with both adjacency matrices but with different weights.
"""

# Filter only the most frequent words.
doc_term_freq = doc_term_matrix[frequent_words.index]

# 1st method.
adj_matrix_1 = np.dot(doc_term_freq, doc_term_freq.T)
# Fill the diagonal with zeros.
np.fill_diagonal(adj_matrix_1, val=0)
# Convert it to a data frame.
adj_matrix_1 = pd.DataFrame(adj_matrix_1, 
                            index=doc_term_freq.index,
                            columns=doc_term_freq.index)

# 2nd method.
# Create a boolean matrix.
doc_term_freq_boolean = doc_term_freq.copy()
doc_term_freq_boolean[doc_term_freq_boolean != 0] = 1
# Compute the adjacency matrix using jaccard similarity.
# See: https://en.wikipedia.org/wiki/Jaccard_index
jaccard_matrix = 1 - pdist(doc_term_freq_boolean, "jaccard")
adj_matrix_2 = pd.DataFrame(squareform(jaccard_matrix), 
                            index=doc_term_freq.index, 
                            columns=doc_term_freq.index)

# Save both adjacency matrix.
# adj_matrix_1.to_csv(r"..\..\datasets\the_lord_of_the_rings\adj_matrix_1.txt", 
#                     sep=";", encoding="utf-8")
# adj_matrix_2.to_csv(r"..\..\datasets\the_lord_of_the_rings\adj_matrix_2.txt", 
#                     sep=";", encoding="utf-8")


## Draw heatmaps with the adjacency matrices.

# Initialize the figure.
f, ax = plt.subplots()
f.set_size_inches(10, 10)

# Plot.
heatmap = plt.pcolor(adj_matrix_2, cmap=plt.cm.bone_r, alpha=0.8)

# Put the major ticks at the middle of each cell.
ax.set_yticks(np.arange(adj_matrix_2.shape[0]) + 0.5, minor=False)
ax.set_xticks(np.arange(adj_matrix_2.shape[1]) + 0.5, minor=False)

# Set the labels.
ax.set_xticklabels(adj_matrix_2.index, minor=False)
ax.set_yticklabels(adj_matrix_2.index, minor=False)

# Remove tick lines in x and y axes.
plt.tick_params(
    axis="both",   # Changes apply to both axes.
    which="both",  # Both major and minor ticks are affected.
    top="off",     # Ticks along the top edge are off.
    right="off",   # Ticks along the right edge are off.
    left="off",    # Ticks along the left edge are off 
    bottom="off")  # Ticks along the bottom edge are off.

# Rotate the xlabels.
plt.xticks(rotation=90)

# Invert the vertical axis.
ax.invert_yaxis()

# Save the figure.
# plt.savefig(r".\plots\heatmap.pdf", bbox_inches="tight")

# Same plot ordered by race: hobbits, men, elves, etc.
Humans = ["ARAGORN", "THÉODEN", "FARAMIR", "BOROMIR", "ÉOWYN"]
Hobbits = ["FRODO", "SAM", "PIPPIN", "MERRY", "BILBO"]
Elves = ["GALADRIEL", "LEGOLAS", "ELROND", "ARWEN"]
Wizards = ["GANDALF", "SARUMAN"]
Other = ["GOLLUM", "GIMLI", "TREEBEARD", "SMÉAGOL"]

sorter = Humans + Hobbits + Elves + Wizards + Other

adj_matrix_2_sorter = adj_matrix_2

# Sort the columns.
adj_matrix_2_sorter = adj_matrix_2_sorter[sorter]

# Sort the index.
adj_matrix_2_sorter = adj_matrix_2_sorter.reindex(sorter)

# Initialize the figure.
f, ax = plt.subplots()
f.set_size_inches(10, 10)

# Plot.
heatmap = plt.pcolor(adj_matrix_2_sorter, cmap=plt.cm.bone_r, alpha=0.8)

# Put the major ticks at the middle of each cell.
ax.set_yticks(np.arange(adj_matrix_2_sorter.shape[0]) + 0.5, minor=False)
ax.set_xticks(np.arange(adj_matrix_2_sorter.shape[1]) + 0.5, minor=False)

# Set the labels.
ax.set_xticklabels(adj_matrix_2_sorter.index, minor=False)
ax.set_yticklabels(adj_matrix_2_sorter.index, minor=False)

# Remove tick lines in x and y axes.
plt.tick_params(
    axis="both",   # Changes apply to both axes.
    which="both",  # Both major and minor ticks are affected.
    top="off",     # Ticks along the top edge are off.
    right="off",   # Ticks along the right edge are off.
    left="off",    # Ticks along the left edge are off 
    bottom="off")  # Ticks along the bottom edge are off.

# Rotate the xlabels.
plt.xticks(rotation=90)

# Invert the vertical axis.
ax.invert_yaxis()

# Save the figure.
# plt.savefig(r".\plots\heatmap_2.pdf", bbox_inches="tight")

# Similar heatmaps with Seaborn.

f = plt.figure()
plt.figure(figsize=(10, 10))

# Plot.
heatmap = sns.heatmap(adj_matrix_2, linewidths=0.4, cmap="bone_r", cbar=False)

# Remove axis title.
plt.xlabel("")
plt.ylabel("")

# Save the figure.
# plt.savefig(r".\plots\heatmap_seaborn.pdf", bbox_inches="tight")

# Same plot ordered by race: hobbits, men, elves, etc.

# Initialize the figure.
f = plt.figure()
plt.figure(figsize=(10, 10))

# Plot.
heatmap = sns.heatmap(adj_matrix_2_sorter, linewidths=0.4, 
                      cmap="bone_r", cbar=False)

# Remove axis title.
plt.xlabel("")
plt.ylabel("")

# Save the figure.
# plt.savefig(r".\plots\heatmap_2_seaborn.pdf", bbox_inches="tight")

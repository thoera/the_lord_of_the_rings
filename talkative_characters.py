# -*- coding: utf-8 -*-

"""
A script to find the most talkative characters in the three movies.
"""

import os
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# Set the working directory.
os.chdir(r".\datasets\the_lord_of_the_rings")

# Import the dialogues text files.
movie_1 = pd.read_table(r"dialogues_the-fellowship-of-the-ring.txt",
                        sep="|", header=0)

movie_2 = pd.read_table(r"dialogues_the-two-towers.txt",
                        sep="|", header=0)

movie_3 = pd.read_table(r"dialogues_the-return-of-the-king.txt",
                        sep="|", header=0)

# Concatenate the names of the characters in the three movies.
characters = pd.concat([movie_1["Character"], movie_2["Character"], 
                        movie_3["Character"]])

# Remove unwanted trailing whitespaces.
characters = characters.str.rstrip()

# Replace some characters names to standardize them.
characters = characters.replace({"DEAGOL":"DÉAGOL", "EOMER":"ÉOMER", 
                                 "EOWYN":"ÉOWYN", "EÓWYN":"ÉOWYN", 
                                 "SMEAGOL":"SMÉAGOL", "THEODEN":"THÉODEN",
                                 "WITCH-KING":"WITCH KING"})

# Convert "characters" to a data frame.
characters = pd.DataFrame(characters)

# Reset the index.
characters = characters.reset_index(drop=True)

# Add the movie number: 1, 2 or 3.
characters["movie_number"] = np.repeat([1, 2, 3], [len(movie_1),
                                                   len(movie_2), len(movie_3)])

# Get the top 20 most talkative characters.
top_20 = pd.value_counts(characters["Character"]).head(n=20)


## Barplots of the top 20.

# Set the working directory.
os.chdir(r"..\..\scripts\the_lord_of_the_rings")

# ggplot style.
matplotlib.style.use("ggplot")

# Initialize the figure.
f = plt.figure()

# Plot.
ax = top_20.plot(kind="bar", color="#348abd", figsize=(15, 10), ax=f.gca())

# Remove tick lines in x and y axes.
plt.tick_params(
    axis="both",   # Changes apply to both axes.
    which="both",  # Both major and minor ticks are affected.
    top="off",     # Ticks along the top edge are off.
    bottom="off",  # Ticks along the bottom edge are off.
    right="off")   # Ticks along the right edge are off.

# Add labels.
plt.xlabel("")
plt.ylabel("# de dialogues", fontsize=14)

# Save the figure.
# plt.savefig(r".\plots\talkative.pdf", bbox_inches="tight")

# Keep only the characters in the top 20.
characters_top_20 = top_20.index.get_values()
characters_top_20 = characters[characters["Character"].isin(characters_top_20)]

# Group by movie number.
top_20_by_movie = characters_top_20.groupby("movie_number")
top_20_by_movie = top_20_by_movie["Character"].value_counts()
top_20_by_movie = top_20_by_movie.unstack().fillna(0)

# Transpose the data frame.
top_20_by_movie = top_20_by_movie.transpose()

# Sort by the total.
top_20_by_movie["Total"] = top_20_by_movie.sum(axis=1)
top_20_by_movie = top_20_by_movie.sort_values(by="Total", ascending=False)

# Initialize the figure.
f = plt.figure()

# Plot.    
ax = top_20_by_movie.ix[:, 0:3].plot(kind="bar", stacked=True, 
                                     color=["#e24a33", "#348abd", "#988ed5"], 
                                     figsize=(15, 10), ax=f.gca())

# Remove tick lines in x and y axes.
plt.tick_params(
    axis="both",   # Changes apply to both axes.
    which="both",  # Both major and minor ticks are affected.
    top="off",     # Ticks along the top edge are off.
    bottom="off",  # Ticks along the bottom edge are off.
    right="off")   # Ticks along the right edge are off.

# Add labels.
plt.xlabel("")
plt.ylabel("# de dialogues", fontsize=14)

# Legend
leg = plt.legend(["The Fellowship of the Ring", "The Two Towers", 
                  "The Return of the King"], frameon=False, loc="upper center", 
                  bbox_to_anchor=(0.5, -0.12), ncol=3)
for text in leg.get_texts():
    plt.setp(text, color = "#555555")

# Save the figure.
# plt.savefig(r".\plots\talkative_by_movie.pdf", bbox_inches="tight")

# Export "top_20_by_movie".
# top_20_by_movie.to_csv(r"..\datasets\the_lord_of_the_rings\top_20_by_movie.txt", 
#                        sep=";", encoding="utf-8")

## Same plots with seaborn.

# Top 20.

# Initialize the figure.
f = plt.figure()
plt.figure(figsize=(15, 10))

# Plot.
ax = sns.countplot(x="Character", data=characters_top_20, 
                   order=top_20.index, color="#348abd")

# Add labels.
plt.xlabel("")
plt.ylabel("# de dialogues", fontsize=14)
plt.xticks(rotation=90)

# Save the figure.
# plt.savefig(r".\plots\talkative_seaborn.pdf", bbox_inches="tight")

# Top 20 by movie.

# Initialize the figure.
f = plt.figure()
plt.figure(figsize=(15, 10))

# Plot.
ax = sns.countplot(x="Character", data=characters_top_20, 
                   order=top_20.index, hue="movie_number", 
                   palette=["#e24a33", "#348abd", "#988ed5"])

# Add labels.
plt.xlabel("")
plt.ylabel("# de dialogues", fontsize=14)
plt.xticks(rotation=90)

# Set ylim.
ax.set(ylim=(0, 170))

# Legend
leg = plt.legend(["The Fellowship of the Ring", "The Two Towers", 
                  "The Return of the King"], frameon=False, loc="upper center", 
                  bbox_to_anchor=(0.5, -0.12), ncol=3)
for text in leg.get_texts():
    plt.setp(text, color = "#555555", fontsize=14)

# Save the figure.
# plt.savefig(r".\plots\talkative_by_movie_seaborn.pdf", bbox_inches="tight")

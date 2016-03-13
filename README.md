![header](the_lord_of_the_rings_by_riku_rocks.jpg?raw=true)

<br>

Ce (modeste) projet à deux objectifs : d'une part, faire un peu de *text mining* avec Python et d'autre part, utiliser `Gephi` et ses nombreuses possibilités pour représenter de manière informative (et dans la mesure du possible esthétique et plaisante) les résultats de l'analyse textuelle préalable.

L'article [*Star Wars* de Gaston Sanchez](http://gastonsanchez.com/got-plot/crunching-data/2013/02/03/Star-Wars-Arc-Diagram/) est la source principale d'inspiration de ce projet. En passant, j'encourage fortement la lecture de son site !

En quelques mots, l'objectif de ce projet et la recette utilisée. L'idée principale était de construire un `réseau` (ou `graph`) entre les personnages les plus *bavards* des trois films du *Seigneur des Anneaux*. 
Dans l'ordre, les différentes étapes permettant la représentation graphique finale sont :
* récupérer les scripts des films et les "nettoyer" pour les rendre utilisables ;
* identifier les personnages les plus bavards sur l'ensemble de la trilogie (i.e. ceux avec le plus de dialogues) ;
* construire un réseau (basé sur la proximité du vocabulaire utilisé) entre les personnages ; 
* représenter graphiquement le réseau obtenu.

## Les scripts

Plusieurs sites se sont fait une spécialité de fournir des scripts de films ([IMSDB](http://www.imsdb.com/), [Simply Scripts](http://www.simplyscripts.com/movie.html), etc.). Cependant, il est rare que ceux-ci soient uniformisés et directement utilisables pour une analyse quelconque.

Pour exemple, voici les premières lignes de *The Fellowship of the Ring* :

```
BLACK SCREEN

SUPER: New Line Cinema Presents

SUPER: A Wingnut Films Production

BLACK CONTINUES... ELVISH SINGING....A WOMAN'S VOICE IS
whispering, tinged with SADNESS and REGRET:

                    GALADRIEL (V.O.)
              (Elvish: subtitled)
          "I amar prestar sen: han mathon ne nen,
          han mathon ne chae...a han noston ned
          wilith."
              (English:)
          The world is changed: I feel it in the
          water, I feel it in the earth, I smell it
          in the air...Much that once was is lost,
          for none now live who remember it.

SUPER: THE LORD OF THE RINGS

EXT. PROLOGUE -- DAY

IMAGE: FLICKERING FIRELIGHT. The NOLDORIN FORGE in EREGION.
MOLTEN GOLD POURS from the lip of an IRON LADLE.

                    GALADRIEL (V.O.)
          It began with the forging of the Great
          Rings.

IMAGE: THREE RINGS, each set with a single GEM, are received
by the HIGH ELVES-GALADRIEL, GIL-GALAD and CIRDAN.

                    GALADRIEL (V.O.) (CONT'D)
          Three were given to the Elves, immortal,
          wisest...fairest of all beings.
```

Le premier objectif consiste ainsi à "nettoyer" les scripts afin de ne conserver que les noms des personnages et leurs dialogues. Pour exemple, voici le programme utilisé sur le premier film de la trilogie.

```Python
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
```

Le "nettoyage" en tant que tel du script est réalisé avec deux expressions régulières : l'une pour isoler le nom des personnages et la seconde pour isoler les dialogues eux-mêmes.

Le résultat obtenu est de la forme suivante :

```
Character|Dialogue
GALADRIEL|han mathon ne chae...a han noston ned wilith." The world is changed: I feel it in the water, I feel it in the earth, I smell it in the air...Much that once was is lost, for none now live who remember it. 
GALADRIEL|It began with the forging of the Great Rings. 
GALADRIEL|Three were given to the Elves, immortal, wisest...fairest of all beings. 
GALADRIEL|Seven to the Dwarf Lords, great miners and craftsmen of the mountain halls. 
GALADRIEL|And Nine...nine rings were gifted to the race of Men who, above all else, desire power. 
GALADRIEL|For within these rings was bound the strength and will to govern each race. 
GALADRIEL|But they were all of them deceived. 
GALADRIEL|...for another ring was made. 
GALADRIEL|In the land of Mordor, in the fires of Mount Doom, the Dark Lord Sauron forged in secret a Master Ring to control all others. 
GALADRIEL|...and into this Ring he poured his cruelty, his malice and his will to dominate all life. 
GALADRIEL|One Ring to rule them all...
```

## Les personnages les plus bavards

Une fois les scripts rendus utilisables, il est alors possible de déterminer quels sont les personnages les plus bavards de la trilogie. Ceci peut notamment être fait en utilisant la fonction `value_counts()` de la bibliothèque `pandas` après avoir concaténé les trois scripts nettoyés.

```Python
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
```

Le graphique suivant présente les vingt personnages ayant le plus de dialogues sur l'ensemble de la trilogie.

[![talkative](/plots/talkative.png?raw=true)](/plots/talkative.pdf)

Sans surprise, le personnage le plus bavard est **Gandalf** suivi de près par **Frodo**, **Sam** et **Aragorn**.

Il est également possible de visualiser la répartition de chacun des trois films dans ce total ce qui permet de remarquer l'importance grandissante que prennent **Sam** et **Gollum** ou, au contraire, la "disparition" de personnages comme **Galadriel** ou **Bilbo** au fil de l'histoire.

[![talkative_by_movie](/plots/talkative_by_movie.png?raw=true)](/plots/talkative_by_movie.pdf)

## *Text mining* et matrices d'adjacence 

Une fois identifié les personnages les plus importants (i.e. les plus bavards), l'étape suivante consiste à construire un réseau entre eux. Parmi les différentes méthodes possibles, celle choisie ici consiste à construire une matrice d'adjacence basée sur la similarité de vocabulaire entre les personnages.

Cette technique nécessite notamment d'effectuer une analyse sémantique et de construire une matrice de type termes-documents. Deux bibliothèques en particulier permettent de grandement faciliter ces opérations : le `Natural Language Toolkit` (ou `nltk` de son petit nom) et le module Feature Extraction de `Scikit-Learn`.


*Header réalisé par [Riku-Rocks.](http://riku-rocks.deviantart.com/art/Lord-of-the-Rings-Wallpaper-98966185)*

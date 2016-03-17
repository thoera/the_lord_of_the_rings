![header](header_the_lord_of_the_rings.jpg?raw=true)

<br>

Ce projet avait deux objectifs : d'une part, présenter quelques exemples de *text mining* en Python (expressions régulières, matrice documents-termes, etc.) et d'autre part, utiliser `Gephi` et ses nombreuses possibilités pour représenter de manière informative/esthétique/plaisante/rigolote les résultats de l'analyse textuelle préalable.

L'idée principale était de construire un `réseau` (ou `graph`) entre les personnages les plus *bavards* de la trilogie du *Seigneur des Anneaux*. 
La "recette" utilisée est la suivante :
* récupérer les scripts des films et les nettoyer pour les rendre utilisables ;
* identifier les vingt personnages les plus bavards sur l'ensemble de la trilogie (i.e. ceux avec le plus grand nombre de dialogues) ;
* construire un réseau basé sur la proximité du vocabulaire utilisé entre les personnages ; 
* représenter graphiquement le réseau obtenu.

L'article [*Star Wars* de Gaston Sanchez](http://gastonsanchez.com/got-plot/crunching-data/2013/02/03/Star-Wars-Arc-Diagram/) fut la principale source d'inspiration de ce projet. (J'encourage d'ailleurs fortement la lecture de son site !)

## Les scripts

Plusieurs sites se sont fait une spécialité de fournir des scripts de films ([IMSDB](http://www.imsdb.com/), [Simply Scripts](http://www.simplyscripts.com/movie.html), etc.). Cependant, il est rare que ceux-ci soient directement utilisables pour une analyse quelconque.

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
```

Le premier objectif consiste ainsi à nettoyer les scripts afin de ne conserver que les noms des personnages et leurs dialogues. Pour exemple, voici le programme utilisé sur le premier film de la trilogie.

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

Le nettoyage en tant que tel du script est réalisé avec deux expressions régulières : une première permettant d'isoler le nom des personnages et une seconde afin d'isoler les dialogues eux-mêmes.

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

Une fois les scripts rendus utilisables, il est alors possible de déterminer quels sont les personnages les plus bavards de la trilogie. J'utilise principalement, ici et dans la suite, la bibliothèque `pandas` pour sa flexibilité, sa lisibilité, son intégration avec `scikit-learn` et `numpy`, son large choix de fonctions et ses performances.

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

Le graphique suivant présente les vingt personnages ayant le plus de dialogues sur l'ensemble des trois films (deux versions de ce graphique et des suivants existent : l'une avec `matplotlib` et l'autre avec `seaborn`).

[![talkative](/plots/talkative.png?raw=true)](/plots/talkative.pdf)

Sans surprise, le personnage le plus bavard est **Gandalf** suivi de près par **Frodo**. Viennent ensuite **Sam** et **Aragorn**. Notons l'absence remarquée de **Sauron**. Le seul personnage maléfique présent étant **Saruman** (et, selon votre interprétation ou sensibilité, **Gollum** ?).

Il est également possible de visualiser la répartition de chacun des trois films dans ce total. Ceci permet notamment de remarquer l'importance grandissante que prennent **Sam** et **Gollum** ou, au contraire, la "disparition" progressive de personnages comme **Galadriel** ou **Bilbo**.

[![talkative_by_movie](/plots/talkative_by_movie.png?raw=true)](/plots/talkative_by_movie.pdf)

## *Text mining* et matrice d'adjacence 

Une fois identifié les personnages les plus importants (i.e. les plus bavards), l'étape suivante consiste à construire un réseau entre eux. Parmi les différentes méthodes possibles, celle ici choisie consiste à construire une matrice d'adjacence basée sur la similarité de vocabulaire utilisé par les vingt personnages.

Cette technique nécessite d'effectuer une analyse sémantique et de construire ce que l'on appelle une [matrice termes-documents](https://en.wikipedia.org/wiki/Document-term_matrix). En Python, deux bibliothèques en particulier permettent de faciliter grandement ces opérations : le `Natural Language Toolkit` (ou encore `nltk` de son petit nom) et le module `Feature Extraction` de `Scikit-Learn`.

Les opérations de *text mining* ici effectuées consistent essentiellement à convertir l'ensemble des caractères en bas-de-casse, à supprimer des dialogues chiffres et signes de ponctuation, à éliminer les mots vides (ou *stop words*, en anglais) qui correspondent aux mots extrêmement communs et enfin, à supprimer les espaces supplémentaires.

```Python
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
```

On peut alors créer une matrice de type termes-documents où les termes sont l'ensemble des mots utilisés et les documents, les personnages.

```Python
# Create a document-term matrix.
vectorizer = CountVectorizer()
doc_term_matrix = vectorizer.fit_transform(dials_per_character["Dialogue"])

# Convert it to a data frame.
doc_term_matrix = pd.DataFrame(doc_term_matrix.toarray(), 
                  columns = vectorizer.get_feature_names(),
                  index = dials_per_character.index)

# Get word count.
count_terms = doc_term_matrix.sum(axis=0).sort_values(ascending=False)
```

Ce format de matrice permet notamment de compter facilement le nombre d'occurences pour chacun des mots employés. L'histogramme suivant présente la distribution obtenue.

[![histogram_words](/plots/histogram_words.png?raw=true)](/plots/histogram_words.pdf)

La très grande majorité des mots employés apparaissent moins d'une dizaine de fois. Afin de simplifier l'analyse à venir, l'on ne conserve dans la suite que les mots dont la fréquence est supérieur au 9e décile (soit 9 occurences).

```Python
# A lot of words are used just a few times.
# To make things a little bit easier: keep only words >= 90% quantile frequency.
count_terms.quantile(q=0.9)

frequent_words = count_terms[count_terms >= count_terms.quantile(q=0.9)]
```

[![histogram_top_words](/plots/histogram_top_words.png?raw=true)](/plots/histogram_top_words.pdf)

[![barplot_top_30_words](/plots/barplot_top_30_words.png?raw=true)](/plots/barplot_top_30_words.pdf)

[![heatmap_seaborn](/plots/heatmap_seaborn.png?raw=true)](/plots/heatmap_seaborn.pdf)

[![heatmap_2_seaborn](/plots/heatmap_2_seaborn.png?raw=true)](/plots/heatmap_2_seaborn.pdf)

[![network_white](/plots/network_white_900.png?raw=true)](/plots/network_white.pdf)

[![network_white_lego](/plots/network_white_lego_900.png?raw=true)](/plots/network_white_lego.pdf)

*Header réalisé par [Riku-Rocks.](http://riku-rocks.deviantart.com/art/Lord-of-the-Rings-Wallpaper-98966185)*

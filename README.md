![header](header_the_lord_of_the_rings.jpg?raw=true)

<br>

L'objectif de ce projet était double : d'une part, présenter quelques exemples de *text mining* en Python (expressions régulières, matrice documents-termes, etc.) et d'autre part, utiliser `Gephi` et ses nombreuses possibilités pour représenter de manière informative/esthétique/plaisante/rigolote (à vous de faire votre choix) les résultats de l'analyse textuelle préalable.

L'idée principale était de construire un `réseau` (ou `graphe`) entre les personnages les plus *bavards* de la trilogie du *Seigneur des Anneaux*. 
La "recette" utilisée est la suivante :
* récupérer les scripts des films et les nettoyer pour les rendre utilisables ;
* identifier les vingt personnages les plus bavards sur l'ensemble de la trilogie (i.e. ceux avec le plus grand nombre de dialogues) ;
* construire un réseau basé sur la proximité du vocabulaire utilisé entre les personnages ; 
* représenter graphiquement le réseau obtenu.

L'article [*Star Wars* de Gaston Sanchez](http://gastonsanchez.com/got-plot/crunching-data/2013/02/03/Star-Wars-Arc-Diagram/) fut la principale source d'inspiration de ce projet. (J'encourage d'ailleurs fortement la lecture de son site !)

## Les scripts

Plusieurs sites se sont fait une spécialité de fournir des scripts de films ([IMSDB](http://www.imsdb.com/), [Simply Scripts](http://www.simplyscripts.com/movie.html), etc.). Cependant, il est rare que ceux-ci soient directement utilisables pour une analyse textuelle quelconque.

Voici les premières lignes de *The Fellowship of the Ring* :

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

Une fois les trois scripts récupérés, le premier objectif consiste à les nettoyer afin de ne conserver que les noms des personnages et leurs dialogues associés. Pour exemple, le programme utilisé sur le premier film de la trilogie est le suivant :

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

Le nettoyage en tant que tel du script est réalisé avec deux expressions régulières : une première permettant d'isoler le nom des personnages et une seconde isolant les dialogues eux-mêmes.

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

Le graphique ci-dessous présente les vingt personnages ayant le plus de lignes de dialogue sur l'ensemble des trois films.

[![talkative](/plots/talkative_scaled.png?raw=true)](/plots/talkative.pdf)

Sans surprise, le personnage le plus bavard est **Gandalf**,  suivi de près par **Frodo**. Viennent ensuite **Sam** et **Aragorn**. Notons par contre l'absence de **Sauron** parmi les personnages principaux. Le seul personnage maléfique présent étant **Saruman** (et, selon votre interprétation ou sensibilité, **Gollum**).

Il est également possible de visualiser la répartition de chacun des trois films dans ce total. Ceci permet notamment de remarquer l'importance grandissante que prennent **Sam** et **Gollum** au fil de l'histoire ou, au contraire, la "disparition" progressive de personnages comme **Galadriel** ou **Bilbo**.

[![talkative_by_movie](/plots/talkative_by_movie_scaled.png?raw=true)](/plots/talkative_by_movie.pdf)

## *Text mining* et matrice d'adjacence

Une fois les personnages les plus importants (i.e. les plus bavards) identifiés, l'étape suivante consiste à construire un réseau les reliant entre eux. Parmi les différentes méthodes possibles, celle ici choisie consiste à construire une matrice d'adjacence basée sur la similarité du vocabulaire utilisé.

Cette technique nécessite d'effectuer une analyse sémantique et de construire une [matrice termes-documents](https://en.wikipedia.org/wiki/Document-term_matrix). En Python, deux bibliothèques en particulier permettent de faciliter grandement ces opérations : le `Natural Language Toolkit` (ou encore `nltk` de son petit nom) et le module `Feature Extraction` de `Scikit-Learn`.

Les opérations de *text mining* réalisées consistent essentiellement à convertir l'ensemble des caractères en bas-de-casse, à supprimer des dialogues les chiffres et signes de ponctuation, à éliminer les mots vides (ou *stop words*, en anglais) qui correspondent aux mots très communs du language et enfin, à supprimer les espaces supplémentaires.

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

On peut ensuite créer une matrice de type termes-documents où les termes correspondent aux différents mots utilisés et les documents aux personnages.

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

Ce format de matrice permet notamment de compter facilement le nombre d'occurences de chacun des mots employés. L'histogramme suivant présente la distribution obtenue.

[![histogram_words](/plots/histogram_words_scaled.png?raw=true)](/plots/histogram_words.pdf)

La très grande majorité des mots employés apparaissent moins d'une dizaine de fois. Afin de simplifier l'analyse à venir, l'on ne conserve dans la suite que les mots dont la fréquence est supérieur au 9e décile (soit 9 occurences).

```Python
# A lot of words are used just a few times.
# To make things a little bit easier: keep only words >= 90% quantile frequency.
count_terms.quantile(q=0.9)

frequent_words = count_terms[count_terms >= count_terms.quantile(q=0.9)]
```

Voici la nouvelle distribution obtenue suite à cette étape de sélection plutôt drastique.

[![histogram_top_words](/plots/histogram_top_words_scaled.png?raw=true)](/plots/histogram_top_words.pdf)

Si la très grande majorité des mots apparaissent moins d'une vingtaine de fois (preuve d'une certaine richesse de vocabulaire), quelques-uns sont par contre utilisés plus de cent fois.

Les trente mots les plus utilisés sont les suivants :

[![barplot_top_30_words](/plots/barplot_top_30_words_scaled.png?raw=true)](/plots/barplot_top_30_words.pdf)

On y retrouve des noms de personnages comme **Frodo** (de loin le mot le plus utilisé avec 179 répétitions), **Gandalf**, **Aragorn** ou encore, dans une moindre mesure, **Sauron**, différents verbes (aller, venir, savoir, etc.) mais également des mots emblématiques de l'œuvre de J. R. R. Tolkien comme *anneau*, *unique*, *seigneur*, etc.

À présent, on peut construire une matrice d'adjacence qui permettra de quantifier la proximité entre les différents personnages.
Le code suivant permet de créer deux matrices d'adjacence : la première étant calculée comme le produit matriciel XX' (où X est la matrice termes-documents) et la seconde étant basée sur l'[indice de Jaccard](https://en.wikipedia.org/wiki/Jaccard_index#Generalized_Jaccard_similarity_and_distance).

```Python
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
```

Notons que ces deux matrices d'adjacence aboutissent à la construction d'un même réseau (au moins au niveau des liens entre personnages - les arrêtes étant, elles, différentes).

Une des façons usuelles de visualiser un réseau consiste à créer une *heatmap*. Cette représentation permet de faire plusieurs observations plutôt générales : 
* les trois personnages les plus bavards (**Gandalf**, **Frodo** et **Sam**) partagent une grande partie de leur vocabulaire en commun ;
* **Aragorn** apparaît à la fois proche de **Gandalf** et, de façon un peu plus surprenante, d'**Elrond** ;
* **Merry** et **Pippin** sont très liés ;
* **Sméagol** et **Éowyn** semblent être les deux personnages les plus isolés ;
* etc.

[![heatmap_seaborn](/plots/heatmap_seaborn_scaled.png?raw=true)](/plots/heatmap_seaborn.pdf)

Sur une *heatmap*, ordonner autrement les personnages permet souvent de mettre en évidence des caractéristiques différentes d'un réseau. 
Si sur la matrice ci-dessus, les personnages étaient ordonnés du plus bavard au moins bavard, on peut également choisir de les ordonner différemment. Par exemple, selon leur race : Humains, Hobbits, Elfes, Magiciens et autres (Nain, Ent et **Gollum**/**Sméagol** bien que ce dernier soit techniquement un Hobbit).

[![heatmap_2_seaborn](/plots/heatmap_2_seaborn_scaled.png?raw=true)](/plots/heatmap_2_seaborn.pdf)

Cet ordonnancement différent met ainsi en évidence les liens forts qui peuvent exister entre Hobbits ou au contraire la faible proximité apparente entre les Hommes. De même, les liens entre Elfes semblent, sur cette représentation, assez distants.

## Visualisation du réseau

La dernière étape de ce projet consiste à visualiser le réseau sous la forme d'un graphe. J'ai choisi d'utiliser `Gephi` bien que les visualisations présentées ci-après aurait pu être directement réalisées avec `igraph` par exemple.

Une fois la matrice d'ajacence créée, on peut transformer celle-ci en un objet de type "graphe", c'est-à-dire en un ensemble de nœuds reliés par des arrêtes. Les relations entre personnages étant ici symétriques, le graphe ainsi créé est dit non orienté.

Ayant rencontré quelques soucis de compatibilité entre la version de Python (3.5.1) et l'implémentation d'`igraph`, cette étape a été réalisée en R.

Voici le résultat que l'on peut obtenir rapidement avec `Gephi` :

[![network_white](/plots/network_white_scaled.png?raw=true)](/plots/network_white.pdf)

J'ai choisi d'attribuer des couleurs aux nœuds en fonction de la race des personnages afin d'essayer d'appréhender les liens intra et inter-races plutôt que d'essayer de trouver, par exemple, des communautés. 

Les observations que l'on peut faire sont très semblables à celles déjà effectuées. Sans réelle surprise, **Gandalf** se trouve au cœur du réseau et possède des liens très forts avec de nombreux personnages (les membres de la Communauté de l'Anneau). Les Hobbits semblent très proches les uns des autres (et même de **Gollum**) tandis que les liens entre Elfes ou entre Humains sont plus ténus. **Éowyn** et **Faramir** (qui finiront par se marier) sont tous les deux assez éloignés des autres personnages. Tout comme, dans une moindre mesure, **Legolas**.

Après la version sérieuse, voici la version plus "fun" de ce même graphe (le pouvoir combiné de `Gimp`, `Gephi` et `Inkscape`) :

[![network_white_lego](/plots/network_white_lego_scaled.png?raw=true)](/plots/network_white_lego.pdf)

*Header réalisé par [Riku-Rocks.](http://riku-rocks.deviantart.com/art/Lord-of-the-Rings-Wallpaper-98966185)*

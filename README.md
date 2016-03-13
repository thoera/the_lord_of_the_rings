![header](the_lord_of_the_rings_by_riku_rocks.jpg?raw=true)

<br>

Ce (modeste) projet à deux objectifs : d'une part, faire un peu de *text mining* avec Python et d'autre part, utiliser `Gephi` et ses nombreuses possibilités pour représenter de manière informative (et dans la mesure du possible esthétique et plaisante) les résultats de l'analyse textuelle préalable.

L'article [*Star Wars* de Gaston Sanchez](http://gastonsanchez.com/got-plot/crunching-data/2013/02/03/Star-Wars-Arc-Diagram/) est la source d'inspiration de ce projet. J'encourage fortement la lecture de son site !

En quelques mots, l'objectif de ce projet et la recette utilisée. L'idée principale était de construire un `réseau` (ou `graph`) entre les personnages les plus *bavards* des trois films du *Seigneur des Anneaux*. 
Dans l'ordre, les différentes étapes permettant la représentation graphique finale sont :
* trouver les scripts des films et les nettoyer pour les rendre utilisables ;
* identifier les personnages les plus bavards sur l'ensemble de la trilogie (i.e. ceux avec le plus de dialogues) ;
* construire un réseau (basé sur la proximité du vocabulaire utilisé) entre les personnages ; 
* représenter graphiquement le réseau obtenu.

## Les scripts

Plusieurs sites se sont fait une spécialité de fournir des scripts de films ([IMSDB](http://www.imsdb.com/), [Simply Scripts](http://www.simplyscripts.com/movie.html), etc.). Cependant, il est rare que ceux-ci soient uniformisés et directement utilisables pour une analyse quelconque.

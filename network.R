## A script to create graphs from the adjacency matrices.

# Load igraph.
library(igraph)

# Set the working directory.
setwd("the_lord_of_the_rings")

# Import "top_20_by_movie.txt".
top_20_by_movie <- read.table("./datasets/top_20_by_movie.txt", header = TRUE,
                              sep = ";", stringsAsFactors = FALSE,
                              encoding = "UTF-8", row.names = 1)

# Import the adjacency matrices.
adj_matrix_1 <- read.table("./datasets/adj_matrix_1.txt", header = TRUE, 
                           sep = ";", stringsAsFactors = FALSE, 
                           encoding = "UTF-8", row.names = 1)

adj_matrix_2 <- read.table("./datasets/adj_matrix_2.txt", header = TRUE, 
                           sep = ";", stringsAsFactors = FALSE, 
                           encoding = "UTF-8", row.names = 1)

# Sort characters according to their race.
Humans <- list("ARAGORN", "THÉODEN", "FARAMIR", "BOROMIR", "ÉOWYN")
Hobbits <- list("FRODO", "SAM", "PIPPIN", "MERRY", "BILBO")
Elves <- list("GALADRIEL", "LEGOLAS", "ELROND", "ARWEN")
Wizards <- list("GANDALF", "SARUMAN")
Other <- list("GOLLUM", "GIMLI", "TREEBEARD", "SMÉAGOL")

# This function create two data frames: one for the edges and another 
# for the nodes. The only difference between the two adjacency matrices is that 
# they give different weights for the edges.
graph_function <- function(adj_matrix) {
  
  # Create graph from the adjacency matrices.
  graph_chars <- graph_from_adjacency_matrix(as.matrix(adj_matrix),
                                             mode = "undirected",
                                             weighted = TRUE, diag = FALSE)

  # Get edge lists.
  edges <- data.frame(as_edgelist(graph_chars))
  colnames(edges) <- c("Source", "Target")
  
  # Weights.
  edges$Weight <- E(graph_chars)$weight
  
  # Undirected graph.
  edges$Type <- "Undirected"
  
  # Create a data frame for the nodes.
  nodes <- data.frame("ID" = rownames(top_20_by_movie))

  # Labels (for Gephi).
  nodes$Label <- nodes$ID
  
  # Size of the nodes.
  nodes$Size <- top_20_by_movie$Total
  
  # Color of the nodes.
  nodes$Color[nodes$ID %in% Humans] <- 1
  nodes$Color[nodes$ID %in% Hobbits] <- 2
  nodes$Color[nodes$ID %in% Elves] <- 3
  nodes$Color[nodes$ID %in% Wizards] <- 4
  nodes$Color[nodes$ID %in% Other] <- 5

  # Put edges and nodes in a list (easiest way to return more than one object).
  edges_nodes <- list(edges, nodes)

  return(edges_nodes)
}

# Get edges and nodes from the 1st adjacency matrix.
edges_nodes_1 <- graph_function(adj_matrix_1)

# Get edges and nodes from the 2nd adjacency matrix.
edges_nodes_2 <- graph_function(adj_matrix_2)

# Save the files.
# write.csv(edges_nodes_1[[1]], file = "./datasets/graph_1_edges.csv", 
#           row.names = FALSE, fileEncoding = "UTF-8")

# write.csv(edges_nodes_2[[1]], file = "./datasets/graph_2_edges.csv", 
#           row.names = FALSE, fileEncoding = "UTF-8")

# write.csv(edges_nodes_1[[2]], file="./datasets/graph_nodes.csv", 
#           row.names = FALSE, fileEncoding = "UTF-8")
